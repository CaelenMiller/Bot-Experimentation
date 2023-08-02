from CoreBot import AI_Programmer
from APIkey import *
from BotIDE import *

#Full iterative development
def iterative_development(core_context, label, max_itr=5):
    #initialize AI and prompt
    AI = AI_Programmer(core_context=core_context)
    AI.generate_response(label, "Write a simple text based adventure game. Include code for items (and using them). Run a few tests on the code. If you think it works well, then ask the user for more input. Use the function calls")


    #Perform loop
    for i in range(max_itr):
        AI.generate_response(label, "")
    AI.write_memory(label=label)

core_context = "Your purpose is to write python code for me. Use the provided functions to write the code, get additional user input, or declare that you are done. Focus on using the functions provided to interact with the user. Code will only be used if it is written into a function call. Initially it is ok to just stub out code, but do not allow infinite loops."

iterative_development(core_context, label="test1")



#Initializing message
#At each iteration, show the AI 1) the current code, and 2) the output of the code. 
