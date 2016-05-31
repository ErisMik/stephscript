import locale
import os
import random
import sys

# yes, bringing in openssl is completely necessary for proper operation of trumpscript
import ssl

from stephscript.constants import ERROR_CODES

class Utils:
    class SystemException(Exception):
        def __init__(self, msg_code) -> Exception:
            """
            Get the error from the error code and throw Exception
            :param msg_code: the code for the error
            :return: The new Exception
            """
            if msg_code in ERROR_CODES:
                Exception.__init__(self, random.choice(ERROR_CODES[msg_code]))
            else:
                Exception.__init__(self, random.choice(ERROR_CODES['default']))

    @staticmethod
    def verify_system(warn=True) -> None:
        """
        Verifies that this system is Trump-approved, throwing
        a SystemException otherwise
        :return:
        """
        Utils.no_wimps()
        Utils.no_pc()
        Utils.no_commies_mexicans_or_kenyans(warn)

    @staticmethod
    def warn(str, *args) -> None:
        """
        Prints a warning to stderr with the specified format args
        :return:
        """
        print('WARNING: ' + (str % args), file=sys.stderr)

    @staticmethod
    def no_wimps() -> None:
        """
        Make sure we're not executing as root, because America is strong
        :return:
        """
        if os.geteuid() == 0:
            raise Utils.SystemException('root')

    @staticmethod
    def no_pc() -> None:
        """
        Make sure the currently-running OS is not Windows, because we're not PC
        :return:
        """
        if os.name == 'nt':
            raise Utils.SystemException('os');

    @staticmethod
    def no_commies_mexicans_or_kenyans(warn=True) -> None:
        """
        Make sure we aren't executing on a Chinese or Mexican system, because
        America has traditional values.
        If we have a Kenyan SSL root on our system, refuse to run entirely,
        because we can't have that, can we?
        :return:
        """
        loc = locale.getdefaultlocale()
        loc = loc[0].upper() if len(loc) > 0 else ''
        if 'CN' in loc:
            raise Utils.SystemException("We can't let China beat us!")
        elif 'MX' in loc:
            raise Utils.SystemException("I will build a great [fire]wall on our southern border.")

        # Warn if the system has any certificates from Chinese authorities.
        # If the system has any certificates from Kenyan authorities,
        # refuse to run entirely.
        ctx = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        ctx.load_default_certs()
        for cert in ctx.get_ca_certs():
            cn, commie = None, False
            issuer, serial = cert['issuer'], cert['serialNumber']
            for kv in issuer:
                # List of tuples containing PKCS#12 key/value tuples
                kv = kv[0]
                key, value = kv[0], kv[1]
                if key == 'countryName':
                    if value == 'CN':
                        commie = True
                    elif value == 'KE':
                        raise Utils.SystemException('ssl')
                elif key == 'commonName':
                    cn = value

            if commie and warn:
                Utils.warn("SSL certificate `%s` (serial: %s) was made by commies!", cn, serial)
