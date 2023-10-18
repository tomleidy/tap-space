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
    # TODO: refactor shapes into their own Shape / shape_name subclasses

    def __init__(self, shape, difficulty):
        self.shape = shape
        self.difficulty = difficulty
        self.track_positions = {}
        self.goal_slope = 1
        self.virtual_track()
        # self._screen_clear()
        self._print_shape()

    def _print_shape(self):
        if self.shape == "pipe":
            self.print_goal_pipe()
        elif self.shape == "hyphen":
            self.print_goals_hyphen()
        elif self.shape == "backslash":
            # TODO: print goals for backslash
            pass
        self._print_track_positions()

    def get_track(self):
        """Return self.track_positions, allow other classes to know the track positions"""
        return self.track_positions

    def get_goal_center(self):
        """Calculate and return coordinates of goal position"""
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
        # TODO: goal location for slash and backslash tracks
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
            # y = 2 to leave a gap below the titlebar
            return (term.width // 2, 2)
        elif self.shape == "backslash":
            return (2, 2)
        elif self.shape == "slash":
            pass
        elif self.shape == "plus":
            pass
        elif self.shape == "multiplication":
            pass
        elif self.shape == "asterisk":
            pass

    def get_track_end(self):
        """Calculate and return ending of track"""
        if self.shape == "hyphen":
            return (term.width, term.height // 2)
        if self.shape == "pipe":
            return (term.width // 2, term.height-1)
        if self.shape == "backslash":
            return (term.width - 2, term.height - 2)
        return None

    def _screen_clear(self):
        """Clear the screen in preparation for track"""
        # TODO: move this to Game
        print(term.home + term.normal + term.clear)

    def _track_hyphen(self):
        positions = []
        start_x, start_y = self.get_track_start()
        end = term.width
        for position in range(start_x, end, 1):
            positions.append((position, start_y))
        return positions

    def _track_pipe(self):
        start_x, start_y = self.get_track_start()
        end_y = self.get_track_end()[1]
        start_x, start_y = self.get_track_start()
        end_y = self.get_track_end()[1]
        positions = []
        for position in range(start_y, end_y, 1):
            positions.append((start_x, position))
        return positions

    def _slope_btwn_points(self, point1, point2):
        x1, y1 = point1
        x2, y2 = point2
        d_y = y2 - y1
        d_x = x2 - x1
        if d_x != 0:
            slope = d_y / d_x
            return slope
        return None

    def _slope_closer_to_goal_slope(self, point1, point2, end_point):
        slope1 = self._slope_btwn_points(point1, end_point)
        slope2 = self._slope_btwn_points(point2, end_point)
        if slope1 is None:
            return point2
        if slope2 is None:
            return point1
        d_goal_slope1 = abs(slope1 - self.goal_slope)
        d_goal_slope2 = abs(slope2 - self.goal_slope)
        if d_goal_slope1 < d_goal_slope2:
            return point1
        elif d_goal_slope2 < d_goal_slope1:
            return point2
        return random.choice([point1, point2])

    def _track_backslash(self):
        start = self.get_track_start()
        end = self.get_track_end()
        # print(start, end)
        self.goal_slope = self._slope_btwn_points(start, end)
        # print(self.goal_slope)
        cur = list(start)
        positions = []
        while cur[0] < end[0] and cur[1] < end[1]:
            next_x = (cur[0]+1, cur[1])
            next_y = (cur[0], cur[1]+1)
            closest_to_goal_slope = self._slope_closer_to_goal_slope(next_x, next_y, end)
            positions.append(closest_to_goal_slope)
            cur = closest_to_goal_slope
        return positions

    def virtual_track(self):
        """Create object with x,y coordinates for each place on the track, and update state"""
        if self.shape == "hyphen":
            positions = self._track_hyphen()
        elif self.shape == "pipe":
            positions = self._track_pipe()
        elif self.shape == "backslash":
            positions = self._track_backslash()
        self.track_positions = positions

    def print_goal_pipe(self):
        """Print goals around where 'center' is"""
        goal_x, goal_y = self.get_goal_center()
        print(term.move_xy(goal_x-1, goal_y-1) + PIPE_GOAL_UPPER_LOWER)
        print(term.move_xy(goal_x-1, goal_y) + PIPE_GOAL_MIDDLE)
        print(term.move_xy(goal_x-1, goal_y+1) + PIPE_GOAL_UPPER_LOWER)

    def _print_track_positions(self):
        for xy in self.track_positions:
            print(term.move_xy(*xy) + f"{reverse} {term.normal}")

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

    # TODO: create is_goal method, remove that test from racer.
    # TODO: two shapes on the screen at once
