import openai

class AI_Person():
    def __init__(self, name, context_message, model="gpt-3.5-turbo"):
        self.name = name
        self.context_message = context_message
        self.model = model

        self.memory = {}
        self.long_term_memory = {} #summarizes perspectives and past information

    '''Generates a response to a conversation. Stores conversation in memory'''
    def generate_response(self, message, sender):
        #print(f'{sender}: {message}')
        if sender not in self.memory.keys():
            self.memory[sender] = [{"role": "system", "content": f"{self.context_message}"}]
        self.memory[sender].append({"role": "user", "content": f'{message}'})
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=self.memory[sender]
        )
        self.memory[sender].append({"role" : "system", "content": response["choices"][0]["message"]["content"]})
        return response["choices"][0]["message"]["content"]

    '''Converts all memories of a given conversation to long term memory'''
    def convo_to_longterm(self, name):
        if name not in self.memory.keys():
            print(f"There is no recent conversation with {name}")
            return None
        if name not in self.long_term_memory.keys():
            self.long_term_memory[name] = []

        temp_mem = [{"role" : "system", "content": f"Your purpose is to summarize the following conversation. When summarizing, pretend you are {self.name}."}]
        full = ''
        for mem in range(len(self.memory[name])):
            if self.memory[name][mem] == "system":
                full += f'Self ({self.name}): {self.memory[name][mem]["content"]}\n'
            else:
                full += f'{name}: {self.memory[name][mem]["content"]}\n'
        temp_mem.append({"role" : "user", "content": full})
        
        response = openai.ChatCompletion.create(
        model=self.model,
        messages=temp_mem
        )
        del self.memory[name]
        self.long_term_memory[name].append({"role" : "system", "content": f'This is a summary of a previous interaction with {name}. Take this into account, as if it were a memory of yours: [{response["choices"][0]["message"]["content"]}]\n'})
        return response["choices"][0]["message"]["content"]

    '''generates a general knowledge '''
    def generate_knowledge(self):
        print("TODO - implement")


    #Perhaps save conversations between individuals as objects. That way they do not each need to save there conversations