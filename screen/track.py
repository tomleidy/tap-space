"""Track class contained within"""
from blessed import Terminal
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, GOAL_UPPER, GOAL_LOWER

term = Terminal()

# I just realized a vertical track is going to require changes in Message
# to display adjacent to the track. But that's a problem for later.

PIPE_GOAL_UPPER_LOWER = f"{regular}|{reverse}{TRACK_CHARACTER}{regular}|{term.normal}"
PIPE_GOAL_MIDDLE = f"{regular}>{reverse}{TRACK_CHARACTER}{regular}<{term.normal}"


class Track:
    """Prepare screen and print track for racer to run on"""

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
        """Calculate and return coordinates of goal position"""
        # add code to modify the y coordinate if difficulty is impossible
        if self.shape == "hyphen":
            return (term.width // 2, term.height // 2)
        elif self.shape == "pipe":
            return (term.width // 2, (term.height - 2) // 2)

    def get_track_start(self):
        """Calculate and return beginning of track"""
        if self.shape == "hyphen":
            return (0, term.height // 2)
        elif self.shape == "pipe":
            # y = 2? leave a gap below the titlebar
            return (term.width // 2, 2)

    def get_track_end(self):
        """Calculate and return ending of track"""
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
            start = self.get_track_start()
            start_x = start[0]
            start_y = start[1]
            end_y = self.get_track_end()[1]
            for position in range(start_y, end_y, 1):
                positions[position] = {"x": start_x, "y": position}
        # print(positions)
        self.track_positions = positions

    def print_track_pipe(self):
        """Print vertical track in middle of terminal"""
        track_x = self.get_track_start()[0]
        goal_y = self.get_goal()[1]
        print(
            term.move_xy(track_x-1, goal_y - 1) + PIPE_GOAL_UPPER_LOWER
        )
        print(term.move_xy(track_x-1, goal_y) + PIPE_GOAL_MIDDLE)
        print(term.move_xy(track_x-1,
              goal_y + 1) + PIPE_GOAL_UPPER_LOWER)
        for row in range(self.get_track_start()[1], self.get_track_end()[1], 1):
            print(term.move_xy(track_x, row) + reverse + ' ' + term.normal)

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
