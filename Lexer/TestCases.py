from Lexer import *


lex = Lexer("def id x = x")
lex.get_tokens()  #convert into list
print (lex.list_tokens)
assert lex.lookahead().type ==  TokenType.DEF.name
#look into next Token
lex.submit_token() #save this token and take it out of the list
assert lex.actual_token.type == "DEF"
assert (lex.lookahead().type == "ID" and lex.lookahead().value == "id")
lex.submit_token()
assert lex.actual_token.type == "ID"
assert lex.lookahead().type == "ID"
lex.submit_token()
assert lex.actual_token.type == "ID"
assert lex.lookahead().type == "EQ"
lex.submit_token()
assert lex.actual_token.type == "EQ"
assert lex.lookahead().type == "ID"
lex.submit_token()
assert lex.actual_token.type == "ID"
assert lex.lookahead().type == "EOF"
lex.submit_token()
assert lex.actual_token.type == "EOF"


