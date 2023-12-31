"""Terminal color settings"""
from blessed import Terminal
from constants.terminal_strings import RACER_CHARACTER

term = Terminal()

regular = term.on_color_rgb(40, 40, 40) + term.color_rgb(255, 169, 0)
reverse = term.color_rgb(40, 40, 40) + term.on_color_rgb(255, 169, 0)

track_string_vertical = f"{reverse}{RACER_CHARACTER}{regular}"