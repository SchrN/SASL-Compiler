from SASL.Lexer.Lexer import *
from SASL.AST.Graph import *
from SASL.AST.Nodes import *
from SASL.Parser.Parser import *
from SASL.Reduction_Graph.Reduction_Graph import *
from SASL.Reduction_Graph.Reduction_Nodes import *


class Compiler:
    parser: Parser
    ast: Graph
    lexer: Lexer
    r_graph: Reduction_Graph

    def appl_remodeling(self, n: ApplNode, g: Graph, var: str) -> Ref:  # tested
        assert isinstance(n, ApplNode)
        assert isinstance(var, str)
        assert isinstance(g, Graph)  # in what Graph is the given Node?
        # S@[x]f@[x]a

        s = SNode()
        s_ref = self.r_graph.add_node(s)

        lhs_ref = self.ski_remodeling(g.get_node(n.lhs), g, var)
        rhs_ref = self.ski_remodeling(g.get_node(n.rhs), g, var)
        at_1 = ApplNode(s_ref, lhs_ref)
        at_1_ref = self.r_graph.add_node(at_1)

        rhs_ref = self.ski_remodeling(g.get_node(n.rhs), g, var)
        at_2 = ApplNode(at_1_ref, rhs_ref)
        at_2_ref = self.r_graph.add_node(at_2)
        return at_2_ref

    # does n in g contain an Id-Node with value name?
    def contains(self, n: Node, name: str, g: Graph) -> bool:
        assert isinstance(n, Node)
        assert isinstance(name, str)
        assert isinstance(g, Graph)

        if isinstance(n, IdNode):
            assert hasattr(n, "value")
            if n.value == name:
                return True

        if hasattr(n, "lhs"):
            assert hasattr(n, "rhs")
            return self.contains(g.get_node(n.lhs), name, g) or self.contains(
                g.get_node(n.rhs), name, g
            )

        if hasattr(n, "bdy"):
            assert hasattr(n, "definitions")
            if self.contains(g.get_node(n.bdy), name, g):
                return True
            for index in n.definitions:
                if self.contains(g.get_node(n.definitions[index]), name, g):
                    return True
        else:
            return False

    def where_remodeling(self, n: WhereNode, variable_list: list) -> Ref:
        assert isinstance(n, WhereNode)
        assert isinstance(variable_list, list)

        if len(n.definitions) == 0:
            raise Exception("missing definition in where")
        if n.bdy == None:
            raise Exception("missing body for where")

        bdy_var_list = []
        e1_ref = self.transfer(self.ast.get_node(n.bdy), bdy_var_list)
        for var_ref in bdy_var_list:
            var = self.r_graph.get_node(var_ref)
            for name in n.definitions:
                # global def
                if not var.value == name:
                    variable_list.append(var_ref)

        def_num = len(n.definitions)

        # containing one def
        if def_num == 1:

            name = list(n.definitions)[0]  # name of the one def
            ref = list(n.definitions.values())[0]  # ref to the one def
            abstr_node = self.ast.get_node(ref)
            assert isinstance(abstr_node, AbstrNode)

            rev_arg_list = []
            rhs_ref = None

            e1_ref = self.ski_remodeling(
                self.r_graph.get_node(e1_ref), self.r_graph, name
            )  # [f]E1

            # E1 where f   = E2      -> ([f]E1) @           E2
            if isinstance(self.ast.get_node(abstr_node.lhs), IdNode):
                e2_ref = self.transfer(self.ast.get_node(abstr_node.rhs), variable_list)
                # no args -> vars in variable_list come from outside
                rhs_ref = e2_ref

            # E1 where f x = E2      -> ([f]E1) @       ([x]E2)
            elif isinstance(self.ast.get_node(abstr_node.lhs), ArgNode):
                self.get_reversed_arguments(
                    rev_arg_list, self.ast.get_node(abstr_node.lhs), self.ast
                )
                # create ref to the body of the def and then remodel it with ski
                xe2_ref = abstr_node.rhs

                arg_counter = 0
                for arg in rev_arg_list:
                    g = self.r_graph
                    if arg_counter < 1:
                        g = self.ast

                    node = g.get_node(xe2_ref)
                    xe2_ref = self.ski_remodeling(node, g, arg)  # [x]E2
                    arg_counter += 1
                assert xe2_ref.ref in self.r_graph.dict
                rhs_ref = xe2_ref

            # E1 where f x = ...f... -> ([f]E1) @ (Y@[f]([x]E2))
            # recursion (Y)
            if self.contains(self.ast.get_node(abstr_node.rhs), name, self.ast):
                y = YNode()
                y_ref = self.r_graph.add_node(y)

                rhs_ref = self.ski_remodeling(
                    self.r_graph.get_node(rhs_ref), self.r_graph, name
                )  # [f]rhs
                y_at = ApplNode(y_ref, rhs_ref)  # (Y@[f] rhs)
                y_at_ref = self.r_graph.add_node(y_at)

                rhs_ref = y_at_ref

            at = ApplNode(e1_ref, rhs_ref)
            at_ref = self.r_graph.add_node(at)
            return at_ref

        # multiple where definitions
        # E1 where f x = E2;
        #          g y = E3  -> U @ ([f](U @ [g](K @ E1))) @ [[x]E2,[y]E3]
        #                        at3      at2     at1      at  (at10-40)

        elif def_num > 1:
            # K @ E1
            k = KNode()
            k_ref = self.r_graph.add_node(k)
            at_1 = ApplNode(k_ref, e1_ref)
            at_1_ref = self.r_graph.add_node(at_1)
            at_2_ref = None

            counter = 1
            for name in reversed(n.definitions):
                if counter == 1:
                    # [g](K @ E1)
                    at_1_ref = self.ski_remodeling(at_1, self.r_graph, name)
                    at_2_ref = at_1_ref  # for loop

                    # ,[y]E3]
                    colon_1 = ColonNode()
                    colon_1_ref = self.r_graph.add_node(colon_1)
                    e3 = self.ast.get_node(n.definitions[name])
                    assert isinstance(e3, AbstrNode)
                    rev_e3_arg_list = []
                    self.get_reversed_arguments(
                        rev_e3_arg_list, self.ast.get_node(e3.lhs), self.ast
                    )
                    e3_var_list = []  # vars in body of e3
                    e3_ref = self.transfer(self.ast.get_node(e3.rhs), e3_var_list)
                    at_10 = ApplNode(colon_1_ref, e3_ref)
                    at_10_ref = self.r_graph.add_node(at_10)

                    for arg in rev_e3_arg_list:
                        at_10_ref = self.ski_remodeling(at_10, self.r_graph, arg)

                    nil = NilNode()
                    nil_ref = self.r_graph.add_node(nil)
                    at_20 = ApplNode(at_10_ref, nil_ref)
                    at_20_ref = self.r_graph.add_node(at_20)

                    counter += 1

                else:
                    assert at_2_ref != None
                    assert at_20_ref != None

                    u_1 = UNode()
                    u_1_ref = self.r_graph.add_node(u_1)
                    temp_at = ApplNode(u_1_ref, at_2_ref)
                    at_ref = self.r_graph.add_node(temp_at)
                    # [f](U @
                    at_ref = self.ski_remodeling(temp_at, self.r_graph, name)
                    at_2_ref = at_ref  # for loop

                    # [[x]E2
                    colon_2 = ColonNode()
                    colon_2_ref = self.r_graph.add_node(colon_2)
                    e2 = self.ast.get_node(n.definitions[name])
                    assert isinstance(e2, AbstrNode)
                    rev_e2_arg_list = []
                    self.get_reversed_arguments(
                        rev_e2_arg_list, self.ast.get_node(e2.lhs), self.ast
                    )
                    e2_var_list = []  # vars in body of e2
                    e2_ref = self.transfer(self.ast.get_node(e2.rhs), e2_var_list)
                    at_30 = ApplNode(colon_2_ref, e2_ref)
                    at_30_ref = self.r_graph.add_node(at_30)

                    for arg in rev_e2_arg_list:
                        at_30_ref = self.ski_remodeling(at_30, self.r_graph, arg)

                    at_40 = ApplNode(at_30_ref, at_20_ref)
                    at_40_ref = self.r_graph.add_node(at_40)
                    at_20_ref = at_40_ref  # for loop

            assert at_2_ref != None
            assert at_40_ref != None
            u_2 = UNode()
            u_2_ref = self.r_graph.add_node(u_2)
            at_3 = ApplNode(u_2_ref, at_2_ref)
            at_3_ref = self.r_graph.add_node(at_3)

            at = ApplNode(at_3_ref, at_40_ref)
            at_ref = self.r_graph.add_node(at)
            return at_ref

        else:
            raise (Exception("a where Node should contain at least one binding"))

    """takes a node and a var and remodels it (with all its child nodes) 
    with the SKI combinators,
    while also adding them all to the r_graph
    returns a ref to the remodeled node in the r_graph"""

    def ski_remodeling(self, n: Node, g: Graph, var: str) -> Ref:
        assert isinstance(n, Node)
        assert isinstance(var, str)
        assert isinstance(g, Graph)  # in what Graph is the given Node?

        if isinstance(g, Reduction_Graph):
            n_ref = Ref(n.idx)
        else:
            n_ref = self.r_graph.add_node(n)

        # function application; [x](f@a)
        if isinstance(n, ApplNode):
            return self.appl_remodeling(n, g, var)

        if isinstance(n, WhereNode):
            return self.where_remodeling(n, [])

        # variable; [x]var(v)
        elif isinstance(n, IdNode):
            if n.value == var:
                i = INode()
                i_ref = self.r_graph.add_node(i)
                return i_ref

            else:
                k = KNode()
                k_ref = self.r_graph.add_node(k)
                at = ApplNode(k_ref, n_ref)
                at_ref = self.r_graph.add_node(at)
                return at_ref
        # constant; [x]c
        else:
            k = KNode()
            k_ref = self.r_graph.add_node(k)
            at = ApplNode(k_ref, n_ref)
            at_ref = self.r_graph.add_node(at)
            return at_ref

    def create_graph(self):
        self.r_graph = Reduction_Graph()
        self.compile()

    def get_reversed_arguments(self, result: list, n: Node, g: Graph) -> list:  # tested
        assert isinstance(result, list)
        assert isinstance(n, Node)
        assert isinstance(g, Graph)

        if isinstance(n, IdNode):
            return
        elif isinstance(n, ArgNode):
            result.append(self.ast.get_node(n.rhs).value)
            self.get_reversed_arguments(result, self.ast.get_node(n.lhs), g)
        else:
            raise Exception("The given Node should be an Id or Argument Node")

    # transfer tree (after .) from ast to r_graph
    # also replace ast-refs in given list by new refs to r_graph
    # Id-Nodes stay for now, get replaced in a later step
    # root dict stays empty -> refs to remodeled defs we need get added later
    def transfer(self, n: Node, variable_list: list) -> Ref:
        assert isinstance(n, Node)
        n_ref = self.r_graph.add_node(n)

        if hasattr(n, "lhs"):
            assert hasattr(n, "rhs")
            n.lhs = self.transfer(self.ast.get_node(n.lhs), variable_list)
            n.rhs = self.transfer(self.ast.get_node(n.rhs), variable_list)
            return n_ref

        elif isinstance(n, WhereNode):
            return self.where_remodeling(n, variable_list)
        else:
            if isinstance(n, IdNode):
                variable_list.append(n_ref)

            return n_ref

    # check if a node (or any of its sub-nodes) in g
    # has variables that need to be replaced
    # vgl. contains
    def has_variables(self, n: Node, g: Graph) -> bool:
        assert isinstance(n, Node)

        if isinstance(n, IdNode):
            return True

        elif hasattr(n, "lhs"):
            assert hasattr(n, "rhs")
            return self.has_variables(g.get_node(n.lhs), g) or self.has_variables(
                g.get_node(n.rhs), g
            )
        elif hasattr(n, "bdy"):
            assert hasattr(n, "definitions")
            if self.has_variables(g.get_node(n.bdy), g):
                return True
            for index in n.definitions:
                if self.has_variables(g.get_node(n.definitions(index)), g):
                    return True
        else:
            return False

    # replace variable with ref to its definition
    def replace(self, var: IdNode, ref: Ref):
        self.r_graph.dict[var.idx] = self.r_graph.dict[ref.ref]

    def compile(self):
        if len(self.ast.dict) == None:
            return

        # no variables -> ast = r_graph
        if not self.has_variables(self.ast.get_node(self.ast.root.bdy), self.ast):
            self.r_graph = self.ast

        # some variables: remove occurences of user-defined names and variables
        else:
            # transform AST-body -> R-Graph-body
            # list to save refs to Id-Nodes (in r_graph!)
            variable_list = []
            self.r_graph.root.definitions = {}
            self.r_graph.root.bdy = self.transfer(
                self.ast.get_node(self.ast.root.bdy), variable_list
            )
            for var_ref in variable_list:
                var = self.r_graph.get_node(var_ref)
                name = var.value
                assert isinstance(var, IdNode)

                # has the definition for this var already been remodeled?
                if name in self.r_graph.root.definitions:
                    # replace var by ref to remodeled definition
                    self.replace(var, self.r_graph.root.definitions[name])

                # global definition in AST -> needs to be remodeled
                elif name in self.ast.root.definitions:
                    abstr_node = self.ast.get_node(self.ast.root.definitions[name])
                    assert isinstance(abstr_node, AbstrNode)
                    ref = abstr_node.rhs  # ref to body of def

                    if isinstance(self.ast.get_node(abstr_node.lhs), ArgNode):

                        # get list of arguments of def
                        rev_arg_list = []
                        self.get_reversed_arguments(
                            rev_arg_list, self.ast.get_node(abstr_node.lhs), self.ast
                        )

                        arg_counter = 0
                        for arg in rev_arg_list:
                            g = self.r_graph
                            if arg_counter < 1:
                                g = self.ast

                            node = g.get_node(ref)
                            ref = self.ski_remodeling(node, g, arg)
                            arg_counter += 1

                    else:
                        node = self.ast.get_node(ref)
                        ref = self.transfer(node, [])

                    if self.contains(self.r_graph.get_node(ref), name, self.r_graph):
                        y = YNode()
                        y_ref = self.r_graph.add_node(y)

                        ref = self.ski_remodeling(
                            self.r_graph.get_node(ref), self.r_graph, name
                        )  # [f]ref
                        y_at = ApplNode(y_ref, ref)  # (Y@[f] ref)
                        y_at_ref = self.r_graph.add_node(y_at)

                        ref = y_at_ref

                    assert ref.ref in self.r_graph.dict
                    self.r_graph.root.definitions[name] = ref
                    self.replace(var, self.r_graph.root.definitions[name])

                else:
                    Exception("{} is not defined".format(name))
