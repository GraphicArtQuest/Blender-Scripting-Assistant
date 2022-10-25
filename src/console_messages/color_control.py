""" Color controller for terminal debugging.

This module provides standardized terminal escape sequences that correspond to
colored text when printing to the terminal. This allows a debugging programmer
to more easily separate the output and see what is going on.

For accessibility for the color blind, users can disable this feature and print
only black and white to the console.
"""

class ConsoleColors:
    """Provides standardized colors to use as escape codes in the terminal."""
    def __init__(self):
        self.enable()

    def disable(self):
        self.CONTROL = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
        
    def enable(self):
        self.CONTROL = '\033[35m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'

color = ConsoleColors()