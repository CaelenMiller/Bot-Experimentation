"""This file includes the memory structure for the bot. The core memory structure is simply a dictionary with
embeddings as the keys and summaries as the values. When searching for a memory, a string is input, for which
an embedding is generated. The system then returns the n most similar summaries that are within a range and
have not been used in the current conversation."""

from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np

'''LT memory is essentially a dictionary that uses embeddings as keys and summaries as values.'''
class LTMemory_System():
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.model = AutoModel.from_pretrained("bert-base-uncased")
        self.lt_memory = dict() #hash -> summary
        self.keys = dict() #hash -> embedding
        

    def generate_embedding(self, doc_string): #input: document string, output: numerical embeddings
        inputs = self.tokenizer(doc_string, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.mean(dim=1)
        return np.array(embeddings)

    def add_memory(self, summary): #input: summary string
        embedding = self.generate_embedding(summary)
        hashed = hash(embedding.tostring())
        self.lt_memory[hashed] = summary
        self.keys[hashed] = embedding

    def access_memory(self, embedding): #input: numerical embedding; output: summary
        return self.lt_memory[hash(embedding.tostring())]
    
    def get_closest_memories(self, embedding, k=3): #input: embedding; output: k closest summaries, k closest embeddings
        distances = []
        for i, embedding_2 in enumerate(self.keys.keys()):
            dist = self.euclidean_distance(embedding, embedding_2)
            distances.append((embedding_2, dist))
            
        distances.sort(key=lambda x: x[1])
        
        k_closest_indices = [x[0] for x in distances[:k]]
        
        return [self.lt_memory[embedding] for embedding in k_closest_indices], [embedding for embedding in k_closest_indices]
    

    def euclidean_distance(self, arr1, arr2):
        return np.linalg.norm(arr1 - arr2)
    
    def to_string(self):
        output = ""
        for key, value in self.lt_memory.items():
            output += f"{key}: {value}\n"
    


        