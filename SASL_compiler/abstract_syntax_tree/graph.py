from SASL.AST.Nodes import *


class Graph:
    def __init__(self):
        self.root = RootNode()  # root node of Graph
        self.dict: dict[
            int, Node
        ] = {}  # dictionary of every node (int, node), according to its id
        self.id_counter = (
            -1
        )  # ensures, that no two nodes have the same id, starts at -1 ? first id is 0
        self.count = [10]  # For printing the graph

    # delivers unique id for each node
    def get_id(self) -> int:
        self.id_counter += 1
        return self.id_counter

    def add_node(self, node: Node) -> Ref:
        idx = self.get_id()
        node.idx = idx
        self.dict[idx] = node
        return Ref(idx)

    def get_node(self, ref: Ref) -> Node:
        index = ref.ref
        return self.dict[index]

    def print_graph(self, node, space):

        space += self.count[0]

        if hasattr(node, "rhs"):
            if node.rhs != None:
                self.print_graph(self.dict[node.rhs.ref], space)

        print()
        for i in range(0, space):
            print(end=" ")
        print(node)

        if hasattr(node, "lhs"):
            if node.lhs != None:
                self.print_graph(self.dict[node.lhs.ref], space)
                
    def get_repr(self, n:Node) -> str:
        try:
            repr = "({}) {}".format(n.idx, n.repr)
        except:
            try:
                repr = "({}) {}".format(n.idx, n.value)
            except:
                repr = "({}) {}".format(n.idx, n.type)
        return repr

    def dot_graph_worker(self, n: Node, saving_path: str):
        # open file to append to it
        f = open(saving_path, "a")

        # representation of n in dot-graph
        if isinstance(n, RootNode):
            n_repr = n.repr
        else:
            n_repr = self.get_repr(n)

        f.write('\t"{}";\n'.format(n_repr))

        if hasattr(n, "lhs"):
            if n.lhs != None:
                lhs = self.get_node(n.lhs)
                lhs_repr = self.get_repr(lhs)

                f.write('\t"{}" -> "{}";\n'.format(n_repr, lhs_repr))
                self.dot_graph_worker(lhs, saving_path)

        if hasattr(n, "rhs"):
            if n.rhs != None:
                rhs = self.get_node(n.rhs)
                rhs_repr = self.get_repr(rhs)
                    
                f.write('\t"{}" -> "{}";\n'.format(n_repr, rhs_repr))
                self.dot_graph_worker(rhs, saving_path)
        if hasattr(n, "bdy"):
            if n.bdy != None:
                bdy = self.get_node(n.bdy)
                bdy_repr = self.get_repr(bdy)

                f.write('\t"{}" -> "{}"[label="body"];\n'.format(n_repr, bdy_repr))
                self.dot_graph_worker(bdy, saving_path)
        if hasattr(n, "definitions"):
            if len(n.definitions) > 0:
                for index in n.definitions:
                    definition = self.get_node(n.definitions[index])
                    definition_repr = self.get_repr(definition)

                    f.write(
                        '\t"{}" -> "{}" [style=dotted, label="def {}"];\n'.format(
                            n_repr, definition_repr, index
                        )
                    )
                    self.dot_graph_worker(definition, saving_path)
        f.close()

    def make_dot_graph(self, n: Node, saving_path: str):
        # empty the file with given name
        f = open(saving_path, "w")
        # add beginning of
        f.write("digraph G {\n")
        f.write('\tsize = "7,7";\n')
        f.write('\tdpi = "300"')
        f.close()

        # worker adds all nodes the descend from n
        self.dot_graph_worker(n, saving_path)

        # end graph
        f = open(saving_path, "a")
        f.write("}")
        f.close
