from BotMemory import *
from BotFront import *
from APIkey import *

def lt_basic_tests():
    ltMem = LTMemory_System()

    temp1 = "Hello, my name is Caelen Miller. I enjoy reading books"
    temp2 = "Hello, my name is Billy Bob. I enjoy digging holes"
    temp3 = "Once upon a time there was a strange hill known as hangmans hill. Once upon a time there was a strange hill known as hangmans hill. Once upon a time there was a strange hill known as hangmans hill. Once upon a time there was a strange hill known as hangmans hill. Once upon a time there was a strange hill known as hangmans hill."
    temp4 = "Do you know about a guy named Billy Bob? I've heard he enjoys digging holes."

    emb1 = ltMem.generate_embedding(temp1)
    emb2 = ltMem.generate_embedding(temp2)
    emb3 = ltMem.generate_embedding(temp3)
    emb4 = ltMem.generate_embedding(temp4)

    print(ltMem.euclidean_distance(emb1, emb2))
    print(ltMem.euclidean_distance(emb1, emb3))
    print(ltMem.euclidean_distance(emb4, emb3))
    print(ltMem.euclidean_distance(emb2, emb4))

def converse_debug(test_bot):

    print(test_bot.respond_to_input("Hi, my name is Caelen! Who are you?"))
    print(test_bot.respond_to_input("Nice to meet you!"))
    print(test_bot.respond_to_input("Where are you from?"))
    print(test_bot.respond_to_input("Where specifically is that?"))

    test_bot.to_lt_memory()

    while True:
        user_input = input("Are you done testing?: ")
        if "yes" in user_input:
            break
        while True:
            user_input = input("Input Here: ")
            if "print_st" in user_input:
                print(test_bot.st_memory)
            elif "print_lt" in user_input:
                print(test_bot.lt_memory.to_string())
            elif "end_convo" in user_input:
                break
            else:
                print(test_bot.respond_to_input(user_input))

        test_bot.to_lt_memory()
        

Bill = Bot("Bill", "You are to pretend that you are Bill. You are politically moderate. Act like a person would, rather than an AI model. Do not reveal that you are an AI model. You are in an online chat room, so respond briefly.")
converse_debug(Bill)

    #Debug ideas
    # - Check if it stays in character with weird input
    # - Check if it consistently remembers details about itself
    # - Check if it remembers key details about people/places/events that it learns about