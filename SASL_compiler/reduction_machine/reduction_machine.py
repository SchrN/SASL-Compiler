import sys

from SASL.AST.Graph import *
from SASL.Reduction_Graph.Reduction_Nodes import *


class Reduction_Machine:
    def __init__(self, graph):
        self.graph: Graph() = graph
        self.leftAncestorsStack = (
            []
        )  # push = append, pop = pop(0) , list[-1] top of stack

    def print_left_ancestor_stack(self):  # for test purposes
        if self.leftAncestorsStack:
            for ref in self.leftAncestorsStack:
                if isinstance(ref, Ref):
                    print(self.graph.get_node(ref))

    def reduction(self, first=1):
        if first == 1:
            self.leftAncestorsStack.append(
                self.graph.root.bdy
            )  # 1  #puts ref to root of bdy

        while True:

            actual_node_ref = self.leftAncestorsStack[-1]
            actual_node = self.graph.get_node(actual_node_ref)

            if isinstance(actual_node, Ref):
                actual_node = self.graph.get_node(actual_node)
            if isinstance(actual_node, ApplNode):
                self.leftAncestorsStack.append(
                    actual_node.lhs
                )  # puts reference to left child in dict
            elif isinstance(actual_node, Combinator):
                self.leftAncestorsStack.pop()
                self.combinator(actual_node)
            elif isinstance(
                actual_node, BuiltIn
            ):  # create class Builtin in Nodes nodes
                self.leftAncestorsStack.pop()
                self.builtin(actual_node)
            elif isinstance(actual_node, PairNode):
                result_list = []
                self.reduce_pair(actual_node, result_list)
                print(result_list)
                return result_list
            else:
                print(actual_node.value)
                return actual_node.value

    def reduce_pair(self, actual_node, result_list: list):

        if (
            (isinstance(actual_node, BoolNode))
            or isinstance(actual_node, NumNode)
            or isinstance(actual_node, INode)
        ):
            result_list.append(actual_node.value)

        if hasattr(actual_node, "lhs"):
            if actual_node.lhs is not None:
                self.reduce_pair(self.graph.dict[actual_node.lhs.ref], result_list)

        if hasattr(actual_node, "rhs"):
            if actual_node.rhs is not None:
                self.reduce_pair(self.graph.dict[actual_node.rhs.ref], result_list)

    def combinator(self, node):
        match node:
            case SNode():
                self.s()
            case KNode():
                self.k()
            case INode():
                self.i()
            case YNode():
                self.y()
            case UNode():
                self.u()

    def s(self):

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)
        f_ref = top_node.rhs

        top2_ref = self.leftAncestorsStack.pop()
        top2_node = self.graph.get_node(top2_ref)

        if isinstance(top2_node, Ref):
            top2_node = self.graph.get_node(top2_node)
        g_ref = top2_node.rhs

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        x_ref = root_node.rhs

        applgx = ApplNode(g_ref, x_ref)
        applgx_ref = self.graph.add_node(applgx)

        applfx = ApplNode(f_ref, x_ref)
        applfx_ref = self.graph.add_node(applfx)

        root_node.lhs = applfx_ref
        root_node.rhs = applgx_ref

    def k(self):

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)
        x = top_node.rhs

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        root_node.rhs = x
        root_node.lhs = i_node_ref

    def i(self):

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)

        x = self.graph.get_node(top_node.rhs)
        x_ref = self.graph.add_node(x)

        self.leftAncestorsStack.append(x_ref)

    def y(self):

        # @1 (f @1)
        top_ref = self.leftAncestorsStack[-1]
        top_node = self.graph.get_node(top_ref)

        f_ref = top_node.rhs

        top_node.lhs = f_ref

        top_node.rhs = top_ref

    def u(self):

        f_ref = self.leftAncestorsStack.pop()
        f_node = self.graph.get_node(f_ref)
        f_right_ref = f_node.rhs

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        z_ref = root_node.rhs

        # @( hd z )

        hd_node = HDNode()
        hd_node_ref = self.graph.add_node(hd_node)

        appl1_node = ApplNode(hd_node_ref, z_ref)
        appl1_ref = self.graph.add_node(appl1_node)

        # @ (f appl1)

        appl2_node = ApplNode(f_right_ref, appl1_ref)
        appl2_ref = self.graph.add_node(appl2_node)

        # @ (tl z)
        tl_node = TLNode()
        tl_node_ref = self.graph.add_node(tl_node)

        appl3_node = ApplNode(tl_node_ref, z_ref)
        appl3_ref = self.graph.add_node(appl3_node)

        root_node.lhs = appl2_ref
        root_node.rhs = appl3_ref

    def builtin(self, node):  # complete nodes

        match node:
            case PlusNode():
                self.reduce_binary(node)
            case MinusNode():
                self.reduce_binary(node)
            case DivNode():
                self.reduce_binary(node)
            case MulNode():
                self.reduce_binary(node)
            case ColonNode():
                self.reduce_colon(node)
            case CondNode():
                self.reduce_conditional(node)
            case LTEQNode():
                self.reduce_binary(node)
            case GTEQNode():
                self.reduce_binary(node)
            case LTNode():
                self.reduce_binary(node)
            case GTNode():
                self.reduce_binary(node)
            case NEQNode():
                self.reduce_binary(node)
            case EQNode():
                self.reduce_binary(node)
            case ANDNode():
                self.reduce_binary(node)
            case ORNode():
                self.reduce_binary(node)
            case NotNode():
                self.reduce_not(node)
            case TLNode():
                self.reduce_tl(node)
            case HDNode():
                self.reduce_hd(node)

    def reduce_conditional(self, node):

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)

        condition_expression_ref = top_node.rhs

        self.leftAncestorsStack.append(condition_expression_ref)

        self.reduction(0)

        condition_result_ref = self.leftAncestorsStack.pop()
        condition_result_node = self.graph.get_node(condition_result_ref)

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)

        x_ref = top_node.rhs

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        y_ref = root_node.rhs

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        root_node.lhs = i_node_ref

        if isinstance(condition_result_node, BoolNode):
            root_node.rhs = x_ref
        else:
            root_node.rhs = y_ref

    def reduce_colon(self, node):

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)

        x_ref = top_node.rhs

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        y_ref = root_node.rhs

        pair_node = PairNode(x_ref, y_ref)
        pair_node_ref = self.graph.add_node(pair_node)

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        root_node.lhs = i_node_ref
        root_node.rhs = pair_node_ref

    def reduce_binary(self, op_node):  # op_node + - * /

        top_ref = self.leftAncestorsStack.pop()
        top_node = self.graph.get_node(top_ref)

        x_ref = top_node.rhs
        x_node = self.graph.get_node(x_ref)

        root_ref = self.leftAncestorsStack[-1]
        root_node = self.graph.get_node(root_ref)

        y_ref = root_node.rhs
        y_node = self.graph.get_node(y_ref)

        ## we wanna reduce x and reduce y to get numbers/value
        self.leftAncestorsStack.append(x_ref)

        if isinstance(x_node, BoolNode):
            pass
        else:
            self.reduction(0)

        x_ref_number = self.leftAncestorsStack.pop()
        x_node_number = self.graph.get_node(x_ref_number)
        x_value = x_node_number.value

        self.leftAncestorsStack.append(y_ref)
        if isinstance(y_node, BoolNode):
            pass
        else:
            self.reduction(0)

        y_ref_number = self.leftAncestorsStack.pop()
        y_node_number = self.graph.get_node(y_ref_number)
        y_value = y_node_number.value

        if (isinstance(y_node_number, NumNode)) and (
            isinstance(x_node_number, NumNode)
        ):
            i_node = INode()
            i_node_ref = self.graph.add_node(i_node)
            root_node.lhs = i_node_ref

            num_node = NumNode(0)
            num_node_ref = self.graph.add_node(num_node)
            bool_node = BoolNode("false")
            bool_node_ref = self.graph.add_node(bool_node)

            match op_node:
                case PlusNode():
                    num_node.value = float(x_value) + float(y_value)
                    root_node.rhs = num_node_ref
                case MinusNode():
                    num_node.value = float(x_value) - float(y_value)
                    root_node.rhs = num_node_ref
                case DivNode():
                    num_node.value = float(x_value) / float(y_value)
                    root_node.rhs = num_node_ref
                case MulNode():
                    num_node.value = float(x_value) * float(y_value)
                    root_node.rhs = num_node_ref

                case LTEQNode():
                    if x_value <= y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref
                case GTEQNode():
                    if x_value >= y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref
                case LTNode():
                    if x_value < y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref
                case GTNode():
                    if x_value > y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref
                case NEQNode():
                    if x_value != y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref
                case EQNode():
                    if x_value == y_value:
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                    root_node.rhs = bool_node_ref

        elif (isinstance(y_node_number, BoolNode)) and (
            isinstance(x_node_number, BoolNode)
        ):
            i_node = INode()
            i_node_ref = self.graph.add_node(i_node)
            root_node.lhs = i_node_ref

            bool_node = BoolNode("false")
            bool_node_ref = self.graph.add_node(bool_node)

            match op_node:
                case EQNode():
                    if x_value == y_value:
                        bool_node.value = "true"
                case NEQNode():
                    if x_value != y_value:
                        bool_node.value = "false"
                case ORNode():
                    if (x_value == "true") or (y_value == "true"):
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"
                case ANDNode():
                    if (x_value == "true") and (y_value == "true"):
                        bool_node.value = "true"
                    else:
                        bool_node.value = "false"

            root_node.rhs = bool_node_ref

    def reduce_not(self, node):

        top_ref = self.leftAncestorsStack[-1]
        top_node = self.graph.get_node(top_ref)

        x_ref = top_node.rhs
        x_node = self.graph.get_node(x_ref)

        self.leftAncestorsStack.append(x_ref)

        if isinstance(x_node, BoolNode):
            pass
        else:
            self.reduction(0)

        x_result_ref = self.leftAncestorsStack.pop()
        x_result_node = self.graph.get_node(x_result_ref)

        x_result_value = x_result_node.value
        if x_result_value == "true":
            x_result_value_neg = "false"
        elif x_result_value == "false":
            x_result_value_neg = "true"

        bool_node = BoolNode(x_result_value)

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        bool_result_node = BoolNode(x_result_value_neg)
        bool_result_ref = self.graph.add_node(bool_result_node)

        top_node.lhs = i_node_ref
        top_node.rhs = bool_result_ref

    def reduce_tl(self, node):

        top_ref = self.leftAncestorsStack[-1]
        top_node = self.graph.get_node(top_ref)

        top_node_rhs_ref = top_node.rhs
        top_node_rhs_node = self.graph.get_node(top_node_rhs_ref)

        self.leftAncestorsStack.append(top_node_rhs_ref)

        if isinstance(top_node_rhs_node, PairNode):
            pass
        else:
            self.reduction(0)

        result_list_ref = self.leftAncestorsStack.pop()
        result_list_node = self.graph.get_node(result_list_ref)

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        top_node.lhs = i_node_ref
        top_node.rhs = result_list_node.rhs

    def reduce_hd(self, node):

        top_ref = self.leftAncestorsStack[-1]
        top_node = self.graph.get_node(top_ref)

        top_node_rhs_ref = top_node.rhs
        top_node_rhs_node = self.graph.get_node(top_node_rhs_ref)

        self.leftAncestorsStack.append(top_node_rhs_ref)

        if isinstance(top_node_rhs_node, PairNode):
            pass
        else:
            self.reduction(0)

        result_list_ref = self.leftAncestorsStack.pop()
        result_list_node = self.graph.get_node(result_list_ref)

        i_node = INode()
        i_node_ref = self.graph.add_node(i_node)

        top_node.lhs = i_node_ref
        top_node.rhs = result_list_node.lhs
