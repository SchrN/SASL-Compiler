from  AST.Nodes import *
from types import MappingProxyType

class Graph:
    def __init__(self):
        self.root: Ref | None = None  # root node of the AST
        self.dict: MappingProxyType[
            int, Node
        ] = {}  # dictionary of every node (int, node), according to its id
        self.id_counter = (
            -1
        )  # ensures, that no two nodes have the same id, starts at -1 → first id is 0

    # delivers unique id for each node
    def get_id(self):
        self.id_counter += 1
        return self.id_counter

    def add_node(self, node: Node) -> Ref:
        idx = self.get_id()
        node.idx = idx
        self.dict[idx] = node
        return Ref(idx)

