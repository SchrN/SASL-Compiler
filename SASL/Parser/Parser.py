import sys
from SASL.Lexer.Lexer import *
from SASL.AST.Graph import *


class Parser(Graph):
    graph: Graph
    lexer: Lexer
    current_token: Token

    def advance(self):
        self.current_token = self.lexer.submit_token()

    def match(self, tt: TokenType) -> bool:
        if self.lexer.lookahead().type == tt.name:
            self.advance()
            return True

    def require(self, tt: TokenType):
        if self.lexer.lookahead().type == tt.name:
            self.advance()
            return True
        else:
            sys.exit(
                str(tt.name)
                + " expected but "
                + self.lexer.lookahead().type
                + " received"
            )

    def create_graph(self):
        self.graph = Graph()
        self.system()

    def system(self):
        self.graph.root.definitions = {}
        if self.lexer.lookahead().type == TokenType.DEF.name:
            self.funcdefs()
            if self.match(TokenType.DOT):
                bdy_ref = self.expr()
                self.graph.root.bdy = bdy_ref

        else:
            bdy_ref = self.expr()
            self.graph.root.bdy = bdy_ref

    def funcdefs(self):
        if self.require(TokenType.DEF):
            self.definition()
            self.funcdefs1()

    def funcdefs1(self):
        if self.match(TokenType.DEF):
            self.definition()
            self.funcdefs1()

    def defs(self, where_dict):
        localdef_ref = self.localdef()
        localdef_node = self.graph.get_node(localdef_ref)

        id_ref = localdef_node.lhs
        id_node = self.graph.get_node(id_ref)

        def_value = localdef_node.rhs

        fun_name = id_node.value

        where_dict[fun_name] = def_value

        if self.lexer.lookahead().type == TokenType.SEMICOLON.name:
            self.defs1(where_dict)
        else:
            return def_value

    def defs1(self, where_dict):
        if self.match(TokenType.SEMICOLON):
            localdef_ref = self.localdef()
            localdef_node = self.graph.get_node(localdef_ref)

            id_ref = localdef_node.lhs
            id_node = self.graph.get_node(id_ref)

            def_value = localdef_node.rhs

            fun_name = id_node.value

            where_dict[fun_name] = def_value

            self.defs1(where_dict)

    def localdef(self):
        name_node_ref = self.name()

        if name_node_ref is not None:
            abstraction_ref = self.abstraction(name_node_ref)

            appl_node = ApplNode(name_node_ref, abstraction_ref)
            appl_ref = self.graph.add_node(appl_node)

            return appl_ref

    def definition(self):
        name_node_ref = self.name()
        abstraction_ref = self.abstraction(name_node_ref)
        abstraction_node = self.graph.get_node(abstraction_ref)

        fun_name_node = abstraction_node
        while not isinstance(fun_name_node, IdNode):
            fun_name_node = fun_name_node.lhs
            fun_name_node = self.graph.get_node(fun_name_node)

        self.graph.root.definitions[fun_name_node.value] = abstraction_ref

        if self.lexer.lookahead().type == TokenType.DEF.name:
            self.advance()
            self.definition()

    def abstraction(self, name_node_ref):

        if self.lexer.lookahead() == TokenType.EOF.name:
            return name_node_ref

        if self.match(TokenType.EQ):
            expr_ref = self.expr()

            abstr_node = AbstrNode(name_node_ref, expr_ref)
            abstr_node_ref = self.graph.add_node(abstr_node)
            return abstr_node_ref
        else:
            if self.lexer.lookahead().type == TokenType.EOF.name:
                return name_node_ref

            right_expression_ref = self.name()
            arg_node = ArgNode(name_node_ref, right_expression_ref)
            arg_node_ref = self.graph.add_node(arg_node)
            abstraction_ref = self.abstraction(arg_node_ref)

        assert isinstance(abstraction_ref, Ref)
        return abstraction_ref

    def expr(self):
        cond_node_ref = self.condexpr()
        expr1_node_ref = self.expr1()

        if expr1_node_ref is None:
            return cond_node_ref
        elif isinstance(self.graph.get_node(expr1_node_ref), WhereNode):
            where_node = self.graph.get_node(expr1_node_ref)
            where_node.bdy = cond_node_ref
            return expr1_node_ref

    def expr1(self):

        if self.match(TokenType.WHERE):
            where_dict = {}
            defs_node_ref = self.defs(where_dict)
            expr_node = self.expr1()
            if expr_node is None:
                where_node = WhereNode(defs_node_ref, where_dict)
                where_ref = self.graph.add_node(where_node)
                return where_ref

        else:
            return None

    def condexpr(self):
        if self.match(TokenType.IF):
            if_expr_node_ref = self.expr()
            assert isinstance(if_expr_node_ref, Ref)
            if self.require(TokenType.THEN):
                then_condexpr_node_ref = self.condexpr()
                assert isinstance(then_condexpr_node_ref, Ref)
                if self.require(TokenType.ELSE):

                    cond_node = CondNode()
                    cond_node_ref = self.graph.add_node(cond_node)

                    condexpr_ref = self.condexpr()
                    condexpr_node = self.graph.get_node(condexpr_ref)

                    appl_node_if = ApplNode(cond_node_ref, if_expr_node_ref)
                    appl_if_ref = self.graph.add_node(appl_node_if)

                    appl_node_then = ApplNode(appl_if_ref, then_condexpr_node_ref)
                    appl_ref_then = self.graph.add_node(appl_node_then)

                    if condexpr_node.type != TokenType.WHERE.name:
                        appl_node_result = ApplNode(appl_ref_then, condexpr_ref)
                        appl_ref_result = self.graph.add_node(appl_node_result)
                        assert isinstance(appl_ref_result, Ref)
                        return appl_ref_result

                    else:

                        condexpr_bdy_ref = condexpr_node.bdy

                        appl4_node = ApplNode(appl_ref_then, condexpr_bdy_ref)
                        appl4_ref = self.graph.add_node(appl4_node)

                        condexpr_node.bdy = appl4_ref

                        return condexpr_ref

        else:
            result_node_ref = self.listexpr()
            return result_node_ref

    def listexpr(self):
        op_node_ref = self.opexpr()
        list_node_ref = self.listexpr1()

        if list_node_ref is None:
            return op_node_ref
        else:
            list_node = self.graph.get_node(list_node_ref)
            if list_node.type == TokenType.WHERE.name:

                where_bdy_ref = list_node.bdy

                colon_node = ColonNode()
                colon_ref = self.graph.add_node(colon_node)

                appl1 = ApplNode(colon_ref, op_node_ref)
                appl1_ref = self.graph.add_node(appl1)

                appl2 = ApplNode(appl1_ref, where_bdy_ref)
                appl2_ref = self.graph.add_node(appl2)

                list_node.bdy = appl2_ref

                return list_node_ref

            else:
                colon_node = ColonNode()
                colon_ref = self.graph.add_node(colon_node)

                appl3_node = ApplNode(colon_ref, op_node_ref)
                appl3_ref = self.graph.add_node(appl3_node)

                return appl3_ref

    def listexpr1(self):
        if self.match(TokenType.COLON):
            expr_node_ref = self.expr()
            assert isinstance(expr_node_ref, Ref)
            return expr_node_ref
        else:
            return None

    def opexpr(self):
        conjunct_node_ref = self.conjunct()
        opexpr1_node_ref = self.opexpr1(conjunct_node_ref)
        return opexpr1_node_ref

    def opexpr1(self, conjunct_ref):
        if self.match(TokenType.OR):
            conjunct1_ref = self.conjunct()

            or_node = ORNode()
            or_node_ref = self.graph.add_node(or_node)

            appl1_node = ApplNode(or_node_ref, conjunct_ref)
            appl1_node.ref = self.graph.add_node(appl1_node)

            appl2_node = ApplNode(appl1_node.ref, conjunct1_ref)
            appl2_ref = self.graph.add_node(appl2_node)

            result_ref = self.opexpr1(appl2_ref)
        else:
            return conjunct_ref

        return result_ref

    def conjunct(self):
        compar_node_ref = self.compar()
        assert isinstance(compar_node_ref, Ref)
        conjunct1_node_ref = self.conjunct1(compar_node_ref)
        return conjunct1_node_ref

    def conjunct1(self, conjunct_node_ref):
        if self.match(TokenType.AND):
            compar_ref = self.compar()
            and_node = ANDNode()
            and_node_ref = self.graph.add_node(and_node)

            appl_node1 = ApplNode(and_node_ref, conjunct_node_ref)
            appl_node1_ref = self.graph.add_node(appl_node1)

            appl_node2 = ApplNode(appl_node1_ref, compar_ref)
            appl_node2_ref = self.graph.add_node(appl_node2)

            result_ref = self.conjunct1(appl_node2_ref)

        else:
            assert isinstance(conjunct_node_ref, Ref)

            return conjunct_node_ref

        return result_ref

    def compar(self):
        add_node_ref = self.add()
        compar1_node_ref = self.compar1(add_node_ref)
        assert isinstance(compar1_node_ref, Ref)
        return compar1_node_ref

    def compar1(self, compar_node_ref):
        if self.relop_helper(self.lexer.lookahead()):
            relop_node_ref = self.relop()
            assert isinstance(relop_node_ref, Ref)
            add_node_ref = self.add()
            assert isinstance(add_node_ref, Ref)
            appl_node1 = ApplNode(relop_node_ref, compar_node_ref)
            appl_node1_ref = self.graph.add_node(appl_node1)

            appl_node_result = ApplNode(appl_node1_ref, add_node_ref)
            appl_node_result_ref = self.graph.add_node(appl_node_result)

            assert isinstance(appl_node_result_ref, Ref)
            return self.compar1(appl_node_result_ref)

        else:
            assert isinstance(compar_node_ref, Ref)

            return compar_node_ref

    def add(self):
        mul_node_ref = self.mul()
        assert isinstance(mul_node_ref, Ref)
        add1_node_ref = self.add1(mul_node_ref)
        assert isinstance(add1_node_ref, Ref)
        return add1_node_ref

    def add1(self, mul_node_ref):
        if self.addop_helper(self.lexer.lookahead()):
            addop_node_ref = self.addop()
            add1_mul_node_ref = self.mul()

            appl_node1 = ApplNode(addop_node_ref, mul_node_ref)
            appl_node1_ref = self.graph.add_node(appl_node1)

            appl_node2 = ApplNode(appl_node1_ref, add1_mul_node_ref)
            appl_node2_ref = self.graph.add_node(appl_node2)

            assert isinstance(appl_node2_ref, Ref)
            return self.add1(appl_node2_ref)

        else:
            assert isinstance(mul_node_ref, Ref)
            return mul_node_ref

    def mul(self):
        factor_node_ref = self.factor()
        assert isinstance(factor_node_ref, Ref)
        mul1_node_ref = self.mul1(factor_node_ref)
        assert isinstance(mul1_node_ref, Ref)
        return mul1_node_ref

    def mul1(self, factor_node_ref):
        if self.mulop_helper(self.lexer.lookahead()):
            mulop_node_ref = self.mulop()
            assert isinstance(mulop_node_ref, Ref)
            factor1_node_ref = self.factor()
            assert isinstance(factor_node_ref, Ref)
            appl_node = ApplNode(mulop_node_ref, factor_node_ref)
            appl_node_ref = self.graph.add_node(appl_node)

            appl_node_result = ApplNode(appl_node_ref, factor1_node_ref)
            appl_node_result_ref = self.graph.add_node(appl_node_result)
            assert isinstance(appl_node_result_ref, Ref)

            return self.mul1(appl_node_result_ref)

        else:
            return factor_node_ref

    def factor(self):
        if self.prefix_helper(self.lexer.lookahead()):
            prefix_node_ref = self.prefix()
            prefix_node = self.graph.get_node(prefix_node_ref)
            assert isinstance(prefix_node_ref, Ref)

            if isinstance(prefix_node, NotNode):
                comb_node_ref = self.comb()
                assert isinstance(comb_node_ref, Ref)
                appl1_node = ApplNode(prefix_node_ref, comb_node_ref)
                appl1_node_ref = self.graph.add_node(appl1_node)
                assert isinstance(appl1_node_ref, Ref)
                return appl1_node_ref
            else:
                num_node_0 = NumNode(0)
                num_node_0_ref = self.graph.add_node(num_node_0)
                assert isinstance(num_node_0_ref, Ref)
                appl2_node = ApplNode(prefix_node_ref, num_node_0_ref)
                appl2_node_ref = self.graph.add_node(appl2_node)
                comb_node_ref = self.comb()
                assert isinstance(comb_node_ref, Ref)
                appl3_node = ApplNode(appl2_node_ref, comb_node_ref)
                appl3_node_ref = self.graph.add_node(appl3_node)
                assert isinstance(appl3_node_ref, Ref)
                return appl3_node_ref

        else:
            comb_node_ref = self.comb()
            assert isinstance(comb_node_ref, Ref)
            return comb_node_ref

    def comb(self):
        sim_ref = self.simple()
        assert isinstance(sim_ref, Ref)
        comb1_ref = self.comb1(sim_ref)
        assert isinstance(comb1_ref, Ref)
        return comb1_ref

    def comb1(self, sim_ref_left):
        if self.simple_helper(self.lexer.lookahead()):
            sim_ref_right = self.simple()
            appl_node = ApplNode(sim_ref_left, sim_ref_right)
            appl_ref = self.graph.add_node(appl_node)

            return self.comb1(appl_ref)
        else:
            assert isinstance(sim_ref_left, Ref)
            return sim_ref_left

    def simple(self) -> Ref:

        token = self.lexer.lookahead()

        if self.builtin_helper(token):
            result_ref = self.builtin()
            assert isinstance(result_ref, Ref)
        elif token.type == "ID":
            result_ref = self.name()
            assert isinstance(result_ref, Ref)
        elif self.constant_helper(token):
            result_ref = self.constant()
            assert isinstance(result_ref, Ref)
        elif token.type == "OPEN":
            self.advance()
            expr_ref = self.expr()
            if self.lexer.lookahead().type != "CLOSE":
                sys.exit(
                    "CLOSE expected but" + str(self.lexer.lookahead().type) + "received"
                )
            else:
                self.advance()
                result_ref = expr_ref
                assert isinstance(result_ref, Ref)

        assert isinstance(result_ref, Ref)
        return result_ref

    def name(self):
        id_node_reference = self.id()
        assert isinstance(id_node_reference, Ref)
        return id_node_reference

    def builtin(self):
        if self.match(TokenType.HD):
            result_node = HDNode()
            result_ref = self.graph.add_node(result_node)

        elif self.match(TokenType.TL):
            result_node = TLNode()
            result_ref = self.graph.add_node(result_node)

        assert isinstance(result_ref, Ref)
        return result_ref

    def constant(self) -> Ref:

        token = self.lexer.lookahead()

        match token.type:
            case "NUMBER":
                result_ref = self.num()
            case "TRUE":
                result_ref = self.bool()
            case "FALSE":
                result_ref = self.bool()
            case "NIL":
                nil_node = NilNode()
                result_ref = self.graph.add_node(nil_node)
                self.advance()
            case "SQOPEN":
                result_ref = self.list()
            case _:
                sys.exit("constant expected but" + str(token.type) + "received")

        return result_ref

    def list(self):
        if self.require(TokenType.SQOPEN):
            list1_ref = self.list1()
            return list1_ref

    def list1(self):
        if self.match(TokenType.SQCLOSE):
            nil_node = NilNode()
            nil_ref = self.graph.add_node(nil_node)
            return nil_ref
        else:
            listelems_ref = self.listelems()
            if self.require(TokenType.SQCLOSE):
                return listelems_ref

    def listelems(self):
        expr_ref = self.expr()

        colon_node = ColonNode()
        colon_node_ref = self.graph.add_node(colon_node)

        appl_node = ApplNode(colon_node_ref, expr_ref)
        appl_ref = self.graph.add_node(appl_node)

        listelemens1_ref = self.listelems1()

        appl_result_node = ApplNode(appl_ref, listelemens1_ref)
        appl_result_ref = self.graph.add_node(appl_result_node)

        return appl_result_ref

    def listelems1(self):
        if self.match(TokenType.COMMA):
            expr_ref = self.expr()

            colon_node = ColonNode()
            colon_node_ref = self.graph.add_node(colon_node)

            appl_node = ApplNode(colon_node_ref, expr_ref)
            appl_ref = self.graph.add_node(appl_node)

            listelemens1_ref = self.listelems1()

            appl_result_node = ApplNode(appl_ref, listelemens1_ref)
            appl_result_ref = self.graph.add_node(appl_result_node)

            return appl_result_ref

        else:
            nil_node = NilNode()
            nil_node_ref = self.graph.add_node(nil_node)
            return nil_node_ref

    def prefix(self):

        current_token_type = self.lexer.lookahead().type
        match current_token_type:
            case TokenType.PLUS.name:
                plus_node = PlusNode()
                result_ref = self.graph.add_node(plus_node)
                self.advance()
                return result_ref
            case TokenType.MINUS.name:
                minus_node = MinusNode()
                result_ref = self.graph.add_node(minus_node)
                self.advance()
                return result_ref
            case TokenType.NOT.name:
                not_node = NotNode()
                result_ref = self.graph.add_node(not_node)
                self.advance()
                return result_ref

    def addop(self):

        if self.match(TokenType.PLUS):
            plus_node = PlusNode()
            result_ref = self.graph.add_node(plus_node)
        elif self.require(TokenType.MINUS):
            minus_node = MinusNode()
            result_ref = self.graph.add_node(minus_node)

        return result_ref

    def mulop(self):

        if self.match(TokenType.MULTIPLY):
            mul_node = MulNode()
            result_ref = self.graph.add_node(mul_node)
        elif self.require(TokenType.DIVIDE):
            div_node = DivNode()
            result_ref = self.graph.add_node(div_node)

        return result_ref

    def relop(self):
        relop_node = self.lexer.lookahead()
        self.advance()

        match relop_node.type:
            case TokenType.LTEQ.name:
                lteq_node = LTEQNode()
                result_ref = self.graph.add_node(lteq_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case TokenType.GTEQ.name:
                gteq_node = GTEQNode()
                result_ref = self.graph.add_node(gteq_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case TokenType.LT.name:
                lt_node = LTNode()
                result_ref = self.graph.add_node(lt_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case TokenType.GT.name:
                gt_node = GTNode()
                result_ref = self.graph.add_node(gt_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case TokenType.NEQ.name:
                neq_node = NEQNode()
                result_ref = self.graph.add_node(neq_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case TokenType.EQ.name:
                eq_node = EQNode()
                result_ref = self.graph.add_node(eq_node)
                assert isinstance(result_ref, Ref)
                return result_ref
            case _:
                sys.exit("relop expected but" + str(relop_node.type) + "received")

    # atomic values

    def id(self) -> Ref:
        token = self.lexer.lookahead()
        id_node = IdNode(token.get_value())
        ref_id_node = self.graph.add_node(id_node)
        self.advance()
        assert isinstance(ref_id_node, Ref)
        return ref_id_node

    def num(self) -> Ref:
        token = self.lexer.lookahead()
        num_node = NumNode(int(token.get_value()))
        ref_num_node = self.graph.add_node(num_node)
        self.advance()
        assert isinstance(ref_num_node, Ref)
        return ref_num_node

    def bool(self) -> Ref:
        token = self.lexer.lookahead()
        bool_node = BoolNode(token.get_value())
        ref_bool_node = self.graph.add_node(bool_node)
        self.advance()
        assert isinstance(ref_bool_node, Ref)
        return ref_bool_node

    def string(self) -> Ref:
        token = self.lexer.lookahead()
        string_node = StringNode(token.get_value())
        ref_string_node = self.graph.add_node(string_node)
        self.advance()
        assert isinstance(ref_string_node, Ref)
        return ref_string_node

    ####helper functions

    def mulop_helper(self, token) -> bool:
        return (
            token.type == TokenType.MULTIPLY.name or token.type == TokenType.DIVIDE.name
        )

    def addop_helper(self, token) -> bool:
        return token.type == TokenType.PLUS.name or token.type == TokenType.MINUS.name

    def relop_helper(self, token) -> bool:
        return (
            token.type == TokenType.LTEQ.name
            or token.type == TokenType.GTEQ.name
            or token.type == TokenType.LT.name
            or token.type == TokenType.GT.name
            or token.type == TokenType.NEQ.name
            or token.type == TokenType.EQ.name
        )

    def simple_helper(self, token) -> bool:
        return (
            token.type == TokenType.ID.name  # <name>
            or self.builtin_helper(token)  # <builtin>
            or self.constant_helper(token)  # <constant>
            or token.type == TokenType.OPEN.name  # (
        )

    def builtin_helper(self, token) -> bool:

        return token.type == TokenType.HD.name or token.type == TokenType.TL.name

    def boolop_helper(self, token) -> bool:
        return token.type == TokenType.TRUE.name or token.type == TokenType.FALSE.name

    def constant_helper(self, token) -> bool:
        return (
            token.type == TokenType.NUMBER.name
            or self.boolop_helper(token)
            or token.type == TokenType.STRING.name
            or token.type == TokenType.NIL.name
            or token.type == TokenType.SQOPEN.name
        )

    def prefix_helper(self, token) -> bool:
        return (
            token.type == TokenType.MINUS.name
            or token.type == TokenType.PLUS.name
            or token.type == TokenType.NOT.name
        )
