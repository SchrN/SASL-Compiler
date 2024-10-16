from typing import NamedTuple
from enum import Enum
import re


class TokenType(Enum):
    # special
    WHITESPACE = r"\ |\t"
    NEWLINE = r"\n"
    COMMENT = r"\|\|.*"

    # keywords
    EOF = r"\Z"
    DEF = r"def"
    WHERE = r"where"
    IF = r"if"
    ELSE = r"else"
    THEN = r"then"
    AND = r"and"
    OR = r"or"
    NOT = r"not"
    HD = r"hd"
    TL = r"tl"
    NIL = r"nil"

    TRUE = r"true"
    FALSE = r"false"

    DOT = r"\."

    # identifier
    ID = r"[a-zA-Z_][a-zA-z_0-9]*\b"

    # types
    NUMBER = r"\d+"
    STRING = r'(".+")'

    # arithmetic
    PLUS = r"\+"
    MINUS = r"-"
    MULTIPLY = r"\*"
    DIVIDE = r"\/"

    # operators
    LTEQ = r"<="
    GTEQ = r">="
    LT = r"<"
    GT = r">"
    NEQ = r"~="
    EQ = r"="

    # symbols
    COMMA = r","
    SEMICOLON = r";"
    COLON = r":"
    OPEN = r"\("
    CLOSE = r"\)"
    SQOPEN = r"\["
    SQCLOSE = r"\]"


class Token(NamedTuple):
    type: TokenType
    value: str
    line: int
    position: int

    def get_value(self):
        return self.value
