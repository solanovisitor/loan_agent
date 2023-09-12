import pandas as pd
from agent.agents import Agent  # or wherever Agent is located

def performance_pipeline(csv_file_path: str, agent: Agent) -> pd.DataFrame:
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
        generated_response = agent.ask_performance(query)['response']

        # Store the generated response
        generated_responses.append(generated_response)

        # Check if the generated response matches the real one
        matches.append(generated_response == real_response)

    # Add the generated responses and matches to the DataFrame
    df['generated_response'] = generated_responses
    df['match'] = matches

    return df

if __name__ == "__main__":
    # Initialize the agent
    agent = Agent(openai_api_key='your_openai_api_key', xml_file_path='your_xml_file_path')

    # Run the performance pipeline
    df = performance_pipeline('queries.csv', agent)

    # Print the results
    print(df)