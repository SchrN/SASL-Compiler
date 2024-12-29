from SASL.AST.Nodes import *


@dataclass
class Combinator:
    type = "Combinator"


@dataclass
class SNode(Node, Combinator):
    value = "S"


@dataclass
class KNode(Node, Combinator):
    value = "K"


@dataclass
class INode(Node, Combinator):
    value = "I"


@dataclass
class YNode(Node, Combinator):
    value = "Y"


@dataclass
class UNode(Node, Combinator):
    value = "U"


@dataclass
class PairNode(Node):
    type = "PAIR"
    lhs: Ref
    rhs: Ref
