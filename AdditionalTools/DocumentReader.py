import openai
from APIkey import *

class Bot:
    def __init__(self, init_message=None, model_weak="gpt-3.5-turbo-16k-0613", model_strong="gpt-4-1106-preview"):
        self.init_message = init_message
        self.st_memory = []
        self.model_weak = model_weak
        self.model_strong = model_strong
        if self.init_message is not None:
            self.inject_message(init_message, "system")

    def wipe_st(self):
        self.st_memory = []
        if self.init_message is not None:
            self.inject_message(self.init_message, "system")

    #Generates a response. Injects input message and generate response into st memory
    def respond_to_input(self, message, role="user", store=False):
        self.inject_message(message, role) #add message to st memory
        response = self.generate_response()
        if store:
            self.inject_message(response, "assistant") #remember what it said
        else:
            self.st_memory = self.st_memory[:-1]
        return response
        
    #Respond to current short term memory
    def generate_response(self):
        response = openai.ChatCompletion.create(
        model=self.model_strong,
        messages=self.st_memory)
        return response["choices"][0]["message"]["content"]

    #injects a message directly into the bots short term memory without prompting a response
    def inject_message(self, message, role="system"):
        formatted = {"role": f'{role}', "content": f'{message}'}
        self.st_memory.append(formatted)

if True: #Beware, this is expensive to run. 
    doc_reader = Bot()
    doc_reader.inject_message("You are a document reading AI that specializes on a specific text. You will consume an entire text, then answer questions (or perform specific functions on the text) according to user input.", "system")
    with open('./Data/Ants.txt', 'r', encoding='utf-8') as file:
        file_content = file.read()
    print(f'Injecting file of char length {len(file_content)}')
    doc_reader.inject_message(file_content, "system")

    user_input = input("Write your input: ")
    while user_input != "quit":
        print(doc_reader.respond_to_input(user_input))
        user_input = input("Write your input [type 'quit' when finished]: ")
    
    
