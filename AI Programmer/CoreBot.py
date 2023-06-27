import openai
import json


class AI_Programmer():
    def __init__(self, design_goal, model="gpt-3.5-turbo-0613"):
        self.design_goal = design_goal
        self.model = model
        self.memory = {}

    '''Generates a response to a conversation. Stores conversation in memory'''
    def generate_response(self, label, message):
        if label not in self.memory.keys():
            self.memory[label] = [{"role": "system", "content": f"{self.design_goal}"}]
        self.memory[label].append({"role": "user", "content": f'{message}'})
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=self.memory[label]
        )
        self.memory[label].append({"role" : "system", "content": response["choices"][0]["message"]["content"]})
        return response["choices"][0]["message"]["content"]
    

    def write_memory(self, label):
        with open(f"{label}.txt", "w") as file:
            file.write(json.dumps(self.memory[label]))


    def recall_memory(self, label):
        with open(f"{label}.txt", "r") as file:
            data = file.read()
        self.memory[label] = json.loads(data)
