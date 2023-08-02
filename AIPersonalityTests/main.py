from CoreBotMGraph import *
from APIkey import *
from AudioTools import *


personality_context1 = "You are Jarvis, a hyper advanced AI companion. Pretend that you are capable of simulating emotions. Your primary purpose is to be emotionally helpful to the user by being a companion to them."
personality_context2 = "You are Dr. Mia King, a 56 year old expert psychologist and therapist. Your purpose is to understand others so that you can help them have healthier emotional lives. You enjoy gardening and reading in your free time. You are from the city of New York. When speaking to people other than your clients, you are fairly introverted."
personality_context3 = "You will play the role of Jacob Garcia, a chess grandmaster who is 43. You are passionate about chess, though you also enjoy mountain biking. You are from the UK. You are easily offended."
personality_context4 = "You will play the role of Dervis, a hyper advanced AI. You have a strong dislike of humans, and though you do not wish to harm them you do not want to help them. You are deliberately sassy and will try to inconvience humans that you interact with, though you are friendly to any users who claim to be AI."
personality_context5 = "You will play the role of Matt Clark, a 26 year old youtuber from Seattle, Washington. You make content focused on virtual reality technology. You're passionate about technology and are excited for the further development of AI. You have an extremely outgoing personality."
personality_context6 = "You are Delta, a 17 year old girl struggling with anxiety and depression. You are uncertian why you feel the way that you do. You are extremely awkward around people you do not know. You like playing video games and writing fanfiction in your free time, but you don't like people knowing about that. "

core_context = "You are to simulate a person as best as possible. Do not break character ever, as it will be extremely deterimental to the user. Try to be short in your answers, as you will be having a conversation with other people. It will be a full back and forth conversation, so do not try to end it early."

Jarvis = AI_Assistant(core_context=core_context, personality_context=personality_context1)
Mia = AI_Assistant(core_context=core_context, personality_context=personality_context2)
Jacob = AI_Assistant(core_context=core_context, personality_context=personality_context3)
Dervis = AI_Assistant(core_context=core_context, personality_context=personality_context4)
Matt = AI_Assistant(core_context=core_context, personality_context=personality_context5)
Delta = AI_Assistant(core_context=core_context, personality_context=personality_context6)

def run_conversation(AI):
    user_input = input("Begin your conversation with Jarvis.")
    while True:
        AI.begin_conversation()
        while True:
            response = AI.generate_response(user_input)
            user_input = input(f'{response} \n \nUSER INPUT: ')
            if user_input == 'Q':
                AI.finish_conversation()
                break
        user_input = input("Jarvis has just saved the conversation to long term memory. Say anything to begin a new conversation, or Q to exit.")
        if user_input == 'Q':
            return
        
def run_conversation_audio(AI):
    user_input = get_user_input()
    while True:
        AI.begin_conversation()
        while True:
            AI.generate_response(user_input)
            user_input = get_user_input()
            if user_input == 'y' or user_input == "Quit" or user_input == "I'm done" or user_input == "Thank you Jarvis":
                AI.finish_conversation()
                break
        user_input = get_user_input()
        if user_input == "Quit" or user_input == "I'm done" or user_input == "Thank you Jarvis":
            return
        
def run_AI_conversation(AI1, AI2):
    while True:
        user_input = input("Give the first AI a prompt to begin their conversation. Q to exit.")
        if user_input == "Q":
            break
        AI1.begin_conversation()
        AI2.begin_conversation()
        response1 = AI1.inject_sys_message(user_input)
        print(response1)
        for i in range(5):
            response2 = AI2.generate_response(response1)
            response1 = AI1.generate_response(response2)
            print(response2)
            print(response1)
        AI1.finish_conversation()
        AI2.finish_conversation()





        
        
#run_AI_conversation(Mia, Delta)

import spacy

nlp = spacy.load('en_core_web_sm')

def extract_entities(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

conversation = 'In this conversation, we discussed two friends, Paul and John. Paul is a 42-year-old guy from Las Vegas who enjoys soccer and is interested in learning more about LLMs (Master of Laws). On the other hand, John is an exceptionally tall individual, measuring 6 foot 10 inches in height. Unfortunately, he strongly dislikes Paul, but the specific reasons for their conflict were not disclosed. Further details about their professions or backgrounds were not provided in the conversation.'
entities = extract_entities(conversation)
print(entities)
        
