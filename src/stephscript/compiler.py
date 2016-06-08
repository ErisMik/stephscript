"""
StephScript Compiler
"""

from ast import *
from stephscript.parser import *
from stephscript.tokenizer import *


class Compiler:
    """
    Controls logic flow of compilation
    """
    def __init__(self):
        self.tok = Tokenizer()
        self.prs = Parser()

    def compile(self, source):
        """ Compiles the Lines of code """
        modu = self.parse(self.tokenize(source))

        fix_missing_locations(modu)
        print("Compiled, starting execution\n-------------------\n")
        exec(compile(modu, filename="<ast>", mode="exec"))

    def parse(self, tokens):
        """ Parses the Lines of code """
        return self.prs.parse(tokens)

    def tokenize(self, filename):
        """ Converts the lines of code into tokens """
        return self.tok.tokenize(filename)
