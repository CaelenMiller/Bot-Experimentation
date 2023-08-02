import openai
import json
import os
import pyttsx3
import Memory_Tools

'''Here is the overall flow of the AI assitant in the current iteration.
    * Assistants short term memory is initialized using its core context message
        * Input is accepted from the user. 
        * The assistant searches long term memory for relevant memories
        * If relevant memories are found, they are recorded as remembered for this conversation and added as a 
        system message in the conversation
        * When summarizing a conversation, references to specific people are found and recorded. Individuals
        who do not have a profile yet have one created, otherwise their profile is restructured
    * Once a conversation is finished, it is placed in long term memory.'''

#Development ideas
    # Keep profiles of individuals. Update these as they interact more with others. Have a list of key characteristics. 
    # Periodically summarize and combine things in long term memory
    # Have an additional context that can be indirectly modified by users through interactions with them
    # Split core context into two parts - the universal context and the personality context
    # Use a graph structure to store ideas. 
    # Have tags attached to each memory. AI is allowed to generate additional tags. Tags are only the most important
        # aspects of a memory, such as names and key concepts. 
    # Perhaps use sentence embeddings to determine connections

class AI_Assistant():
    def __init__(self, core_context, personality_context, verbal=False, model_weak="gpt-3.5-turbo-16k-0613", model_strong="gpt-3.5-turbo-16k-0613"):
        self.core_context = core_context
        self.personality_context = personality_context
        self.model_weak = model_weak
        self.model_strong = model_strong
        self.ltmemory_graph = Memory_Tools.Memory_Graph()
        self.begin_conversation()
        self.remembered_memories = []
        self.verbal = verbal
        if self.verbal:
            self.init_voice()

    '''Generates a response to a conversation. Stores conversation in memory'''
    def generate_response(self, message):
        print('Generating response - Memory Length: {len(self.stmemory)}, LT length: {self.ltmemory_graph.size}')
        self.stmemory.append({"role": "user", "content": f'{message}'})
        #If there are unremembered long term memories, look if any are relevant
        if len(self.remembered_memories) > 0:
            self.remember_ltmemories()

        response = openai.ChatCompletion.create(
        model=self.model_strong,
        messages=self.stmemory)
        
        self.stmemory.append({"role" : "assistant", "content": response["choices"][0]["message"]["content"]})

        if self.verbal:
            self.speak(response["choices"][0]["message"]["content"])

        return response["choices"][0]["message"]["content"]

    #clears short term memory 
    def begin_conversation(self):
        print("initializing memory")
        self.stmemory = []
        self.stmemory.append({"role": "system", "content": f'{self.core_context}'})
        self.stmemory.append({"role": "system", "content": f'{self.personality_context}'})
        self.remembered_memories = []

        #self.ltmemory_graph.add_node

    #searches through all memories to determine which ones may be relevant
    def remember_ltmemories(self):
        similarities = self.ltmemory_graph.process_input(self.stmemory[-1]["content"])
        unremembered_memories = self.ltmemory_graph.process_similarities(similarities)
            
        if len(unremembered_memories) > 0:
            print("Searching memories")

            self.stmemory.append({"role": "system", "content": f"Here is a list of \"memory\" or concept names in your database: {unremembered_memories}. If any of them seem relevant to the conversation at this point, call the \"recall_memory\" function on them to access their contents. Otherwise, only respond very briefly."})
            remember_output = openai.ChatCompletion.create(
            model=self.model_weak,
            messages=self.stmemory,
            functions=[
                {
                    "name": "recall_memories",
                    "description": "Recall memories that are or could be relevant to the current conversation.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "label": {
                                "type": "string",
                                "description": "A label for the most relevant memory",
                            },
                        },
                    },
                }]
            )
        
    #Injects a system message onto the end of the conversation and prompts a response
    def inject_sys_message(self, message):
        print("Generating response to sys message")
        print(f'Memory Length: {len(self.stmemory)}')
        self.stmemory.append({"role": "system", "content": f'{message}'})

        #If there are unremembered long term memories, look if any are relevant
        if self.ltmemory_graph.size > 5:
            self.remember_ltmemories()

        response = openai.ChatCompletion.create(
        model=self.model_strong,
        messages=self.stmemory)
        
        self.stmemory.append({"role" : "assistant", "content": response["choices"][0]["message"]["content"]})

        if self.verbal:
            self.speak(response["choices"][0]["message"]["content"])

        return response["choices"][0]["message"]["content"]

    #Takes a list of memory labels in, adds the associated memories to the current conversation
    def recall_memories(self, label):
        self.stmemory.pop() # if we got here, there is an extra system memory in place. 
        user_input = self.stmemory.pop() # puts the memories behind the user input
        print(f'Recalling: {label}')
        node = self.ltmemory_graph.get_node(label)

        if node:
            self.ltmemory_graph.access_node(label)
            self.stmemory.append({"role": "system", "content": f"This is a memory you should keep in mind: label: {label} \n content \n {node.content}. "})
        else:
            print("ERROR: Attempt to access nonexistant memory")
        self.stmemory.append(user_input)

    #Converts the current contents of short term memory to a long term memory. 
    def finish_conversation(self):
        print("Ending conversation")

        #Have LLM summarize conversation
        #Perform NER to extract key entities from the summary of the conversation
        #Decide which entities are important
            #Term frequency
            #Embeddings? Words vs paragraph comparison
            #
        #Make summaries for each important entity using the full conversation




        #TODO - For initial testing, do not allow for creation of new memory tags. Only accessing

        # similarities = self.ltmemory_graph.process_input(self.stmemory[-1]["content"])
        # related_memories = self.ltmemory_graph.process_similarities(similarities)
            
        
        # temp = []
        # temp.append({"role": "system", "content": f"Which of these best matches this memory? {related_memories}"})
        # closest = openai.ChatCompletion.create(
        # model=self.model_weak,
        # messages=self.stmemory)

        # self.ltmemory_graph.add_node(memory_label, memory_content["choices"][0]["message"]["content"])


    def speak(self, message):
        print("speaking")
        self.engine.say(message)
        self.engine.runAndWait()

    def init_voice(self):
        self.engine = pyttsx3.init(driverName='sapi5')

    def get_current_memory(self, label):
        return self.stmemory[label]
        



