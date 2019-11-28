from pycparser import c_parser, c_ast
# import argparse

with open("butts.c") as fr:
    text = fr.read()
    parser = c_parser.CParser()
    ast = parser.parse(text, filename='butts.c')
    ast.show(showcoord=True)
