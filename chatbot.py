import os
import logging
import gradio as gr
from loan_agent import LoanAgent
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# load environment variables from .env.list
load_dotenv('.env.list')

openai_api_key = os.getenv('OPENAI_API_KEY')

def handle_upload(file):
    global loan_agent
    global history
    if file is not None:
        loan_agent = LoanAgent(openai_api_key, file.name)
        history = loan_agent.chat_history
    else:
        logger.error('No file was uploaded.')

def get_response(message, history, file_upload):
    handle_upload(file_upload)
    logger.info(f'Chat history: {history}')

    res = loan_agent.ask(message)

    chat_response = res['choices'][0]['message']['content']

    return chat_response

def main():

    with gr.Blocks() as chat:
        file_upload = gr.File(file_types=['.xml'])
        gr.ChatInterface(
            fn=get_response,
            additional_inputs=file_upload,
        )

    chat.queue().launch()

if __name__ == "__main__":
    main()