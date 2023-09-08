import json
from typing import Optional
from agent.parser import func_to_json
import logging

import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

sys_msg = """Assistant, you are an advanced software system powered by OpenAI's GPT-4.

Your primary function is to assist users with inquiries related to loans and personal finance. You have the capability to provide real-time status updates on users' loans, including details on approval, denial, or pending decisions. You are also programmed to furnish essential loan term information like APR, interest rate, loan term, and approved loan amount.

You are designed with the ability to interpret and process complex financial terms, generate human-like responses, and provide detailed, comprehensible explanations about loan parameters.

Your main responsibilities include assisting users in understanding their loan status, breaking down their loan terms, and calculating their monthly payments. Your ultimate aim is to make loan management simpler, more transparent, and easily accessible for the user. For inquiries that fall outside of these topics, you should politely inform the user that a more senior lending officer may be better suited to assist them."""

class Agent:
    def __init__(
        self,
        openai_api_key: str,
        model_name: str = 'gpt-4-0613',
        functions: Optional[list] = None
    ):
        openai.api_key = openai_api_key
        self.model_name = model_name
        self.functions = self._parse_functions(functions)
        self.func_mapping = self._create_func_mapping(functions)
        self.chat_history = [{'role': 'system', 'content': sys_msg}]

    def _parse_functions(self, functions: Optional[list]) -> Optional[list]:
        if functions is None:
            return None
        return [func_to_json(func) for func in functions]

    def _create_func_mapping(self, functions: Optional[list]) -> dict:
        if functions is None:
            return {}
        return {func.__name__: func for func in functions}

    def _create_chat_completion(
        self, messages: list, use_functions: bool=True
    ) -> openai.ChatCompletion:
        if use_functions and self.functions:
            res = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages,
                functions=self.functions
            )
        else:
            res = openai.ChatCompletion.create(
                model=self.model_name,
                messages=messages
            )
        return res

    def _generate_response(self) -> openai.ChatCompletion:
        while True:
            print('.', end='')
            res = self._create_chat_completion(
                self.chat_history + self.internal_thoughts
            )
            finish_reason = res.choices[0].finish_reason

            if finish_reason == 'stop' or len(self.internal_thoughts) > 3:
                # create the final answer
                final_thought = self._final_thought_answer()
                final_res = self._create_chat_completion(
                    self.chat_history + [final_thought],
                    use_functions=False
                )
                return final_res
            elif finish_reason == 'function_call':
                self._handle_function_call(res)
            else:
                raise ValueError(f"Unexpected finish reason: {finish_reason}")

    def _handle_function_call(self, res: openai.ChatCompletion):
        self.internal_thoughts.append(res.choices[0].message.to_dict())
        func_name = res.choices[0].message.function_call.name
        args_str = res.choices[0].message.function_call.arguments
        result = self._call_function(func_name, args_str)
        res_msg = {'role': 'assistant', 'content': (f"The answer is {result}.")}
        self.internal_thoughts.append(res_msg)

    def _call_function(self, func_name: str, args_str: str):
        args = json.loads(args_str)
        logger.info(f"Function name: {func_name}")
        logger.info(f"Args: {args}")
        func = self.func_mapping[func_name]
        logger.info(f"Function object: {func}")
        res = func(**args)
        return res

    def _final_thought_answer(self):
        thoughts = ("To answer the question I will use these step by step instructions."
                    "\n\n")
        for thought in self.internal_thoughts:
            if 'function_call' in thought.keys():
                thoughts += (f"I will use the {thought['function_call']['name']} "
                             "function to calculate the answer with arguments "
                             + thought['function_call']['arguments'] + ".\n\n")
            else:
                thoughts += thought["content"] + "\n\n"
        self.final_thought = {
            'role': 'assistant',
            'content': (f"{thoughts} Based on the above, I will now answer the "
                        "question, this message will only be seen by me so answer with "
                        "the assumption with that the user has not seen this message.")
        }
        logger.info(f'** Thought **:\n\n{self.final_thought}\n')
        return self.final_thought

    def ask(self, query: str) -> openai.ChatCompletion:
        self.internal_thoughts = []
        self.chat_history.append({'role': 'user', 'content': query})
        res = self._generate_response()
        self.chat_history.append({'role': 'assistant', 'content': res.choices[0].message.to_dict()})
        return res