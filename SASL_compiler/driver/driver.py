# Driver for SASL Compiler by Cato Kurtz and Nico Schreiner
# call with python Driver.py -p <sasl-path> [--lex] [--pars] [--comp]
# or
#  Driver.py -e <sasl-expr> [--lex] [--pars] [--comp]
from SASL.Lexer.Lexer import *
from SASL.Parser.Parser import *
from SASL.Compiler.Compiler import *
from SASL.Reduction_Machine.Reduction_Machine import *
import os
import argparse

# create argument parser
arg_parser = argparse.ArgumentParser(description="compile a given SASL expression")
arg_parser.add_argument(
    "--sasl_path",
    "-p",
    type=str,
    help="path to a .sasl file",
)
arg_parser.add_argument(
    "--sasl_expr",
    "-e",
    type=str,
    help="a valid expression in SASL",
)
arg_parser.add_argument("--lex", help="print Lexer output", action="store_true")
arg_parser.add_argument(
    "--pars", help="make dot-graph of Parse-Tree", action="store_true"
)
arg_parser.add_argument(
    "--comp", help="make dot-graph of Compiler-Tree", action="store_true"
)

args = arg_parser.parse_args()


def compile_from_expr(expr, l: bool = False, p: bool = False, c: bool = False):

    lex = Lexer(expr)
    lex.get_tokens()
    if l:
        for elem in lex.list_tokens:
            print(elem)

    pars = Parser()
    pars.lexer = lex
    pars.create_graph()
    if p:
        pars.graph.make_dot_graph(pars.graph.root, "pars-graph.gv")
        os.system("dot -Tpng pars-graph.gv -o pars-graph.png")

    comp = Compiler()
    comp.r_graph = Reduction_Graph()
    comp.ast = pars.graph
    comp.create_graph()
    if c:
        comp.r_graph.make_dot_graph(comp.r_graph.root, "comp-graph.gv")
        os.system("dot -Tpng comp-graph.gv -o comp-graph.png")

    red = Reduction_Machine(comp.r_graph)
    return red.reduction()


def compile_from_path(path, l: bool = False, p: bool = False, c: bool = False):

    with open(path, "r") as data:
        sasl_code = data.read()

        return compile_from_expr(sasl_code, l, p, c)


def main():
    try:
        compile_from_path(args.sasl_path, args.lex, args.pars, args.comp)
    except:
        compile_from_expr(args.sasl_expr, args.lex, args.pars, args.comp)


if __name__ == "__main__":
    main()
