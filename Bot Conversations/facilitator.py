from bots import *
'''HUBS: a group conversation for bots'''

PROMPT1 = "Your purpose is to simulate a conversation from the perspective of several people. \
            A user will input the first part of the conversation. You will finish it. \
            The topic of the conversation will be: "
            
PROMPT2 = " A bio for each person will be provided, with each bio being in the first person \
            (as if it were directions), being contained in square brackets []. The bios are as follows:"

class Hub():
    def __init__(self, bots, model="gpt-3.5-turbo"):
        
        self.bots = {bot.name : bot for bot in bots}
        self.model = model
        self.convos = []

    def converse_multi(self, names, topic):
        prompt = PROMPT1 + topic + PROMPT2

        #Add in bio's
        for name in names:
            prompt += f'BIO FOR {name}: [{self.bots[name].context_message}]\n\n'
        
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt
        )
        self.convos.append({"role" : "system", "content": response["choices"][0]["message"]["content"]})
        return response["choices"][0]["message"]["content"]

    def converse_2p(self, name_1, name_2, initial_prompt, max_itr, to_longterm=True):
        person1 = self.bots[name_1]
        person2 = self.bots[name_2]
        r2 = person2.generate_response(initial_prompt, "general")
        iteration = 0
        while iteration < max_itr:
            iteration += 1
            print(f'Beginning iteration {iteration}')
            r1 = person1.generate_response(r2, person2.name)
            print(r1)
            r2 = person2.generate_response(r1, person1.name)
            print(r2)

        if to_longterm:
            person1.convo_to_longterm(person2.name)
            print(person1.long_term_memory)
            person2.convo_to_longterm(person1.name)
            print(person2.long_term_memory)

    def summarize_conversation(self, name):
        #TODO - summarize the conversation from the perspective of of bot with name
        pass

    def add_bot(self, bot):
        self.bots[bot.name] = bot