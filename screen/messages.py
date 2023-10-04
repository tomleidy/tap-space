"""Functions that send messages to the screen"""
import sys
import time
from constants.terminal_colors import regular, reverse
from screen.locations import message_row, term


class Message:
    def __init__(self):
        self.last_updated = time.time()

    def send_endgame(self, message):
        """Print last message of game before quitting"""
        print(term.move_y(message_row) + term.normal + term.center(message))
        sys.exit()

    def send(self, message):
        """Print message to message row"""
        self.last_updated = time.time()
        print(term.move_y(message_row) + regular + term.center(message) + reverse)

    def refresh(self):
        if time.time() - self.last_updated >= 1.0:
            self.clear()

    def clear(self):
        """Clear message from message row"""
        print(term.move_y(message_row) + term.normal + term.center("") + reverse)
