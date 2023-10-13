The purpose of this project is to develop a meaningful way to have bots converse. This could be used in designing AI thinktanks, or for research where simulating conversations is important. 


To make this work you need an API key. Just make a file called APIkey.py and place it in the project folder. Include the following in it:

    import openai
    openai.organization = "ORGANIZATION NAME"
    openai.api_key = "API KEY"