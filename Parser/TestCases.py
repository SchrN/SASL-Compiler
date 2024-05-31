from Parser import *


lex = Lexer("def id x = x")   #initializing lexer
lex.get_tokens()

pars = Parser()       #initializing parser
pars.lexer = lex

assert pars.lexer.lookahead().type == "DEF"
pars.advance()
assert pars.current_token.type == "DEF"
assert pars.lexer.lookahead().type == "ID"
assert (pars.match("ID") == True)

#pars.match("error") #works like intended




#testing atomic value number
lex1 = Lexer("3 22 4 5")
lex1.get_tokens()

pars1 = Parser()
pars1.lexer = lex1

pars1.create_graph()
print(pars1.graph.dict[0].value)
print(pars1.graph.dict[1])
print(pars1.graph.dict)




