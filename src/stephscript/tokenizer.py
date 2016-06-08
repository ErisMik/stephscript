"""
StephScript Tokenizer
"""

import re

from stephscript.allowed_words import ALLOWED
from stephscript.constants import *
from stephscript.disallowed_words import DISALLOWED
from stephscript.utils import Utils

class Tokenizer:
    @staticmethod
    def toke(token_type, token_value, line) -> dict:
        """
        Create a mapping for the given token
        :param token_type: the type of the token
        :param token_value: The token's value
        :param line: The line number for this token
        :return: A mapping of the properties to their values
        """
        return {"type": token_type, "value": token_value, "line": line}

    @staticmethod
    def tokenize(filename):
        """
        Tokenize the given file
        :param filename:
        :return: The tokens in the file
        """

        tokens = Tokenizer._first_pass(filename)
        tokens = Tokenizer._second_pass(tokens)

        return tokens

    @staticmethod
    def _first_pass(filename) -> list:
        """
        Tokenize the given file
        :param filename: the file to tokenize
        :return: The tokens in the file
        """

        end_word = re.compile("[:!,;\.\s\?]")

        with open(filename, 'r') as src:
            data = src.read().lower()
            tokens = []
            line = 1
            i = 0
            while i < len(data):

                c = data[i]

                # Spaces, newlines, and periods
                if c.isspace() or c == ".":
                    if c == "\n":
                        line += 1
                    pass

                # Operators (special symbol form) and punctuation
                elif c == "+":
                    tokens.append(Tokenizer.toke(T_Plus, None, line))
                elif c == "-":
                    tokens.append(Tokenizer.toke(T_Minus, None, line))
                elif c == "*":
                    tokens.append(Tokenizer.toke(T_Times, None, line))
                elif c == "/":
                    tokens.append(Tokenizer.toke(T_Over, None, line))
                elif c == "<":
                    tokens.append(Tokenizer.toke(T_Less, None, line))
                elif c == ">":
                    tokens.append(Tokenizer.toke(T_Greater, None, line))

                # Closures and precedence
                elif c == ",":
                    tokens.append(Tokenizer.toke(T_LParen, None, line))
                elif c == ";":
                    tokens.append(Tokenizer.toke(T_RParen, None, line))
                elif c == ":":
                    tokens.append(Tokenizer.toke(T_LBrace, None, line))
                elif c == "!":
                    tokens.append(Tokenizer.toke(T_RBrace, None, line))

                # Don't forget question marks
                elif c == "?":
                    tokens.append(Tokenizer.toke(T_Question, None, line))

                # Integers (no floating point)
                elif c.isdigit():
                    num = ""
                    while data[i].isdigit():
                        num += data[i]
                        i += 1
                    else:
                        tokens.append(Tokenizer.toke(T_Num, int(num), line))
                    i -= 1  # Read one char too many, readjust.

                # Words and keywords
                elif c.isalpha():
                    word = ""
                    while i < len(data) and (data[i].isalpha() or data[i] == "'"):
                        word += data[i]
                        i += 1
                    if i < len(data) and not end_word.match(data[i]):
                        Tokenizer._rant(line, 'nonword')
                    i -= 1  # Read one char too many, readjust.

                    # Keywords
                    if word == "is":
                        tokens.append(Tokenizer.toke(T_Is, None, line))
                    elif word == "will":
                        tokens.append(Tokenizer.toke(T_If, None, line))
                    elif word == "fuck":
                        tokens.append(Tokenizer.toke(T_Else, None, line))
                    elif word == "right":
                        tokens.append(Tokenizer.toke(T_True, None, line))
                    elif word == "wrong":
                        tokens.append(Tokenizer.toke(T_False, None, line))
                    elif word == "best":
                        tokens.append(Tokenizer.toke(T_Not, None, line))
                    elif word == "and":
                        tokens.append(Tokenizer.toke(T_And, None, line))
                    elif word == "i":
                        tokens.append(Tokenizer.toke(T_Or, None, line))
                    # elif word == "MAKE":
                    #     tokens.append(Tokenizer.toke(T_Make, None, line))
                    elif word == "hey":
                        tokens.append(Tokenizer.toke(T_Print, None, line))

                    # English form of the operators
                    elif word == "add":
                        tokens.append(Tokenizer.toke(T_Plus, None, line))
                    elif word == "minus":
                        tokens.append(Tokenizer.toke(T_Minus, None, line))
                    elif word == "multi":
                        tokens.append(Tokenizer.toke(T_Times, None, line))
                    elif word == "divide":
                        tokens.append(Tokenizer.toke(T_Over, None, line))
                    elif word == "worse":
                        tokens.append(Tokenizer.toke(T_Less, None, line))
                    elif word == "better":
                        tokens.append(Tokenizer.toke(T_Greater, None, line))

                    # Otherwise, it's just a word, interpreting is the lexer's job
                    else:
                        tokens.append(Tokenizer.toke(T_Word, word, line))

                # Strings
                elif c == '"':
                    i += 1
                    quote = ""
                    while data[i] != '"':
                        quote += data[i]
                        i += 1
                        if i >= len(data):
                            Tokenizer._rant(line, 'unterminated_quote')
                            pass
                    tokens.append(Tokenizer.toke(T_Quote, quote, line))

                else:
                    pass
                    Tokenizer._rant(line, 'nonword')
                i += 1
            return tokens

    @staticmethod
    def _second_pass(tokens):
        """
        Makes the second pass for tokenization purposes
        :param tokens: The tokens on which we're taking a second pass
        :return: The tokens after the second pass
        """

        # Make sure we do "America is great"
        if not Tokenizer._check_for_wall(tokens):
            Tokenizer._rant(tokens[-1]['line'], 'wall occur')

        # Convert "as long as" to while
        tokens = Tokenizer._combine_whiles(tokens)

        # Ensure words are English
        Tokenizer._ensure_rules(tokens)

        return tokens

    @staticmethod
    def _is_word_allowed(word) -> bool:
        """
        Check to see if a given word is allowed
        :param word: Word to check and see if it's allowed
        :return: true if the word is valid, false otherwise
        """

        # First, make sure we haven't explicitly banned the word
        if word in DISALLOWED:
            return False

        # Now see if it's an allowed word
        return word in ALLOWED

    @staticmethod
    def _ensure_rules(tokens) -> None:
        """
        Make sure all the variables are in our list of allowed words
        :param tokens: the tokens to filter
        :return: None, throws error upon infraction of rule
        """

        for token in tokens:
            if token['type'] == T_Word and not Tokenizer._is_word_allowed(token['value']):
                print(token['value'] + "?")
                Tokenizer._rant(token['line'], 'nonword')

    @staticmethod
    def _combine_whiles(tokens) -> list:
        """
        Combine the words "as long as" to make a while token
        :param tokens: The tokens to combine on
        :return: The tokens with
        """

        combine_at = []

        for idx in range(len(tokens)):
            if tokens[idx]['type'] == T_Word and tokens[idx]['value'] == 'as' and idx + 2 < len(tokens):
                if (tokens[idx + 1]['type'] == T_Word and tokens[idx + 1]['value'] == 'long') and (
                                tokens[idx + 2]['type'] == T_Word and tokens[idx + 2]['value'] == 'as'):
                    combine_at.append(idx)

        # Cover the degenerate case like "as long as long as"
        non_overlapping = []
        for value in combine_at:
            if value - 2 not in non_overlapping:
                non_overlapping.append(value)

        # Now combine the tokens and return
        for idx in reversed(non_overlapping):
            line = tokens[idx]['line']
            for dummy in range(3):
                tokens.pop(idx)

            tokens.insert(idx, Tokenizer.toke(T_While, None, line))

        return tokens

    @staticmethod
    def _check_for_wall(tokens) -> bool:
        """
        Make sure that in the tokens passed,
        the last two are tokens representing the phrase "Berlin Wall"
        :param tokens: The tokens to verify
        :return: True if the check holds, false otherwise
        """

        last_two = tokens[-2:]
        if len(last_two) != 2:
            return False

        # Tokens for "Berlin Wall"
        expected = [Tokenizer.toke(T_Word, 'berlin', 0),
                    Tokenizer.toke(T_Word, 'wall', 0)]

        # Make sure our types and values match each of the expected
        for idx in range(2):
            if expected[idx]['type'] != last_two[idx]['type'] or expected[idx]['value'] != last_two[idx]['value']:
                return False

        for idx in range(2):
            tokens.pop()

        return True

    @staticmethod
    def _rant(line, message_code) -> None:
        """
        Prints the error message and then aborts the program
        :param line: The line the error occurred on
        :param message_code: String code associated with the error message
        :return: None
        """

        print("Parsing error:")
        print("What are you doing on line " + str(line) + "?")
        raise Utils.SystemRant(message_code)
