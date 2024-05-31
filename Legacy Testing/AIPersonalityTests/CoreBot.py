import openai
import json
import os
import pyttsx3

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


    # Assign an embedding as the key to all memories

class AI_Assistant():
    def __init__(self, core_context, personality_context, verbal=False, model_weak="gpt-3.5-turbo-16k-0613", model_strong="gpt-3.5-turbo-16k-0613"):
        self.core_context = core_context
        self.personality_context = personality_context
        self.model_weak = model_weak
        self.model_strong = model_strong
        self.begin_conversation()
        self.ltmemory = {}
        self.remembered_memories = []
        self.verbal = verbal
        if self.verbal:
            self.init_voice()

        #People -> 
            # Dictionary of {names: information}
            # if a name is mentioned, consider if any significant change in understanding has happened

    '''Generates a response to a conversation. Stores conversation in memory'''
    def generate_response(self, message):
        print("Generating response")
        print(f'Memory Length: {len(self.stmemory)}, LT length: {len(self.ltmemory.keys())}')
        self.stmemory.append({"role": "user", "content": f'{message}'})

        #If there are unremembered long term memories, look if any are relevant
        if len(self.remembered_memories) < len(self.ltmemory.keys()):
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

    #searches through all memories to determine which ones may be relevant
    def remember_ltmemories(self):
        unremembered_memories = []
        for label in self.ltmemory.keys():
            if label not in self.remembered_memories:
                unremembered_memories.append(label)
        if len(unremembered_memories) > 0:
            print("Searching memories")

        self.stmemory.append({"role": "system", "content": f"Here is a list of \"memory\" labels: {unremembered_memories}. If any of them seem relevant to the conversation at this point, call the \"recall_memory\" function on them. Otherwise, only respond very briefly."})
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
                            "description": "A label for the most relevant memory (Assuming any might be relevant)",
                        },
                    },
                },
            }]
        )

    def open_function_interface(self):
        print("In the function interface.")
        #Perhaps use a shorted input for this call? Just first and last?
        response = openai.ChatCompletion.create(
        model=self.model_strong,
        messages=self.stmemory,
        functions=[
            {
                "name": "write_memory",
                "description": "writes the current conversation into memory for the user to see later.",
                "parameters": {
                    "type": "object",
                    "properties": {
                    },
                },
            }]
        )

        return response["choices"][0]["message"]["content"]
        
    def inject_sys_message(self, message):
        print("Generating response to sys message")
        print(f'Memory Length: {len(self.stmemory)}, LT length: {len(self.ltmemory.keys())}')
        self.stmemory.append({"role": "system", "content": f'{message}'})

        #If there are unremembered long term memories, look if any are relevant
        if len(self.remembered_memories) < len(self.ltmemory.keys()):
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
        if label in self.ltmemory.keys():
            self.stmemory.append({"role": "system", "content": f"This is a memory you should keep in mind: label: {label} \n content \n {self.ltmemory[label]}. "})
        else:
            print("ERROR: Attempt to access nonexistant memory")
        self.stmemory.append(user_input)

    #removes all system messages from the end of short term memory. 
    def clean_short_term(self):
        while True:
            temp = self.stmemory.pop()
            if temp["role"] != "system":
                self.stmemory.append(temp)
                break

    #Converts the current contents of short term memory to a long term memory. 
    def finish_conversation(self):
        print("Ending conversation")
        self.stmemory.append({"role": "system", "content": "Write a 1 sentence \"memory\" title for this conversation. The title should accurately mention who is involved and the topic. Specifically mention names of those involved."})
        memory_label = openai.ChatCompletion.create(
        model=self.model_weak,
        messages=self.stmemory)
        self.stmemory.pop()

        self.stmemory.append({"role": "system", "content": "Write a 1 paragraph \"memory\" of this conversation. Include any key details, and make sure the summary accurately describes the main ideas of what happened."})
        memory_content = openai.ChatCompletion.create(
        model=self.model_weak,
        messages=self.stmemory)
        
        self.ltmemory[memory_label["choices"][0]["message"]["content"]] = memory_content["choices"][0]["message"]["content"]

    def speak(self, message):
        print("speaking")
        self.engine.say(message)
        self.engine.runAndWait()

    def init_voice(self):
        self.engine = pyttsx3.init(driverName='sapi5')

    #reads a memory from a json txt file
    def read_memory(self, label):
        with open(f"./Memories{label}.txt", "r") as file:
            data = file.read()
        self.ltmemory[label] = json.loads(data)


    #writes a memory to a json txt file
    def write_memory(self, label):
        os.makedirs("./Memories")
        with open(f"./Memories{label}.txt", "w") as file:
            file.write(json.dumps(self.stmemory[label]))

    def get_current_memory(self, label):
        return self.stmemory[label]
        



