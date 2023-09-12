import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from loan_agent import LoanAgent
import logging
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

openai_api_key = os.getenv('OPENAI_API_KEY')

def compare_responses(real_response, generated_response) -> bool:
    try:
        # Try to convert the responses to floats and compare them
        return float(real_response) == float(generated_response)
    except ValueError:
        # If the conversion fails, compare the responses as strings
        return real_response == generated_response

def performance_pipeline(csv_file_path: str, agent: LoanAgent) -> pd.DataFrame:
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Initialize lists to store the generated responses and whether they match the real ones
    generated_outputs = []
    matches = []
    off_topics = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        try:
            # Get the query and real response
            query = row['query']
            real_response = row['real_response']

            # Generate a response using the agent
            generated_response = agent.ask_performance(query)

            # Store the generated response
            generated_outputs.append(generated_response['response'])

            # Check if the generated response matches the real one
            matches.append(compare_responses(generated_response['response'], real_response))

            off_topics.append(generated_response['off_topic'])

            # Save intermediate results after each iteration
            df_temp = df.iloc[:index+1].copy()
            df_temp['generated_response'] = generated_outputs
            df_temp['generated_off_topic'] = off_topics
            df_temp['match'] = matches
            df_temp.to_csv('intermediate_results.csv', index=False)

        except Exception as e:
            logger.error(f"Error at index {index}: {e}")

    # Add the generated responses and matches to the DataFrame
    df['generated_response'] = generated_outputs
    df['generated_off_topic'] = off_topics
    df['match'] = matches

    # Calculate and print the classification metrics for the 'match' column when 'off_topic' is False
    on_topic_df = df[df['off_topic'] == False]
    print('\nOn-topic match classification metrics:')
    print('Accuracy:', accuracy_score(on_topic_df['match'], [True]*len(on_topic_df)))
    print('Precision:', precision_score(on_topic_df['match'], [True]*len(on_topic_df)))
    print('Recall:', recall_score(on_topic_df['match'], [True]*len(on_topic_df)))
    print('F1 score:', f1_score(on_topic_df['match'], [True]*len(on_topic_df)))

    return df

if __name__ == "__main__":
    # Initialize the agent
    agent = LoanAgent(openai_api_key, xml_file_path='./tests/test.xml')

    # Run the performance pipeline
    df = performance_pipeline('./tests/tester_clutch.csv', agent)
    df.to_csv('./tests/final_results.csv', index=False)
    # Print the results
    print(df)