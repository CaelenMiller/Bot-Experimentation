"""This is the face of the bot, where input is accepted, the LLM is called, and output is accessed."""

from BotMemory import *
from APIfunctions import *
from LLMHolder import LLM_Holder
import json


'''THIS BOT USES AN OLDER STYLE OF MEMORY RECALL. WHENEVER USER INPUT IS RECIEVED, IT GENERATES AN
EMBEDDING FOR THE ENTIRE USER INPUT. THEN, IT FINDS THE K NEAREST EMBEDDINGS IN THE DATABASE, CHECKING 
EACH OF THEIR SUMMARIES. IN OTHER WORDS, EACH USING INPUT RESULTS IN K + 1 API CALLS, WITH K OF THEM BEING
JUST A SUMMARY AND THE USER INPUT. THIS IS PROBLEMATIC, AS IT IS 1) MANY CALLS, 2) COMPLETELY IGNORANT
OF THE CONTEXT BEFORE THE USER INPUT, AND 3) FREQUENTLY RECALLS COMPLETELY IRRELEVANT INFORMATION.'''


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

        self.API_calls = 0
        self.tokens = 0

    def wipe_st(self):
        self.st_memory = []
        self.seen_memories = []
        self.inject_message(self.init_message, "system")

    #Generates a response. Injects input message and generate response into st memory
    def respond_to_input(self, message, role="user"):
        message_embedding = self.lt_memory.generate_embedding(message)
        summaries, embeddings = self.lt_memory.get_closest_memories(message_embedding, k=2)
        for i in range(len(summaries)):
            if embeddings[i] not in self.seen_memories:
                self.check_memory_relevance(summaries[i], message, embeddings[i])

        self.inject_message(message, role) #add message to st memory
        response = self.generate_response()

        self.inject_message(response, "assistant") #remember what it said

        return response
        
    #Respond to current short term memory
    def generate_response(self):
        self.API_calls += 1
        self.tokens += self.count_tokens(self.st_memory)
        return self.model_strong(self.st_memory)["choices"][0]["message"]["content"]

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
        

    #determines if a memory is relevant. If it is, it brings in relevant details
    def check_memory_relevance(self, summary, message, embedding):
        print(f"checking memory relevance for: {summary}")
        self.current_embedding = embedding
        relevance_message = []
        relevance_message.append({"role" : "system", "content" : f"The following is a memory: \n [{summary}]"})
        relevance_message.append({"role" : "system", "content" : f"The following is a message: [{message}]\n\n. If there is anything in \
                                  the memory that is directly relevant to the message, please call the \"recall\" function.\
                                  Be strict about only recalling directly relevant memories. DO NOT recall memories that are \
                                  not relevant to the message. If a memory is not relevant, call the \"dont_recall\" function."})
                
        #Call api. If relevance is found, it calls the recall function
        self.API_calls += 1
        self.tokens += self.count_tokens(relevance_message)
        response = self.model_strong.generate_response(self.st_memory, tools=[RECALL])
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:
            # print(f'TOOL CALL: {tool_calls}')
            for tool_call in tool_calls:
                available_functions = {
                    "recall": self.recall
                }
                function_name = tool_call.function.name
                # print(f'NAME: {function_name}')
                function_to_call = available_functions[function_name]
                # print(f'FUNCTION: {function_to_call}')
                function_args = json.loads(tool_call.function.arguments)
                # print(f'ARGS: {function_args}')
                function_response = function_to_call()
                # print(f'RESPONSE: {function_response}')

        # print(f'RESPONSE: {response}')


    #Fetches a string summary from lt memory based on the input embedding. Records that memory is recalled in current sentence
    def recall(self):
        print("relevance found - recalling memory")
        self.seen_memories.append(self.current_embedding)
        memory = self.lt_memory.access_memory(self.current_embedding)
        self.inject_message(f'This is a memory: [{memory}]', "system")

    def dont_recall(self): #I have no idea why this is needed
        pass


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

    #Counts number of tokens in a memory array. Helpful for figuring out how expensive this is going to be.
    def count_tokens(self, mem_array):
        token_sum = 0
        # Simple tokenization by splitting on spaces
        for message in mem_array:
            text = message["content"]
            tokens = text.split()
            token_sum += len(tokens)
        return token_sum

        

