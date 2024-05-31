import openai


openai_llm = ["gpt-3.5-turbo-16k-0613", "gpt-4-1106-preview"]

class LLM_Holder():
    def __init__(self, llm="gpt-3.5-turbo-16k-0613"):
        self.llm = llm
        self.API_calls = 0
        self.tokens = 0

    
    def generate_response(self, st_memory, tools=[]):
        self.perform_token_count(st_memory)

        if self.llm in openai_llm:
            if len(tools) > 0:
                response = openai.ChatCompletion.create(
                model=self.llm,
                messages=st_memory,
                tools=tools)
            else:
                response = openai.ChatCompletion.create(
                model=self.llm,
                messages=st_memory)
            return response
        else:
            #["choices"][0]["message"]["content"] Must be in this format to work correctly
            return "ERROR - INVALID LLM"
        
    def get_api_calls(self):
        return self.API_calls

    def get_tokens_passed(self):
        return self.tokens


    #Counts number of tokens in a memory array. Helpful for figuring out how expensive this is going to be.
    def __count_tokens(self, mem_array):
        token_sum = 0
        # Simple tokenization by splitting on spaces
        for message in mem_array:
            text = message["content"]
            tokens = text.split()
            token_sum += len(tokens)
        return token_sum
    

    def perform_token_count(self, call_contents):
        self.API_calls += 1
        self.tokens += self.__count_tokens(call_contents)


