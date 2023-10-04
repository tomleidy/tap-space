"""Variables indicating where things should be on the screen"""
from blessed import Terminal

term = Terminal()


row_track = term.height // 2
column_goal = term.width // 2
message_row = row_track - 5
