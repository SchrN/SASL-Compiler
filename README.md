# Teamprojekt: **SASL**

## Eckdaten
- _Betreuer:_ [Tim Fischer](mailto:Tim%20Fischer%20<tim.fischer@uni-tuebingen.de>?&subject=[Teamprojekt])
- _Studenten:_ [Cato Kurtz & Nico Schreiner](mailto:Cato%20Kurtz%20<cato.kurtz@student.uni-tuebingen.de>,%20Nico%20Schreiner%20<nico.schreiner@student.uni-tuebingen.de>?&subject=[Teamprojekt])
- _Sprache:_ `Python`

## Verwendung Compiler
* navigiere in dieses Verzeichnis:
`cd ../SASL-ss22-timfi`

* erstelle ein virtual environment mit dem SASL-Paket:
```
python3.10 -m venv .venv
source .venv/bin/activate
pip install -e .
```

* (wenn du das dot-graph-feature verwenden willst, istalliere graphviz:
`sudo apt install graphviz`)

* wechsle in das Verzeichnis "Driver":
`cd SASL/Driver`

* rufe den Driver auf mit:
`python Driver.py -p <sasl-path> [--lex] [--pars] [--comp]`
oder
`Driver.py -e <sasl-expr> [--lex] [--pars] [--comp]`

mit `--lex` werden die Tokens aus dem Lexer mit in die Kommandozeile geprintet

mit `--pars` wird der Parser-Graph als dot-graph (pars-graph.gv und pars-graph.png) erstellt

mit `--comp` wird der Reduction-Graph als dot-graph (comp-graph.gv und comp-graph.png) erstellt


## Nützliche Links
* [Handout](docs/handout_ss22.pdf)
* [SASL Prelude](SASL_test_files/prelude.sasl)
* [Beispiel Compiler](demo)
