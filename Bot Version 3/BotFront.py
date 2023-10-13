"""This is the face of the bot, where input is accepted, the LLM is called, and output is accessed."""

from BotMemory import *
from APIfunctions import *
import openai

class Bot:
    def __init__(self, name, init_message, model_weak="gpt-3.5-turbo-16k-0613", model_strong="gpt-3.5-turbo-16k-0613"):
        self.name = name
        self.init_message = init_message
        self.seen_memories = []
        self.st_memory = []
        self.lt_memory = LTMemory_System()
        self.model_weak = model_weak
        self.model_strong = model_strong

        self.inject_message(init_message, "system")

    def wipe_st(self):
        self.st_memory = []
        self.seen_memories = []
        self.inject_message(self.init_message, "system")

    #Generates a response. Injects input message and generate response into st memory
    def respond_to_input(self, message, role="user"):
        message_embedding = self.lt_memory.generate_embedding(message)
        summaries, embeddings = self.lt_memory.get_closest_memories(message_embedding)
        for i in range(len(summaries)):
            if embeddings[i] not in self.seen_memories:
                self.check_memory_relevance(summaries[i], message, embeddings)

        self.inject_message(message, role) #add message to st memory
        response = self.generate_response()

        self.inject_message(response, "assistant") #remember what it said

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

    #Compacts st memory into summary, then adds it to lt memory. Optionally wipes st memory
    def to_lt_memory(self, clear_st=True):
        summary = self.respond_to_input("Write a short paragraph summary of this entire conversation, focusing on key details you would like to remember for later.", "system")
        self.lt_memory.add_memory(summary)
        if clear_st:
            self.wipe_st()

    #Fetches a string summary from lt memory based on the input embedding
    def recall(self):
        print("recalling memory")
        self.seen_memories.append(self.current_embedding)
        return self.lt_memory.access_memory(self.current_embedding)
    
    #determines if a memory is relevant. If it is, it brings in relevant details
    def check_memory_relevance(self, summary, message, embedding):
        print("checking memory relevance")
        self.current_embedding = embedding
        relevance_message = []
        relevance_message.append({"role" : "system", "content" : f"The following is a summary: \n {summary}"})
        relevance_message.append({"role" : "system", "content" : f"The following is a message {message}. If there is anything in \
                                  message that out be relevant to the summary, please call the \"recall\" function.\
                                  Otherwise, simply reply with \"no\"."})
        
        #Call api. If relevance is found, it calls the recall function
        output = openai.ChatCompletion.create(
        model=self.model_weak,
        messages=relevance_message,
        functions=[recall_function]
        )
        #print(output)
        #print(relevance_message)