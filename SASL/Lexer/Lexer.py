from SASL.Tokens.Tokens import *
import re


class Lexer:
    def __init__(self, data):
        self.data = data
        self.actual_token = None
        self.list_tokens = None

    def get_tokens(self):
        tokens = []

        tok_regex = r"|".join(
            rf"(?P<{TokenType.name}>{TokenType.value})" for TokenType in TokenType
        )
        line = 1
        line_start = 0
        for match in re.finditer(tok_regex, self.data):
            type = match.lastgroup
            value = match.group()
            position = match.start() - line_start
            if type == "NEWLINE":
                line_start = match.end()
                line += 1
                continue
            elif type == "WHITESPACE" or type == "COMMENT":
                continue
            tokens.append(Token(type, value, line, position))

            if type == "EOF":
                self.list_tokens = tokens

    def submit_token(self):
        self.actual_token = self.list_tokens[0]
        self.list_tokens.pop(0)

    def lookahead(self):
        return self.list_tokens[0]
