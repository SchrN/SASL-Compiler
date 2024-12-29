# SASL-Compiler

#
A Compiler for the rudimentary functional programming language [SASL](https://en.wikipedia.org/wiki/SASL_(programming_language)).
Made in collaboration with Cato Kurtz.

## Usage

* Create a virtual environment with the SASL package:
```
python3.10 -m venv .venv
pip install -e .
```

* (If you want to use the dot-graph feature, install graphviz: sudo apt install graphviz)

* Switch to the "Driver" directory: cd SASL/Driver

* Run the driver with: python Driver.py -p <sasl-path> [--lex] [--pars] [--comp] or Driver.py -e <sasl-expr> [--lex] [--pars] [--comp]

With --lex, the tokens from the lexer will be printed in the command line.

With --pars, the parser graph will be created as a dot graph (pars-graph.gv and pars-graph.png).

With --comp, the reduction graph will be created as a dot graph (comp-graph.gv and comp-graph.png).

Example:

python Driver.py -e 4+4 --lex

