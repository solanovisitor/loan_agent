import os
import logging
import gradio as gr
from loan_agent import LoanAgent
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

# Now you can access the variables using os.environ
openai_api_key = os.getenv('OPENAI_API_KEY')
nut_api_key = os.getenv('NUT_API_KEY')

# Instantiate FitnessAgent here so it remains open
loan_agent = LoanAgent(openai_api_key, nut_api_key)

def get_response(message, history):

    logger.info(f'Chat history: {history}')

    if history:
        for i, chat in enumerate(history[0]):
            formatted_chat_history.append({
                'role': 'user' if i % 2 == 0 else 'assistant',
                'content': chat
            })

        logger.info(formatted_chat_history)
        fitness_agent.chat_history = formatted_chat_history

        logger.info(fitness_agent.chat_history)

    # Get raw chat response
    res = fitness_agent.ask(message)

    chat_response = res['choices'][0]['message']['content']

    return chat_response

def main():

    chat_interface = gr.ChatInterface(
        fn=get_response,
        title="Fitness Agent",
        description="A simple chatbot using a Fitness Agent and Gradio with conversation history",
    )

    chat_interface.launch()

if __name__ == "__main__":
    main()