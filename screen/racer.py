import random
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
from constants.game import INPUT_TIMEOUT
from screen.track import term
from screen.messages import Message


class Racer:
    """Display the racer character"""

    def __init__(self, track_positions, goal_xy, shape, difficulty):
        self.input_key = ""
        self.current_position = 0
        self.previous_position = 0
        self.shape = shape
        self.goal_xy = goal_xy
        self.direction = 1
        self.message = Message()
        self.difficulty = difficulty

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
        return (self.track_positions[self.current_position])

    def is_at_wall(self):
        """Determine if position is against the end of the track"""
        min_place = 0
        max_place = len(self.track_positions)-1
        at_wall = self.current_position in (min_place, max_place)
        return at_wall

    def advance_position(self):
        """Update current position, and the previous/next _xy dictionaries"""
        self.previous_position = self.current_position
        next_position = self.current_position+self.direction
        if self.does_position_exist(next_position):
            self.current_position += self.direction
            if self.difficulty == 5:
                rand = random.randint(0, len(self.track_positions)//5)
                self.current_position += rand
                current = self.current_position % len(self.track_positions)
                self.current_position = current
            else:
            self.current_position += self.direction

    def does_position_exist(self, position):
        """Determine if position is available in track_positions dictionary"""
        return position >= 0 and position < len(self.track_positions)

    def get_position_xy(self, position):
        """Return xy coordinate object for a position."""
        # This is clunky. I'll figure out how to refine it eventually.
        if self.does_position_exist(position):
            return self.track_positions[position]
        return (5, 5)

    def print_to_position(self, position, content):
        """Print content to x,y coordinates according to position from track_positions"""
        xy_pos = self.get_position_xy(position)
        print(term.move_xy(*xy_pos) + content)

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
