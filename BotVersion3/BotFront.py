"""This is the face of the bot, where input is accepted, the LLM is called, and output is accessed."""

from BotMemory import *
from APIfunctions import *
from LLMHolder import LLM_Holder
import json

'''THIS VERSION OF THE BOT GENERATES QUERIES BEFORE RESPONDING TO ANYTHING. IF THERE IS ONE OR MORE QUERY, THEN 
THEY ARE USED AS A BASIS FOR NEURAL SEARCH IN MY DATABASE, MUCH LIKE HOW A GOOGLE SEARCH MIGHT WORK. I AM 
STILL WORKING OUT HOW TO DETERMINE WHAT SHOULD BE INJECTED INTO THE MODELS ST MEMORY. PERHAPS, I SHOULD ONLY
STORE INDIVIDUAL SENTENCES IN THE MODEL.'''

class Bot:
    def __init__(self, name, init_message, model_weak="gpt-3.5-turbo-16k-0613", model_strong="gpt-4-1106-preview"):
        self.name = name
        self.init_message = init_message
        self.seen_memories = []
        self.st_memory = []
        self.lt_memory = LTMemory_System()
        self.model_weak = LLM_Holder(model_weak)
        self.model_strong = LLM_Holder(model_strong)

        self.inject_message(init_message, "system")

    def wipe_st(self):
        self.st_memory = []
        self.seen_memories = []
        self.inject_message(self.init_message, "system")

    #Generates a response. Injects input message and generate response into st memory
    def respond_to_input(self, message, role="user"):
        
        #TODO - check if there are any queries that should be generated

        #TODO - If there are queries, check if there are answers in the database

        self.inject_message(message, role) #add message to st memory
        response = self.generate_response()
        self.inject_message(response, "assistant") #remember what it said
        return response
        
    #Respond to current short term memory
    def generate_response(self):
        return self.model_strong.generate_response(self.st_memory)["choices"][0]["message"]["content"]

    #injects a message directly into the bots short term memory without prompting a response
    def inject_message(self, message, role="system"):
        formatted = {"role": f'{role}', "content": f'{message}'}
        self.st_memory.append(formatted)

    #Compacts st memory into summary, then adds it to lt memory. Optionally wipes st memory
    def to_lt_memory(self, clear_st=True):
        print("Sending ST to LT")
        if len(self.st_memory) > 1:
            summary = self.respond_to_input("Write a short paragraph summary of this entire conversation, focusing on key details you would like to remember for later.", "system")
            self.lt_memory.add_memory(summary)
            if clear_st:
                self.wipe_st()   
    
    def generate_queries(self):
        self.st_memory.append({"role" : "system", "content" : f"If there are any facts that you need to search your \
                               memory for, use recall. Otherwise, respond with NO"})
                
        #Call api. If relevance is found, it calls the recall function, otherwise it simply says no
        response = self.model_strong.generate_response(self.st_memory, tools=[RECALL])

        queries = []

        for query in queries:
            summaries, embeddings = self.lt_memory.embedding_search(queries)

    #determines if a memory is relevant. If it is, it brings in relevant details
    def check_memory_relevance(self, query, fact):
        print(f"checking memory relevance for: {fact}")
        relevance_message = []
        relevance_message.append({"role" : "user", "content" : f"Fact: {fact} \n Query: {query} \n \
                                  If the fact is relevant to the query, use the recall function. Otherwise, respond with NO."})
                
        #Call api. If relevance is found, it calls the recall function, otherwise it simply says no
        response = self.model_strong.generate_response(self.st_memory, tools=[RECALL])
        print(f"MEMORY RESPONSE: {response}")


    #Fetches a string summary from lt memory based on the input embedding. Records that memory is recalled in current sentence
    def recall(self, fact):
        print("relevance found - recalling memory")
        #TODO - recall the fact, save that it has been recalled. 

        #self.inject_message(f'This is a memory: [{memory}]', "system")

    #Used for testing basic recall about people
    def implant_memories(self):
        print("implanting memories...")
        memory = "Sam is a student from BYU that is studying information science."
        self.lt_memory.add_memory(memory)
        memory = "Edward is a guy from South Dakota. He enjoys rock climbing and eating hamburgers. He claims to have found the best burger joint in the United States."
        self.lt_memory.add_memory(memory)
        memory = "Last time a guy started a conversation with \"Hello there\" he ended up being a huge troll."
        self.lt_memory.add_memory(memory)
        memory = "My ex-girlfriend occasionally is on these forums, her username is \"SimpSlayer\"."
        self.lt_memory.add_memory(memory)
        print("memory implant finished.")

    #Implant memories directly into lt memory 
    def implant_memory(self, memory):
        print("implanting memory...")
        self.lt_memory.add_memory(memory)
        print("memory implanted")


        

