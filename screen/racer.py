from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
from constants.game import INPUT_TIMEOUT
from screen.track import term
from screen.messages import Message


class Racer:
    """Display the racer character"""

    def __init__(self, track_positions, goal_xy, shape):
        self.input_key = ""
        self.current_position = min(track_positions.keys())
        self.previous_position = 0
        self.shape = shape
        self.goal_xy = goal_xy
        self.direction = 1
        self.message = Message()

        self.track_positions = track_positions

    def refresh(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        self.print_racer()
        self.advance_position()
        if self.is_at_wall():
            self.direction *= -1
        return self.get_input()

    def get_input(self):
        """Use terminal methods to get user input."""
        # The limitations of the inkey timeout in Windows is what sets our speed.
        with term.cbreak(), term.hidden_cursor():
            self.input_key = term.inkey(INPUT_TIMEOUT).lower()
            if self.input_key == "q":
                return "q"
            if self.input_key == " ":
                if self.get_current_xy() == self.goal_xy:
                    return "goal"
                return "miss"
            return ""

    def get_current_xy(self):
        position = self.current_position
        return (self.track_positions[position]["x"], self.track_positions[position]["y"])

    def is_at_wall(self):
        """Determine if position is against the end of the track"""
        min_place = min(self.track_positions.keys())
        max_place = max(self.track_positions.keys())
        at_wall = self.current_position in (min_place, max_place)
        # if at_wall == True:
        #     print(term.move_xy(3, 3) + str(self.get_current_xy()))
        return at_wall

    def advance_position(self):
        """Update current position, and the previous/next _xy dictionaries"""
        self.previous_position = self.current_position
        next_position = self.current_position+self.direction
        if self.does_position_exist(next_position):
            self.current_position += self.direction

    def does_position_exist(self, position):
        """Determine if position is available in track_positions dictionary"""
        return position in self.track_positions

    def get_position_xy(self, position):
        """Return xy coordinate object for a position."""
        # This is clunky. I'll figure out how to refine it eventually.
        if self.does_position_exist(position):
            x_pos = self.track_positions[position]["x"]
            y_pos = self.track_positions[position]["y"]
            return (x_pos, y_pos)
        return (-1, -1)

    def print_to_position(self, position, content):
        """Print content to x,y coordinates according to position from track_positions"""
        xy_pos = self.get_position_xy(position)
        x_pos = xy_pos[0]
        y_pos = xy_pos[1]
        if x_pos == -1 or y_pos == -1:
            return None
        with term.hidden_cursor():
            print(term.move_xy(x_pos, y_pos) + content)

    def print_racer_pipe(self):
        """Print the racer on the pipe track, replacing previous track"""
        pipe_string_previous = f"{term.normal}{reverse}{TRACK_CHARACTER}{term.normal}"
        pipe_string_racer = f"{term.normal}{regular}{RACER_CHARACTER}{term.normal}"
        previous = self.previous_position
        current = self.current_position
        self.print_to_position(previous, pipe_string_previous)
        self.print_to_position(current, pipe_string_racer)

    def print_racer_hyphen(self):
        """Print the racer to the hyphen track, replace previous track"""
        hyphen_string_previous = f"{reverse}{TRACK_CHARACTER}{reverse}"
        hyphen_string_racer = f"{reverse}{regular}{RACER_CHARACTER}{reverse}"
        previous = self.previous_position
        current = self.current_position
        self.print_to_position(previous, hyphen_string_previous)
        self.print_to_position(current, hyphen_string_racer)

    def print_racer(self):
        """Call the appropriate print_racer_TRACK"""
        if self.shape == "pipe":
            self.print_racer_pipe()
        elif self.shape == "hyphen":
            self.print_racer_hyphen()
