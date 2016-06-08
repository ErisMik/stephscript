"""
StephScript Utility Functions
"""

import locale
import platform
import os
import subprocess
import random
import sys

from stephscript.constants import ERROR_CODES

class Utils:
    class SystemRant(Exception):
        def __init__(self, msg_code) -> Exception:
            """
            Get the error from the error code and throw Exception
            :param msg_code: the code for the error
            :return: The new Exception
            """
            if msg_code in ERROR_CODES:
                Exception.__init__(self, "rant: "+random.choice(ERROR_CODES[msg_code])+" /rant")
            else:
                Exception.__init__(self, "rant: "+random.choice(ERROR_CODES['default'])+" /rant")

    @staticmethod
    def warn(str, *args) -> None:
        """
        Prints a warning to stderr with the specified format args
        :return:
        """
        print('WARNING: ' + (str % args), file=sys.stderr)

    @staticmethod
    def verify_system() -> None:
        """
        Verifies that this system is Trump-approved, throwing
        a SystemRant otherwise
        :return:
        """
        Utils.no_latest_version()
        Utils.no_empty_space()
        Utils.no_not_desktop()

    @staticmethod
    def no_latest_version() -> None:
        """
        Make sure the currently-running OS is not the latest version
        :return:
        """
        # TODO: Compatibility with more than just OSX
        data = platform.mac_ver()
        if "10.11.4" in data[0]:
            raise Utils.SystemRant("os ver")

    @staticmethod
    def no_empty_space() -> None:
        """
        Make sure the computer has little to no remaining space left on it
        :return:
        """
        command = "df | awk '/Available/{getline; print $4}'"
        proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        out = proc.communicate()
        if out[:-2] > 5:
            raise Utils.SystemRant("hdd")

    @staticmethod
    def no_not_desktop() -> None:
        """
        Make sure the program is being run from the desktop
        :return:
        """
        cur_dir = os.getcwd()
        cur_dir = cur_dir.split("/")
        if not cur_dir[-1] == "Desktop":
            raise Utils.SystemRant("location")
