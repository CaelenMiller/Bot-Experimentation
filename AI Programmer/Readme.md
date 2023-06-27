The purpose of this project is to create a semi-independent AI programmer. I am attempting to achieve this by having a GPT model write code, execute it, then respond to the success or error message. I am also planning on implementing a human in the loop element that allows for human feedback or testing.


To make this work you need an API key. Just make a file called APIkey.py and place it in the project folder. Include the following in it:

    import openai
    openai.organization = "ORGANIZATION NAME"
    openai.api_key = "API KEY"