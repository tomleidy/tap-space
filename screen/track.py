
from screen.locations import row_track, column_goal, term
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, GOAL_UPPER, GOAL_LOWER

# I just realized a vertical track is going to require changes in Message
# to display adjacent to the track. But that's a problem for later.

class Track:
    def __init__(self, shape="line"):
        self.shape = shape
        self.track = {}
        self.virtual_track()
        self.length = len(self.track)
        self.screen_clear()
        self.print_goals()
        self.print_track()

    def get_track(self):
        """Return self.track, allow other classes to know the track positions"""
        return self.track

    def screen_clear(self):
        """Clear the screen in preparation for track"""
        print(term.home + term.clear)
        
    def virtual_track(self):
        """Create object with x,y coordinates for each place on the track, and update state"""
        positions = {}
        if self.shape == "line":
            start = 0
            end = term.width
            row = term.width // 2
            for position in range(start, end, 1):
                positions[position] = {"x": position, "y": row }
        self.track = positions

    def print_goals(self):
        """Print goal posts"""
        if self.shape == "line":
            print(regular)
            print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
            print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)

    def print_track(self):
        """Print track in terminal"""
        if self.shape == "line":
            print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
            print(term.move_xy(0, row_track) + TRACK_CHARACTER*term.width)

