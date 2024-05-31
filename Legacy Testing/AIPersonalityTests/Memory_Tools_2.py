

class Memory_Node:
    def __init__(self, node_type, label, contents):
        self.type = node_type
        self.contents = contents
        self.title = label
        self.edges = []


class Memory_Graph:
    def __init__(self):
        self.size = 0
        self.nodes = dict()

    def add_node(self, node_type, label, contents):
        node = Memory_Node(node_type, label, contents)
        self.nodes[label] = node
        self.size += 1

    def add_edge(self, node1, node2):
        node1.edges.append(node2)
        node2.edges.append(node1)

    def del_edge(self, node1, node2):
        node1.edges.remove(node2)
        node2.edges.remove(node1)

    def del_node(self, node):
        for tnode in node.edges:
            self.del_edge(tnode, node)
        del self.nodes[node.label]
        self.size -= 1

    def get_all_of_type(self, node_type):
        targeted_nodes = []
        for node_name in self.nodes.keys():
            if self.nodes[node_name].node_type == node_type:
                targeted_nodes.append(self.nodes[node_name])
        return targeted_nodes

        
    