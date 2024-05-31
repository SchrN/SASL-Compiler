from AST.Graph import *

from AST.Nodes import *
from AST.Graph import *

# Tree from handout, page 14
# Code: def incr x = 1 + x . incr x where x = 41

g = Graph()

a = IntNode
a.value = 3

b = IntNode
b.value = 4

c = Appl

g.add_node(c(g.add_node(a), g.add_node(b)))

print(g.dict)