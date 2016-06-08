"""
StephScript Constants
"""

# Token constants
T_End = -1

T_Plus = 0
T_Minus = 1
T_Times = 2
T_Over = 3
T_Less = 4
T_Greater = 5

T_LParen = 10
T_RParen = 11
T_LBrace = 12
T_RBrace = 13

T_Is = 20
T_If = 21
T_Else = 22

T_True = 30
T_False = 31
T_And = 32
T_Or = 33
T_Not = 34

T_Word = 40
T_Num = 41
T_Quote = 42

T_Make = 50
T_Question = 51
T_Print = 52
T_While = 53

# Error messages
ERROR_CODES = {
    # For quotes that didn't get terminated
    'unterminated_quote': ["NO! Don't stop, I want to hear more!"],
    # If they try to use a word that isn't listed
    'nonword': ["I literally have no idea what you're talking about"],
    # If they try to use a word that we've explicitly banned
    'badword': ["R00d. No need to mention that"],
    # Generic errors for when we're lazy
    'default': ["It's literally broken and I don't know why"],
    # If they try to run on the incorrect os version
    'os ver': ["Hey, where did my dashboard go?"],
    # If the computer has too much free space
    'hdd': ["It's a little too spacious in here don't you think?"],
    # If StephScript isn't being run on the desktop
    'location': ["I don't like it here, lets leave"]
}
