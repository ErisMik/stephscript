""" The main parsing file for the programming language, StephScript """
__author__ = "Eric M."


import sys
import os
import subprocess
import platform
import shlex

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
            stripped_line = line
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
        if not bwall:
            print_rant("When did the Berlin Wall occur?", -1)
            # return
        passes["berlin wall"] = bwall

        # CODE MUST BE WRITTEN IN ALL CAPS BECAUSE STEPH LIKES TO SHOUT
        allcap = False
        lower_letter = [c for c in input_lines if c.islower()]
        if len(lower_letter) == 0:
            allcap = True
        if not allcap:
            print_rant("COULD YOU SPEAK UP? I CANT HEAR YOU!", -1)
            # return
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
        if john:
            print_rant("Why did you mention him?", -1)
            # return
        passes["john"] = not john

        # Stephscript can only be run on a computer with less than 5gb of space remaining...
        space = False
        command = "df | awk '/Available/{getline; print $4}'"
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out = proc.communicate()
        if out[:-2] <= 5:
            space = True
        if not space:
            print_rant("It's a little too spacious on this HDD", -1)
            # return
        passes["low space"] = space

        # ...and the computer is NOT running the latest version of it's OS
        # TODO: TEST WHAT SYSTEM IT'S ON
        version = True
        data = platform.mac_ver()
        if "10.11.4" in data[0]:
            version = False
        if not version:
            print_rant("Where did my dashboard go?", -1)
            # return
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
        if not directory:
            print_rant("I don't like it here, I'm leaving", -1)
            # return
        passes["desktop"] = directory

        # Verify that it passes, for programmer benifit only
        # TODO: Delete this and uncomment the returns on the errors
        self.verify(passes)

    def verify(self, pass_dict):
        for key in pass_dict:
            print key, ":", pass_dict[key]

# ############################################
# Parser Class
class Parser:
    keywords = {
        "NOPE" : "None",
        "WRONG" : "False",
        "RIGHT" : "True",
        "GET THE FUCK OUT" : "break",
        "WHEN DID" : "def",
        "WILL THIS WORK" : "if",
        "SHIT I'LL TRY THIS" : "elif",
        "FUCK MY LIFE" : "else",
        "COULD YOU PLEASE" : "try",
        "WELL SHIT" : "except",
        "BETTER FUCKING NOT BE" : "not",
        "AND" : "and",
        "I DON'T CARE" : "or",
        "OCCUR" : "return",
        "HEY" : "print",
        "IS" : "=",
        "REALLY IS" : "==",
        "ADD" : "+",
        "MINUS" : "-",
        "MULTI" : "*",
        "DIVIDE" : "/",
        "WORSE" : "<",
        "BETTER" : ">",

        "WHILE" : "while",
        "FOR" : "for"
    }

    goodwords = [
        "ERIC",
        "PETER",
        "STEPH"
    ]

    specialchars = [
        ":",
        "(",
        ")"
    ]

    def parse(self, input_lines):
        output_lines = []
        for line in input_lines:
            oline = ""

            leading_space = len(line) - len(line.lstrip())
            if leading_space > 0:
                num = leading_space
                space = " " * num
                oline = oline + space
            line = shlex.shlex(line)

            skip = True
            for word in line:
                if skip:
                    skip = False
                else:
                    oline += " "

                if word in self.keywords:  # If it's an operator (single word operator)
                    oline += self.keywords[word]
                elif self.test_multiline(word)[0]:  # If it's a operator (multiword operator)
                    oline += self.keywords[self.test_multiline(word)[1]]
                elif word in self.goodwords:  # If it's a variable
                    oline += word
                elif word in self.specialchars:  # If it's a special character
                    oline += word
                elif word.isdigit():  # If it's a number TODO: ONLY DOES ints MUST DO ALL NUMBERS
                    oline += word
                elif word[0] == "\"" and word[-1] == "\"":  # If the word is a string value
                    oline += word
                else:
                    skip = True

            output_lines.append(oline)

        for line in output_lines:
            print line

    def test_multiline(self, input_word):
        for kword in self.keywords:
            kword = kword.split()
            if input_word in kword[0]:
                return (True, " ".join(kword))
        return (False, None)

# ############################################
# Main Method
def main():
    code_lines = []

    for line in sys.stdin:
        code_lines.append(line)

    code_lines = Filter().filter(code_lines)  # Filter the lines
    Rule_Checker().check(code_lines) # Check if follows all the rules
    print "#" * 50
    Parser().parse(code_lines) # Parse Code
    # Execute Code

if __name__ == "__main__":
    main()
