import xml.etree.ElementTree as ET
from agent.agents import Agent  # or wherever Agent is located

class LoanAgent:
    def __init__(self, openai_api_key: str, xml_file_path: str):
        """Initialize the LoanAgent with API keys and read loan parameters from an XML file.

        :param openai_api_key: The OpenAI API key for GPT-4
        :param xml_file_path: Path to the XML file containing loan parameters
        """
        self.openai_api_key = openai_api_key
        self.xml_file_path = xml_file_path

        self.agent = Agent(
            openai_api_key=self.openai_api_key,
            functions=[
                self.read_loan_parameters_from_xml,
            ]
        )
        self.chat_history = self.agent.chat_history

    def read_loan_parameters_from_xml(self) -> dict:
        """Read loan parameters from an XML file and return them as a dictionary.

        This method parses an XML file to fetch
        loan status, rates, terms and monthly payments.

        Do not use this function if the inquiry from the user does not include any of these parameters.

        :param file_path: Path to the XML file containing loan parameters.
        :return: Dictionary containing loan parameters.
        """
        tree = ET.parse(self.xml_file_path)
        root = tree.getroot()

        parameters = {}

        stage_status = root.find('.//StageStatus')

        # Check if StageStatus element exists
        if stage_status is not None:
            stage = stage_status.find('Stage')
            status = stage_status.find('Status')
            
            if stage is not None:
                parameters['Stage'] = str(stage.text)
            else:
                parameters['Stage'] = None
                
            if status is not None:
                parameters['Status'] = str(status.text)
            else:
                parameters['Status'] = None
        else:
            print("StageStatus element not found.")

        # Parse Decision for rate, amount, term, and other loan terms
        decision = root.find('.//Decision')
        if decision is not None:
            rate = decision.find('Rate')
            amount = decision.find('Amount')
            term = decision.find('Term')
            other_data = decision.find('OtherData')

            if rate is not None:
                parameters['Rate'] = float(rate.text)
            else:
                parameters['Rate'] = None

            if amount is not None:
                parameters['Amount'] = float(amount.text)
            else:
                parameters['Amount'] = None

            if term is not None:
                parameters['Term'] = int(term.text)
            else:
                parameters['Term'] = None

            if other_data is not None:
                estimated_payment = other_data.find('EstimatedPayment')
                if estimated_payment is not None:
                    parameters['EstimatedPayment'] = float(estimated_payment.text)
                else:
                    parameters['EstimatedPayment'] = None

        return parameters

    def ask(self, question: str):
        response = self.agent.ask(question)
        return response
    
    def ask_performance(self, question: str):
        response = self.agent.ask_performance(question)
        return response

    def view_functions(self):
        return self.agent.functions

    def view_chat_history(self):
        return self.agent.chat_history