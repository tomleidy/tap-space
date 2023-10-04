
from screen.locations import row_track, column_goal, term
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, GOAL_UPPER, GOAL_LOWER

class Track:
    def __init__(self):
        self.screen_clear()
        self.print_goals()
        self.print_track()
    
    def screen_clear(self):
        print(term.home + term.clear)
    
    def print_goals(self):
        print(regular)
        print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
        print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)
        
    def print_track(self):
        print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
        print(term.move_xy(0, row_track) + TRACK_CHARACTER*term.width)
    
    