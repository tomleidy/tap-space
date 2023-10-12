"""Functions that send messages to the screen"""
import sys
import time
from constants.terminal_colors import regular, reverse
from screen.locations import message_row, term


class Message:
    def __init__(self):
        self.last_updated = time.time()
        self.message = ""

    def send_endgame(self, message):
        """Print last message of game before quitting"""
        with term.hidden_cursor():
            print(term.move_y(message_row) + term.normal + term.center(message))
        sys.exit()

    def send(self, message):
        """Print message to message row"""
        self.message = message
        self.last_updated = time.time()
        with term.hidden_cursor():
            print(term.move_y(message_row) + regular +
                  term.center(message) + reverse)

    def refresh(self):
        """Refresh the message banner in case time has expired"""
        if self.message != "" and time.time() - self.last_updated >= 1.0:
            self.clear()

    def clear(self):
        """Clear message from message row"""
        self.message = ""
        with term.hidden_cursor():
            print(term.move_y(message_row) +
                  term.normal + term.center("") + reverse)
