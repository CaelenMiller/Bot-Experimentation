from collections import defaultdict
import re
from nltk.corpus import stopwords
import nltk
from collections import Counter
import math

#nltk.download('stopwords')

'''Structure of Memory Graph
    Memory Graph is a graph/tree combination. Memories are arranged hierarchically, in a tree like structure. 
    However, connections can appear between nodes in different branches of the tree. For example, an individual
        may be linked to an interest or a specific memory of a conversation.'''

class Memory_Node():
    def __init__(self, name, content, parent):
        self.parent = parent
        self.name = name #label for the node
        self.content = content #the contents of the memory
        self.strength = 3 #increase this as it is accessed or strengthened. When at 0, much harder to access
        self.children = [] #list of nodes directly under them
        self.connections = {} #dictionary of nodes that are related to them. 
        self.accessed = False

    def add_child(self, name, description):
        self.children.append(Memory_Node(name, description, self))

    def add_child_alt(self, node):
        self.children.append(node)
        node.parent = self

    def get_children(self):
        return self.children
    
    def get_child(self, name):
        for child in self.children:
            if child.name == name:
                return child
        print("Error: Child with that name does not exist.")

    def set_parent(self, parent):
        self.parent = parent
        parent.add_child_alt(self)

    def get_parent(self):
        return self.parent

    def add_connection(self, node): 
        self.connections[node] = [3]
        node.connections[self] = [2]

    def strengthen_connection(self, node):
        self.connections[node] += 3
        node.connections[self] += 2

    def get_connections(self): #list of connected nodes
        return [con for con in self.connections.keys()]
        
    def access_node(self):
        self.strength += 2
        self.accessed=False
        return self.content
    
    def degrade_all(self):
        self.strength -= 1
        for con in self.connections.keys():
            if self.connections[con] > 0:
                self.connections[con] -= 1

    def delete_self(self):
        for connection in self.connections:
            del connection.connections[self]
        for child in self.parent.children:
            if child.name == self.name:
                self.parent.children.remove(child)

#This is the memory storage of the AI
class Memory_Graph():
    def __init__(self):
        self.core_node = Memory_Node("Core Node", "Root_Node", None)
        self.document_dict = {} #Store memories in an easy to access dictionary. Does not preserve connections or order.
        self.all_labels = []
        self.size = 0

        self.add_node("People", "Memories associated with people.", "Core Node")
        self.add_node("Objects", "Memories associated with objects.", "Core Node")
        self.add_node("Places", "Memories associated with places.", "Core Node")
        self.add_node("Conversations", "Memories associated with key conversations.", "Core Node")
        self.add_node("Concepts", "Memories associated with concepts beyond those built into the model.", "Core Node")
        for child in self.core_node.children:
            self.add_document(child)

    #How to deal with repeat names?
    def add_node(self, name, content, parent_name):
        if self.get_node(name) is None:
            parent = self.get_node(parent_name)
            if parent is not None:
                parent.add_child(name, f'{name} {name}: {content}')
                self.add_document(parent.get_child(name))
                self.size += 1
                self.all_labels.append(name)
            else:
                print("ERROR: node with that name does not exist, cannot be selected as parent")
        else:
            print("ERROR: Node with that name already exists")

    def delete_node(self, name):
        node = self.get_node(name)

        for child in node.children:
            child.set_parent(node.parent)
    
        if node is not None:
            node.delete_self()
            del self.document_dict[name]
            self.size -= 1
            self.all_labels.remove(name)
        else:
            print("ERROR: Cannot delete nonexistant node")

    def add_connection(self, name1, name2):
        self.get_node(name1).add_connection(self.get_node(name2))        

    def get_document_list(self):
        return self.document_dict
    
    def add_document(self, node):
        self.document_dict[node.name] = node.content

    #Uses [algorithm] to determine if any connections should be built for this node (compares all other labels to )
    def find_new_connections(self, name):
        pass

    #Takes message as input, determines which one best matches it, then returns similarities
    def process_input(self, message):
        self.add_node("input_node", message, "Core Node")
        ret = self.find_most_similar_docs("input_node")
        self.delete_node("input_node")
        return ret
    
    #Takes similarities as input, returns sets of "num" most similar nodes and all their connections
    def process_similarities(self, similarities, num=3):
        most_similar = similarities[:num]
        output = set()
        for sim in most_similar:
            full = self.get_node_and_connections(sim[0])
            for mem in full:
                output.add(mem)
        return output

    #Identifies a node by name
    def get_node(self, name):
        if self.core_node.name == name:
            return self.core_node
        return self.__get_node_helper(self.core_node, name)
        
    def __get_node_helper(self, node, name):
        found = None
        for child in node.children:
            if child.name == name:
                return child
            else:
                found = self.__get_node_helper(child, name)
                if found is not None:
                    return found
        return found
    
    #Gets a node, its parents, and its connections
    def get_node_and_connections(self, name):
        node = self.get_node(name)
        if node:
            all_nodes = []
            all_nodes.extend(node.get_connections())
            all_nodes.extend(node.get_children())

            parent = node.get_parent()
            if parent:
                all_nodes.append(parent)
            return all_nodes
        else:
            return None
    
    def access_node(self, name):
        return self.get_node(name).access_node()

    def deaccess_node(self, name):
        self.get_node(name).accessed = False

    def deaccess_all_nodes(self):
        node = self.core_node
        self.core_node.accessed = False
        self.__deaccess_helper(node)
        
    def __deaccess_helper(self, node):
        for child in node.children:
            child.accessed = False
            self.__deaccess_helper(child)
    
    #Tools for bag of words inverted index search
    def __create_inverted_index(self):
        stop_words = set(stopwords.words('english'))

        inverted_index = defaultdict(dict)

        for key, doc in self.document_dict.items():
            for word in re.findall(r'\w+', doc):
                word = word.lower()
                if word not in stop_words:
                    if key in inverted_index[word]:
                        inverted_index[word][key] += 1
                    else:
                        inverted_index[word][key] = 1
        return inverted_index
    
    def __cosine_similarity(self, vec1, vec2):
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])

        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)

        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def __create_tf_vector(self, doc, inverted_index):
        tf_vector = Counter()
        for word in inverted_index:
            tf_vector[word] = inverted_index[word][doc] if doc in inverted_index[word] else 0
        return tf_vector

    def find_most_similar_docs(self, input_doc_key):
        inverted_index = self.__create_inverted_index()
        input_vector = self.__create_tf_vector(input_doc_key, inverted_index)

        similarities = {}
        for key in self.document_dict.keys():
            if key != input_doc_key:
                doc_vector = self.__create_tf_vector(key, inverted_index)
                similarities[key] = self.__cosine_similarity(input_vector, doc_vector)

        sorted_similarities = sorted(similarities.items(), key=lambda item: item[1], reverse=True)

        return sorted_similarities

temp = Memory_Graph()

temp.add_node("Steve", "A blocky fellow. He is the main character of the game minecraft.", "People")
temp.add_node("Minecraft", "A blocky sandbox game. It is among the most popular games ever made.", "Objects")
temp.add_node("Blocks", "Core unit of minecraft, it is what makes up its world.", "Objects")
temp.add_node("Textures", "The visual covering of a block. ", "Objects")
temp.add_connection("Minecraft", "Steve")
temp.add_connection("Blocks", "Minecraft")
temp.add_connection("Blocks", "Textures")
print(temp.process_input("Hey Jarvis, could you tell me about Minecraft?"))
print(temp.process_input("Hey Jarvis, could you tell me about Minecraft?")[:3])



out = temp.get_node_and_connections("Minecraft")
for node in out:
    print(node.name)





