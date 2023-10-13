"""Track class contained within"""
import random
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

    def __init__(self, shape, difficulty):
        self.shape = shape
        self.difficulty = difficulty
        self.track_positions = {}
        self.virtual_track()
        self.screen_clear()
        if self.shape == "pipe":
            self.print_goal_pipe()
            self.print_track_pipe()
        elif self.shape == "hyphen":
            self.print_goals_hyphen()
            self.print_track_hyphen()

    def get_track(self):
        """Return self.track_positions, allow other classes to know the track positions"""
        return self.track_positions

    def get_goal_center(self):
        """Calculate and return coordinates of goal position"""
        # add code to modify the y coordinate if difficulty is impossible
        x_pos = 0
        y_pos = 0
        if self.shape == "hyphen":
            x_pos = term.width // 2
            y_pos = term.height // 2
            if self.difficulty == 5:
                y_pos += random.choice([3])
        elif self.shape == "pipe":
            x_pos = term.width // 2
            y_pos = (term.height - 2) // 2
            if self.difficulty == 5:
                x_pos += random.choice([3, -3])
        return (x_pos, y_pos)

    def get_goal_tuple(self):
        """Get ful list of positions for goal, including non-center, for clearing track."""
        positions = []
        if self.shape == "hyphen":
            # row above: x-1, x, x+1
            # row below: x-1, x, x+1
            pos_x = term.width // 2
            pos_y = term.height // 2
            positions.append((pos_x, pos_y))
            positions.append((pos_x, pos_y-1))
            positions.append((pos_x-1, pos_y-1))
            positions.append((pos_x+1, pos_y-1))
            positions.append((pos_x, pos_y+1))
            positions.append((pos_x-1, pos_y+1))
            positions.append((pos_x+1, pos_y+1))
        elif self.shape == "pipe":
            # column left: y-1, y, y+1
            # column right: y-1, y, y+1
            pos_x = term.width // 2
            pos_y = (term.height - 2) // 2
            positions.append((pos_x, pos_y))
            positions.append((pos_x-1, pos_y))
            positions.append((pos_x-1, pos_y-1))
            positions.append((pos_x-1, pos_y+1))
            positions.append((pos_x+1, pos_y))
            positions.append((pos_x+1, pos_y-1))
            positions.append((pos_x+1, pos_y+1))
        return tuple(positions)

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
        positions = []
        start_x, start_y = self.get_track_start()
        end_x, end_y = self.get_track_end()
        if self.shape == "hyphen":
            start = 0
            end = term.width
            for position in range(start, end, 1):
                positions.append((position, start_y))
        elif self.shape == "pipe":
            start_x, start_y = self.get_track_start()
            end_y = self.get_track_end()[1]
            for position in range(start_y, end_y, 1):
                positions.append((start_x, position))
        self.track_positions = positions

    def print_goal_pipe(self):
        """Print goals around where 'center' is"""
        goal_x, goal_y = self.get_goal_center()
        print(term.move_xy(goal_x-1, goal_y-1) + PIPE_GOAL_UPPER_LOWER)
        print(term.move_xy(goal_x-1, goal_y) + PIPE_GOAL_MIDDLE)
        print(term.move_xy(goal_x-1, goal_y+1) + PIPE_GOAL_UPPER_LOWER)

    def print_track_pipe(self):
        """Print vertical track in middle of terminal"""
        start_x, start_y = self.get_track_start()
        end_x, end_y = self.get_track_end()
        for row in range(start_y, end_y, 1):
            print(term.move_xy(start_x, row) + f"{reverse} {term.normal}")

    def wipe_track_normal(self):
        """Clear the track, returning it to normal terminal"""
        print(term.normal)
        for position in self.get_goal_tuple():
            print(term.move_xy(*position) + " ")
        for position in self.track_positions:
            print(term.move_xy(*position) + " ")
        print(term.move_xy(0, term.height-3))

    def print_goals_hyphen(self):
        """Print goal posts"""
        goal_x, goal_y = self.get_goal_center()
        print(regular)
        print(term.move_xy(goal_x-1, goal_y-1) + GOAL_UPPER)
        print(term.move_xy(goal_x-1, goal_y+1) + GOAL_LOWER)
        print(reverse)
        print(term.move_xy(goal_x-1, goal_y) + "   ")

    def print_track_hyphen(self):
        """Print track in terminal"""
        track_x, track_y = self.get_track_start()
        if self.shape == "hyphen":
            # print(reverse + term.move_xy(0,row_track) + TRACK_CHARACTER)
            print(reverse + term.move_xy(0, track_y) +
                  term.center(TRACK_CHARACTER))
