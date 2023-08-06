import sys


class Logger:
    """
    :type _instance Logger
    """
    _instance = None

    def __init__(self):
        self._prefix = ''
        Logger._instance = self

    @staticmethod
    def log(text):
        Logger._instance._log(text)

    @staticmethod
    def err(text):
        Logger._instance._err(text)

    @staticmethod
    def prefix(prefix):
        Logger._instance._prefix = prefix

    def _log(self, text):
        for line in text.split('\n'):
            sys.stdout.write(self._prefix + line + '\n')

    def _err(self, text):
        for line in text.split('\n'):
            sys.stderr.write(self._prefix + line + '\n')
