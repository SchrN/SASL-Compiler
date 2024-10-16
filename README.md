# SASL-Compiler

#
A Compiler for the rudimentary functional programming language SASL(St Andrews Static Language).
Made in collaboration with Cato Kurtz.

## Eckdaten
- _Studenten:_ [Cato Kurtz & Nico Schreiner](mailto:Cato%20Kurtz%20<cato.kurtz@student.uni-tuebingen.de>,%20Nico%20Schreiner%20<nico.schreiner@student.uni-tuebingen.de>?&subject=[Teamprojekt])
- _Sprache:_ `Python`

## Verwendung Compiler
* Navigate to this directory: cd ../SASL-ss22-timfi

* Create a virtual environment with the SASL package:
```
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .
```

* (If you want to use the dot-graph feature, install graphviz: sudo apt install graphviz)

* Switch to the "Driver" directory: cd SASL/Driver

* Run the driver with: python Driver.py -p <sasl-path> [--lex] [--pars] [--comp] or Driver.py -e <sasl-expr> [--lex] [--pars] [--comp]

With --lex, the tokens from the lexer will be printed in the command line.

With --pars, the parser graph will be created as a dot graph (pars-graph.gv and pars-graph.png).

With --comp, the reduction graph will be created as a dot graph (comp-graph.gv and comp-graph.png).


## Nützliche Links
* [Handout](docs/handout_ss22.pdf)
* [SASL Prelude](SASL_test_files/prelude.sasl)
* [Beispiel Compiler](demo)
