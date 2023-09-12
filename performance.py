import pandas as pd
from loan_agent import LoanAgent
import os
import logging
from dotenv import load_dotenv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

# Now you can access the variables using os.environ
openai_api_key = os.getenv('OPENAI_API_KEY')

def performance_pipeline(csv_file_path: str, agent: LoanAgent) -> pd.DataFrame:
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Initialize lists to store the generated responses and whether they match the real ones
    generated_responses = []
    matches = []

    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        # Get the query and real response
        query = row['query']
        real_response = row['real_response']

        # Generate a response using the agent
        generated_response = agent.ask_performance(query)

        # Store the generated response
        generated_responses.append(generated_response)

        # Check if the generated response matches the real one
        matches.append(generated_response == real_response)

    # Add the generated responses and matches to the DataFrame
    df['generated_response'] = generated_responses['response']
    df['generated_off_topic'] = generated_responses['off_topic']
    df['match'] = matches

    # Calculate and print the classification metrics for the 'off_topic' column
    print('Off-topic classification metrics:')
    print('Accuracy:', accuracy_score(df['off_topic'], df['generated_off_topic']))
    print('Precision:', precision_score(df['off_topic'], df['generated_off_topic']))
    print('Recall:', recall_score(df['off_topic'], df['generated_off_topic']))
    print('F1 score:', f1_score(df['off_topic'], df['generated_off_topic']))

    # Calculate and print the classification metrics for the 'match' column
    print('\nMatch classification metrics:')
    print('Accuracy:', accuracy_score(df['match'], df['match']))
    print('Precision:', precision_score(df['match'], df['match']))
    print('Recall:', recall_score(df['match'], df['match']))
    print('F1 score:', f1_score(df['match'], df['match']))

    return df

if __name__ == "__main__":
    # Initialize the agent
    agent = LoanAgent(openai_api_key, xml_file_path='test.xml')

    # Run the performance pipeline
    df = performance_pipeline('tester_clutch.csv', agent)
    df.to_csv('results.csv')
    # Print the results
    print(df)