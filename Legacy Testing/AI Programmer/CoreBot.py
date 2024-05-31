import openai
import json
from BotIDE import get_user_input, write_code, finish_programming


class AI_Programmer():
    def __init__(self, core_context, model="gpt-3.5-turbo-16k-0613"):
        self.core_context = core_context
        self.model = model
        self.memory = {} #Allows the bot to see the entire conversation so far

    '''Generates a response to a conversation. Stores conversation in memory'''
    def generate_response(self, label, message, functions=[]):
        print("Generating response")
        if label not in self.memory.keys():
            self.memory[label] = [{"role": "system", "content": f"{self.core_context}"}]
        self.memory[label].append({"role": "user", "content": f'{message}'})
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=self.memory[label],
        functions=[
            {
                "name": "get_user_input",
                "description": "Request for user input.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "Message from the AI about what is needed",
                        },
                    },
                },
            },
            {
                "name": "write_code",
                "description": "Write code to a file to execute. Use this instead of giving the code to the user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "code": {
                            "type": "string",
                            "description": "The new contents of the python3 file that will be written and executed.",
                        },
                    },
                },
            },
            {
                "name": "finish_programming",
                "description": "Run this to declare that the code is tested and ready to use, and that no more input will be needed from the user.",
                "parameters": {
                    "type": "object",
                    "properties": {    },
                },
            }
        ],
        function_call="auto"
        )
        self.memory[label].append({"role" : "assistant", "content": response["choices"][0]["message"]["content"]})

        response = self.handle_functions(response["choices"][0]["message"], label)

        #return response["choices"][0]["message"]["content"]
    
    def handle_functions(self, response, label):
        if response.get("function_call"):
            print(f'Calling {response["function_call"]["name"]}')
            # Step 3: call the function
            # Note: the JSON response may not always be valid; be sure to handle errors
            available_functions = {
                "get_user_input": get_user_input,
                "write_code" : write_code,
                "finish_programming" : finish_programming
            }  # only one function in this example, but you can have multiple
            function_name = response["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response["function_call"]["arguments"])

            if function_name == "get_user_input":
                function_response = function_to_call(
                    message=function_args.get("message")
                )
            elif function_name == "write_code":
                function_response = function_to_call(
                    code=function_args.get("code")
                )
            elif function_name == "write_code":
                function_response = function_to_call()

            # Step 4: send the info on the function call and function response to GPT
            self.memory[label].append(
                {
                    "role": "function",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
            second_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=self.memory[label],
            )  # get a new response from GPT where it can see the function response
            self.memory[label].append(second_response)
        else:
            print(f'{response}'[:100])



    def write_memory(self, label):
        with open(f"{label}.txt", "w") as file:
            file.write(json.dumps(self.memory[label]))


    def recall_memory(self, label):
        with open(f"{label}.txt", "r") as file:
            data = file.read()
        self.memory[label] = json.loads(data)

    def get_current_memory(self, label):
        return self.memory[label]
        
