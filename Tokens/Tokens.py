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

    # identifier
    ID = r"[a-zA-Z_][a-zA-z_0-9]*"

    # types
    NUMBER = r"\d+(\.\d*)?"
    STRING = r'(".+")'
    TRUE = r"true"
    FALSE = r"false"

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
    DOT = r"\."
    COMMA = r","
    SEMICOLON = r";"
    COLON = r":"
    OPEN = r"\("
    CLOSE = r"\)"
    SQOPEN = r"\["
    SQCLOSE = r"\]"  # FIXME this after id gets into one token with the id (see line 23 prelude.sasl)


class Token(NamedTuple):
    type: TokenType
    value: str
    line: int
    position: int

    def get_value(self):
        return self.value
