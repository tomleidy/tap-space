
# from screen.locations import row_track, column_goal, term
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, GOAL_UPPER, GOAL_LOWER

from blessed import Terminal
term = Terminal()

# I just realized a vertical track is going to require changes in Message
# to display adjacent to the track. But that's a problem for later.

col_track = term.width // 2
row_goal = (term.height - 2) // 2
PIPE_TRACK_START_ROW = 3  # to accommodate the titlebar+1
pipe_col_goal_left = col_track - 1
pipe_col_goal_right = col_track + 1
PIPE_TRACK_STRING = f"{reverse} {term.normal}"

PIPE_GOAL_UPPER_LOWER = f"{regular}|{reverse}{TRACK_CHARACTER}{regular}|{term.normal}"
PIPE_GOAL_MIDDLE = f"{regular}>{reverse}{TRACK_CHARACTER}{regular}<{term.normal}"


class Track:
    def __init__(self, shape):
        self.shape = shape
        self.track_positions = {}
        self.virtual_track()
        self.screen_clear()
        self.print_goals()
        if self.shape == "pipe":
            self.print_track_pipe()
        elif self.shape == "hyphen":
            self.print_track_hyphen()

    def get_track(self):
        """Return self.track_positions, allow other classes to know the track positions"""
        return self.track_positions

    def get_goal(self):
        if self.shape == "hyphen":
            return (term.width // 2, term.height // 2)
        elif self.shape == "pipe":
            return (term.width // 2, (term.height - 2) // 2)

    def get_track_start(self):
        if self.shape == "hyphen":
            return (0, term.height // 2)
        elif self.shape == "pipe":
            return (term.width // 2, 3)

    def get_track_end(self):
        if self.shape == "hyphen":
            return (term.width, term.height // 2)
        elif self.shape == "pipe":
            return (term.width // 2, term.height-1)

    def screen_clear(self):
        """Clear the screen in preparation for track"""
        print(term.home + term.normal + term.clear)

    def virtual_track(self):
        """Create object with x,y coordinates for each place on the track, and update state"""
        positions = {}
        goal_xy = self.get_goal()
        if self.shape == "hyphen":
            start = 0
            end = term.width
            for position in range(start, end, 1):
                positions[position] = {"x": position, "y": goal_xy[1]}
        elif self.shape == "pipe":
            start = PIPE_TRACK_START_ROW
            end = term.height-1
            col = term.width // 2
            for position in range(start, end, 1):
                positions[position] = {"x": col, "y": position}
        # print(positions)
        self.track_positions = positions

    def print_track_pipe(self):
        """Print vertical track in middle of terminal"""
        print(term.move_xy(pipe_col_goal_left,
              row_goal - 1) + PIPE_GOAL_UPPER_LOWER)
        print(term.move_xy(pipe_col_goal_left, row_goal) + PIPE_GOAL_MIDDLE)
        print(term.move_xy(pipe_col_goal_left,
              row_goal + 1) + PIPE_GOAL_UPPER_LOWER)
        for row in range(PIPE_TRACK_START_ROW, term.height, 1):
            print(term.move_xy(col_track, row) + reverse + ' ' + term.normal)

    def print_goals(self):
        """Print goal posts"""
        goal_xy = self.get_goal()
        if self.shape == "hyphen":

            print(regular)
            print(term.move_xy(goal_xy[0] - 1, goal_xy[1] - 1) + GOAL_UPPER)
            print(term.move_xy(goal_xy[0] - 1, goal_xy[1] + 1) + GOAL_LOWER)

    def print_track_hyphen(self):
        """Print track in terminal"""
        goal_xy = self.get_goal()
        if self.shape == "hyphen":
            # print(reverse + term.move_xy(0,row_track) + TRACK_CHARACTER)
            print(reverse + term.move_xy(0, goal_xy[1]) +
                  term.center(TRACK_CHARACTER))


def get_track_ends(track):
    min_x = -1
    max_x = -1
    min_y = -1
    max_y = -1
    for position in track.values():
        if min_x == -1 or position["x"] < min_x:
            min_x = position["x"]
        if position["x"] > max_x:
            max_x = position["x"]
        if min_y == -1 or position["y"] < min_y:
            min_y = position["y"]
        if position["y"] > max_y:
            max_y = position["y"]
    return {"min": (min_x, min_y), "max": (max_x, max_y)}
