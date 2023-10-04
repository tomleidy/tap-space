"""Functions that send messages to the screen"""
import sys
from blessed import Terminal
from constants.terminal_colors import regular, reverse
from screen.locations import message_row

term = Terminal()

def message_send_endgame(message):
    """Print last message of game before quitting"""
    print(term.move_y(message_row) + term.normal + term.center(message))
    sys.exit()

def message_send(message):
    """Print message to message row"""
    print(term.move_y(message_row) + regular + term.center(message) + reverse)

def message_row_clear():
    """Clear message from message row"""
    print(term.move_y(message_row) + term.normal + term.center("") + reverse)
