The purpose of this project is to determine the best method to create an AI with a persistent personality using chatgpt/gpt4. This includes experiments with memory, memory summarization, using a combination of models, and saving personalities for use for later. 


To make this work you need an API key. Just make a file called APIkey.py and place it in the project folder. Include the following in it:

    import openai
    openai.organization = "ORGANIZATION NAME"
    openai.api_key = "API KEY"
