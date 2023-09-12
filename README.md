# Loan Management Chatbot

This project is a chatbot that assists users in managing their loans. It provides information about loan status, rate, terms, and monthly payments. The chatbot is built using OpenAI's GPT-4 model and Gradio for the user interface.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [To-Do] (#todo)

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/solanovisitor/loan_agent.git
    ```
2. Install the required packages:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Set your OpenAI API key in the `.env.list` file:
    ```
    OPENAI_API_KEY=your_openai_api_key
    ```
2. Run the chatbot:
    ```
    python run_chatbot.py
    ```

## Testing

1. Run the performance pipeline:
    ```
    python performance.py
    ```
2. Classification metrics will be calculated and printed in your terminal.
3. The raw results will be saved in `./tests/final_results.csv`.

## Files

- `chatbot.py`: The main script that runs the chatbot.
- `agents.py`: Contains the `Agent` class that interacts with the OpenAI API.
- `loan_agent.py`: Contains the `LoanAgent` class that reads loan parameters from an XML file and interacts with the `Agent` class.
- `run_chatbot.py`: Script to run the chatbot with hot-reloading enabled.
- `performance.py`: Script to test the performance of the chatbot.

## To-Do

| Task | Description | Status |
| --- | --- | --- |
| Prompt improvements to user-faced Gradio application | Improve the user interface and experience of the Gradio application. | Pending |
| Integrate the function to a database | Instead of relying solely on XML inputs, integrate the function with a database to fetch user data. | Pending |
| Add more functions | Add functions to calculate different parameters related to loans. | Pending |
| Implement Vectorstore | Use Vectorstore to align the chatbot's responses with the company's guidelines. | Pending |
| Improve performance pipeline | Make the performance pipeline calls run in parallel to improve speed. | Pending |
| Improve error handling | Implement better error handling and logging throughout the application. | Pending |
| Add user authentication | Implement user authentication to ensure data security and privacy. | Pending |
| Implement multi-language support | Add support for multiple languages to make the chatbot more accessible. | Pending |
| Add more tests | Write more comprehensive tests for the chatbot to ensure its reliability and accuracy. | Pending |
| Improve documentation | Update and improve the project's documentation, including the README and code comments. | Pending |