from dataclasses import dataclass, field


@dataclass
class Node():
    idx: int = field(init=False)


@dataclass
class Ref:
    ref: int


@dataclass
class CondNode(Node):
    value = "cond"


@dataclass
class RootNode(Node):
    lhs: Ref
    rhs: Ref


@dataclass
class IntNode(Node):
    value: int


@dataclass
class BoolNode(Node):
    value: bool


@dataclass
class StringNode(Node):
    value: str


@dataclass
class Appl(Node):
    lhs: Ref
    rhs: Ref


@dataclass
class EqNode(Node):
    lhs: Ref
    rhs: Ref


@dataclass
class WhereNode(Node):
    bindings: dict[str, Ref]
    body: Ref