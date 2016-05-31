""" The main parsing file for the programming language, StephScript """
__author__ = "Eric M."


import sys


TRUE = "???"
FALSE = "???"
TRUFAL = [TRUE, FALSE]

def print_error(message, line_address):
    if line_address == -1:
        print "error:", message
    else:
        print "error:", message, "at line", line_address + 1

class Parser:

    def parse(self, input_lines):
        return

    def main(self):
        input_lines = []

        for line in sys.stdin:
            stripped_line = line.lstrip()
            if len(stripped_line) == 0:  # Empty Line
                input_lines.append("")
            else:
                if stripped_line[0] == "#":  # Commented line
                    input_lines.append("")
                else:
                    input_lines.append(stripped_line)
        self.parse(input_lines)

if __name__ == "__main__":
    Parser().main()
