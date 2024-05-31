"""This file includes the memory structure for the bot. The core memory structure is simply a dictionary with
embeddings as the keys and summaries as the values. When searching for a memory, a string is input, for which
an embedding is generated. The system then returns the n most similar summaries that are within a range and
have not been used in the current conversation."""

from sentence_transformers import SentenceTransformer
import torch
import numpy as np

'''LT memory is essentially a dictionary that uses embeddings as keys and summaries as values.'''
class LTMemory_System():
    def __init__(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')
        
        self.lt_memory = dict() #tuple -> summary
        
    def generate_embedding(self, doc_string): #input: document string, output: numerical embeddings
        inputs = [doc_string]
        with torch.no_grad():
            outputs = self.model.encode(inputs)
        output = outputs[0]
        return tuple(output)

    def add_memory(self, summary): #input: summary string
        embedding = self.generate_embedding(summary)
        self.lt_memory[embedding] = summary

    def access_memory(self, embedding): #input: embedding; output: summary
        return self.lt_memory[embedding]
    


    def embedding_search(self, input, k=3, mode="embedding"): #input: embedding; output: k closest summaries, k closest embeddings
        if mode=="embedding":
            embedding = input
        else:
            embedding = self.generate_embedding(input)
            
        distances = []
        for i, embedding_2 in enumerate(self.lt_memory.keys()):
            dist = self.euclidean_distance(embedding, embedding_2)
            distances.append((embedding_2, dist))
            
        distances.sort(key=lambda x: x[1])
        
        k_closest_indices = [x[0] for x in distances[:k]]
        
        return [self.lt_memory[embedding] for embedding in k_closest_indices], [embedding for embedding in k_closest_indices]
    

    def euclidean_distance(self, arr1, arr2):
        return np.linalg.norm(np.array(arr1) - np.array(arr2))
    
    def to_string(self):
        output = ""
        for key, value in self.lt_memory.items():
            output += f"{key}: {value}\n"
        return output


        