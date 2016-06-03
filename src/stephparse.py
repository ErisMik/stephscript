""" The main parsing file for the programming language, StephScript """
__author__ = "Eric M."


import sys
import os
import subprocess
import platform

TRUE = "???"
FALSE = "???"
TRUFAL = [TRUE, FALSE]

# ############################################
# Universal Functions
def print_rant(message, line_address):
    if line_address == -1:
        print "rant:", message, "/rant"
    else:
        print "rant:", message, "at line", line_address + 1, "/rant"

# ############################################
# Filter Class
class Filter:
    def filter(self, input_lines):
        output_lines = []
        for line in input_lines:
            stripped_line = line.lstrip()
            if len(stripped_line) == 0:  # Empty Line
                output_lines.append("")
            else:
                if stripped_line[0] == "#":  # Commented line
                    output_lines.append("")
                else:
                    output_lines.append(stripped_line)
        return output_lines

# ############################################
# Rule Checker
class Rule_Checker:
    def check(self, input_lines):
        passes = {}

        # "Berlin Wall" must occur at some time during the program
        bwall = False
        for line in input_lines:
            if "berlin wall" in line.lower():
                bwall = True
                break
            else:
                bwall = False
        passes["berlin wall"] = bwall

        # CODE MUST BE WRITTEN IN ALL CAPS BECAUSE STEPH LIKES TO SHOUT
        allcap = False
        lower_letter = [c for c in input_lines if c.islower()]
        if len(lower_letter) == 0:
            allcap = True
        passes["allcaps"] = allcap

        # Mentioning Aesthetics causes the program to run faster than usual
        aest = False
        for line in input_lines:
            if "aesthetics" in line.lower():
                aest = True
                break
            else:
                aest = False
        passes["aesthetics"] = aest

        # Stephscript will not compile if John is mentioned anywhere
        john = False
        for line in input_lines:
            if "john" in line.lower():
                john = True
                break
            else:
                john = False
        passes["john"] = not john

        # Stephscript can only be run on a computer with less than 5gb of space remaining...
        space = False
        command = "df | awk '/Available/{getline; print $4}'"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out = p.communicate()
        if out[:-2] <= 5:
            space = True
        passes["low space"] = space

        # ...and the computer is NOT running the latest version of it's OS
        # TODO: TEST WHAT SYSTEM IT'S ON
        version = True
        data = platform.mac_ver()
        if "10.11.4" in data[0]:
            version = False
        passes["os ver"] = version

        # The device must NOT be flat/level for Stephscript to run (If available)
        #TODO: everything for this

        # Stephscript must be run from the Desktop, or else it deletes itself
        #TODO: Actually Delete itself
        directory = False
        cur_dir = os.getcwd()
        cur_dir = cur_dir.split("/")
        if cur_dir[-1] == "Desktop":
            directory = True
        passes["desktop"] = directory

        # Verify that it passes, throw errors and close if it doesn't
        self.verify(passes)

    def verify(self, pass_dict):
        for key in pass_dict:
            print key, ":", pass_dict[key]

# ############################################
# Parser Class
class Parser:
    def parse(self, input_lines):
        return

# ############################################
# Main Method
def main():
    code_lines = []

    for line in sys.stdin:
        code_lines.append(line)
        print "test :_:", line

    code_lines = Filter().filter(code_lines)  # Filter the lines
    Rule_Checker().check(code_lines) # Check if follows all the rules
    # Parse Code
    # Execute Code

if __name__ == "__main__":
    main()
