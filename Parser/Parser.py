import copy
from dataclasses import dataclass
from re import T
from typing import Union
from Lexer.Lexer import *
from AST.Graph import *


class Parser(Graph):

    graph : Graph
    lexer : Lexer
    current_token : Token


    def advance(self):
        self.current_token = self.lexer.submit_token()

    def match(self, tt : TokenType):
        if self.lexer.lookahead().type == tt :
            return True


    def create_graph(self):
        self.graph = Graph()
        self.system()

    def mulop_helper(self,Token):

        return Token.type == TokenType.MULTIPLY or Token.type == TokenType.DIVIDE

    def relop_helper(self, Token):

        return (
                Token.type == TokenType.LTEQ
                or Token.type == TokenType.GTEQ
                or Token.type == TokenType.LT
                or Token.type == TokenType.GT
                or Token.type == TokenType.NEQ
                or Token.type == TokenType.EQ
        )

    def simple_helper(self, Token):
        return (
                Token.type == TokenType.ID  # <name>
                or self.builtin_helper(Token)  # <builtin>
                or self.constant_helper(Token)  # <constant>
                or Token.type == TokenType.OPEN  # (
        )

    def builtin_helper(self,Token):

        return Token.type == TokenType.HD or Token.type == TokenType.TL

    def boolop_helper(self, Token):

        return Token.type == TokenType.TRUE or Token.type == TokenType.FALSE

    def constant_helper(self, Token):

        return (
                Token.type == "NUMBER"
                or self.boolop_helper(Token)
                or Token.type == TokenType.STRING
                or Token.type == TokenType.NIL
                or Token.type == TokenType.SQOPEN
        )

    def prefix_helper(self, Token):

        return (
                Token.type == TokenType.MINUS
                or Token.type == TokenType.PLUS
                or Token.type == TokenType.NOT
        )

    def builtin_helper(self, Token):
        return Token.type == TokenType.HD or Token.type == TokenType.TL

    def system(self):
        print("system")
        print(self.lexer.lookahead().type)
        if (self.match("DEF")):
            self.funcdefs();
            if (self.match("DOT")):
                self.advance()
        else:
            print("system7")
            Treee = self.expr()


    def funcdefs(self):
        print("funcdefs")

    def expr(self):
        print("expr")
        condNode = self.condexpr();
        expr1Node = self.expr1()
        if (expr1Node == None):
            print("exprA")
            return condNode

    def condexpr(self):
        print("condexpr")
        resultNode = None
        if(self.lexer.lookahead().type == "IF"):
            print("condexprA")
            self.lexer.submit_token()
            if (self.lexer.lookahead().type == "THEN"):
                print("condexprB")
                self.lexer.submit_token()
                if (self.lexer.lookahead().type == "ELSE"):
                    print("condexprC")
                    self.lexer.submit_token()
        else:
            print("condexprH")
            resultNode = self.listexpr()

        print("condexprI")
        return resultNode

    def listexpr(self):
        print("listexpr")
        opNode = self.opexpr()
        listNode = self.listexpr1()
        if (listNode != None):
            print("listexprA")
            if (4 == 3):
                print("listexprB")
                ###palceholeder

        print("listexprD")
        return opNode;


    def opexpr(self):
        print("opexpr")
        return self.opexpr1(self.conjunct())

    def opexpr1(self, Node):
        print("opexpr1")

    def conjunct(self):
        print("conjunct")
        return self.conjunct1(self.compar())

    def conjunct1(self, conjunctNode):
        print("conjuct1")
        tempNode = conjunctNode
        if (self.lexer.lookahead()== "AND"):
            self.lexer.submit_token()

        return tempNode

    def compar(self):
        print("compar")
        addnode = self.add()
        return self.compar1(addnode)

    def add(self):
        print("add")
        mul = self.mul()
        return self.add1(mul);

    def add1(self, right):
        print("add1")

    def mul(self):
        print("mul")
        right = self.factor();
        return self.mul1(right)

    def mul1(self, right):
        print("mul1")
        if(self.mulop_helper(self.lexer.lookahead())):
            return
        else:
            return right

    def factor(self):
        print("factor")
        if (self.prefix_helper(self.lexer.lookahead()) == True):
            print("l")  ####PLACEHOLDER


        return self.comb()

    def comb(self):
        print("comb")
        sim = self.simple()
        print(sim)
        return self.comb1(sim);

    def simple(self):
        print("simple")
        resultnode = None

        temp = self.lexer.lookahead()

        if  (self.builtin_helper(temp) == True):
            print("error")
            resultnode = self.builtin()
        elif(temp.type == "ID"):
            print("error")
            print("NAME BRACKET")
            resultnode = self.name()
        elif(self.constant_helper(temp) == True):
            resultnode = self.constant()
        elif(temp.type == "SQOPEN"):
            print("error")
            self.lexer.submit_token()
            tempNode = self.expr()
            if(self.lexer.lookahead() != "SQCLOSE"):
                print("ERROR ")
            else:
                self.lexer.submit_token()
                resultnode = tempNode


        return resultnode;


    def constant(self):
        print("constant")
        resultNode = None;
        token = self.lexer.lookahead()
        if (token.type == "NUMBER"):
            resultNode = self.num()
        elif (token.type == "BOOl"):
            resultNode = self.bool()
        elif (token.type == "STRING"):
            resultNode = self.string()
        elif (token.type == "NIL"):
            self.lexer.submit_token()
        elif (token.type == "SQOPEN"):
            self.lexer.submit_token()
        else:
            "error"
        return resultNode

    def num(self):
        token = self.lexer.lookahead()
        node = IntNode(2)
        node.value = token.get_value()
        result =self.graph.add_node(node)
        self.advance()
        return result

    def name(self):
        print("name")

    def comb1(self, left):
        print("comb1")
        print(left)
        if (self.simple_helper(self.lexer.lookahead())):
            result = Appl(left, self.simple())
            self.graph.add_node(result)
            return self.comb1(result)
        else:
            return left



    #def comb122(self, left):
     #   print("comb1")
      #  print(left)
       # if (self.simple_helper(self.lexer.lookahead())):
        #    print("Application getting built")
         #   print(self.simple())
          #  result = Appl
           # Appl.lhs = left
           # Appl.rhs = self.simple()
            #return self.comb1(result)
        #else:
           # return left




    def compar1(self, nodeLeft):
        print ("compar1")
        if (self.relop_helper(self.lexer.lookahead()) == True) :
            print("l") ####PLACEHOLDER

        return nodeLeft


    def listexpr1(self):
        print ("listexpr1")
        if (self.lexer.lookahead().type == "COLON"):
            print("listexpr1a")
            self.lexer.submit_token()
            return self.expr()
        else:
            print("listexpr1B")
            return None




    def expr1(self):
        print("expr1")
            #if (lexer.lookAhead().getType() == TokenType.DEF) {
            #funcdefs(); // RETURN Abstraction
            #if (lexer.lookAhead().getType() == TokenType.DOT) {
            #lexer.nextToken();
            #AST_Node callTree = expr(); // RETURN Application
            #String callString = "00FuncCall00";


