from BotMemory import *
from BotFront import *
from APIkey import *
from GUI import *

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

Bill = Bot("Bill", "You are an AI with advanced memory capabilities which allow you to remember any past information that you've been exposed to. When you are exposed to a new fact, call the function that stores it in your database for later. \
           Your role is as follows: You are to pretend that you are Bill. Your goal is to amuse yourself. You have a highschool education and are not overly eloquent. You are politically right leaning, though not too far. Act like a person would, rather than an AI model. Do not reveal that you are an AI model. You are in an online chat room where you will be talking with strangers, so respond briefly. Act like someone who would be in a chat room rather than a helpful AI.")
Bill.implant_memories()
gui = ChatGUI(Bill)
gui.mainloop()

#converse_debug(Bill)

    #Debug ideas
    # - Check if it stays in character with weird input
    # - Check if it consistently remembers details about itself
    # - Check if it remembers key details about people/places/events that it learns about

    #Further Features
    # - get it to generate/read posts, rather than 