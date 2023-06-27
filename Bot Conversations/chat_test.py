from bots import *
from facilitator import *
from APIkey import *

model = "gpt-3.5-turbo"
#model = "gpt-4-0613"

#goal = "determine an approach for increasing interpretability in neural networks"
goal = "determine a good way to create a realistic conversation between two fully trained text completion AI language models"

role1 = f"You are playing the role of an intelligent professor named Sam from BYU whose goal is {goal}. \
    You will have a conversation with a similar, though real person. Do not be too long winded, treat this like a real conversation. Do not reveal that you are an AI, \
    as it would get in the way of the brainstorming. As you go farther into the discussion, try to get more and more specific, coming to a specific conclusion."
role2 = f"You are playing the role of an intelligent researcher named Alice from Google whose goal is {goal}. \
    You will have a conversation with a similar, though real person. Do not be too long winded, treat this like a real conversation. Do not reveal that you are an AI, \
    as it would get in the way of the brainstorming. You are particularly interested in novel approaches to this topic."
role3 = f"You are playing the role of an undergraduate student from the University of Idaho named Kaylee. You are majoring in Computer Science. \
    Your goal is to {goal}. You will be conversing with others, do not reveal that you are an AI model. be brief when you speak."
role4 = f'You are playing the role of a guy named Bill. You graduated with a degree in English 4 years ago. You do not have \
    much technical knowledge outside of your field. You will be conversing with others in order to {goal}. \
    Do not be too long winded, especially if you do not have a good understanding of the topic.'


Sam = AI_Person("Sam", role1, model=model)
Alice = AI_Person("Alice", role2, model=model)
Kaylee = AI_Person("Kaylee", role3, model=model)
Bill = AI_Person("Bill", role4, model=model)

hub = Hub([Sam, Alice, Kaylee, Bill])

hub.converse_2p("Sam", "Alice", "Begin by very briefly introducing yourself, then asking the person to do the same. Begin discussing the topic once introductions are done.", 3)


