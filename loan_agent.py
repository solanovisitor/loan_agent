import xml.etree.ElementTree as ET
from agent.agents import Agent  # or wherever Agent is located

class LoanAgent:
    def __init__(self, openai_api_key: str, xml_file_path: str):
        self.openai_api_key = openai_api_key
        self.xml_file_path = xml_file_path
        self.parameters = self.read_loan_parameters_from_xml(self.xml_file_path)

        self.agent = Agent(
            openai_api_key=self.openai_api_key,
            functions=[
                self.calculate_monthly_payment,
                self.get_loan_status  # Added new function here
            ]
        )

    def read_loan_parameters_from_xml(self, file_path: str) -> dict:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        parameters = {}
        loan_info = root.find('loan')
        parameters['status'] = loan_info.find('status').text
        parameters['APR'] = float(loan_info.find('APR').text)
        parameters['rate'] = float(loan_info.find('rate').text)
        parameters['term'] = int(loan_info.find('term').text)
        parameters['amount_approved'] = float(loan_info.find('amount_approved').text)

        return parameters

    def calculate_monthly_payment(self) -> float:
        principal = self.parameters['amount_approved']
        rate = self.parameters['rate']
        term = self.parameters['term']

        monthly_rate = rate / 12 / 100
        monthly_payment = (principal * monthly_rate) / (1 - (1 + monthly_rate)**(-term))
        return monthly_payment

    def get_loan_status(self) -> dict:
        return self.parameters

    def ask(self, question: str):
        response = self.agent.ask(question)
        return response