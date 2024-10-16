from dataclasses import dataclass, field


@dataclass
class Node:
    idx: int = field(init=False)


@dataclass
class Ref:
    ref: int


@dataclass
class RootNode(Node):
    definitions = {}
    bdy = None
    repr = "root"


@dataclass
class IdNode(Node):
    type = "ID"
    value: str


@dataclass
class NumNode(Node):
    type = "NUMBER"
    value: int


@dataclass
class BoolNode(Node):
    type = "BOOL"
    value: "true" or "false"


@dataclass
class StringNode(Node):
    type = "STRING"
    value: str


@dataclass
class ApplNode(Node):
    type = "APPL"
    lhs: Ref
    rhs: Ref
    repr = "@"


@dataclass
class AbstrNode(Node):
    type = "ABST"
    lhs: Ref
    rhs: Ref


@dataclass
class ArgNode(Node):
    type = "ARG"
    lhs: Ref
    rhs: Ref


@dataclass
class WhereNode(Node):
    type = "WHERE"
    bdy: Ref
    definitions: dict[str, Ref]


# Arithmetic Nodes
@dataclass
class BuiltIn:
    type = "BUILTIN"


@dataclass
class ORNode(Node, BuiltIn):
    type = "OR"


@dataclass
class ANDNode(Node, BuiltIn):
    type = "AND"


@dataclass
class ColonNode(Node, BuiltIn):
    type = "COLON"
    repr = ":"


@dataclass
class NotNode(Node, BuiltIn):
    type = "NOT"


# Arithmetic Nodes
@dataclass
class MulNode(Node, BuiltIn):
    type = "MULTIPLY"
    repr = "⋅"


@dataclass
class DivNode(Node, BuiltIn):
    type = "DIVIDE"
    repr = "/"


@dataclass
class PlusNode(Node, BuiltIn):
    type = "PLUS"
    repr = "+"


@dataclass
class MinusNode(Node, BuiltIn):
    type = "MINUS"
    repr = "-"


# Rel Operations
@dataclass
class LTEQNode(Node, BuiltIn):
    type = "LTEQ"
    repr = "<="


@dataclass
class GTEQNode(Node, BuiltIn):
    type = "GTEQ"
    repr = ">="


@dataclass
class LTNode(Node, BuiltIn):
    type = "LT"
    repr = "<"


@dataclass
class GTNode(Node, BuiltIn):
    type = "GT"
    repr = ">"


@dataclass
class NEQNode(Node, BuiltIn):
    type = "NEQ"
    repr = "!="


@dataclass
class EQNode(Node, BuiltIn):
    type = "EQ"
    repr = "="


@dataclass
class NilNode(Node, BuiltIn):
    type = "NIL"
    repr = "nil"


@dataclass
class HDNode(Node, BuiltIn):
    type = "HD"
    repr = "hd"


@dataclass
class TLNode(Node, BuiltIn):
    type = "TL"
    repr = "tl"


@dataclass
class CondNode(Node, BuiltIn):
    value = "cond"
    repr = "cond"
