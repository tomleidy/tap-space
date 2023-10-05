from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
from constants.game import INPUT_TIMEOUT
from screen.locations import row_track, column_goal, term

class Racer:
    def __init__(self, track_positions):
        self.input_key = ""
        self.place_cur = 0
        self.prev_xy = {}
        self.cur_xy = {}
        self.next_xy = {}
        self.direction = 1
        self.track_positions = track_positions

    def set_track_positions(self, track_positions):
        """A setter, just in case the track changes"""
        self.track_positions = track_positions

    def get_term_input(self):
        """Use terminal methods to get user input"""
        with term.cbreak(), term.hidden_cursor():
            self.input_key = term.inkey(INPUT_TIMEOUT).lower()
            if self.input_key == "q":
                return "q"
            elif self.input_key == " ":
                if self.place_cur == column_goal:
                    return "goal"
                else:
                    return "miss"
            return ""

    def is_at_wall(self, place):
        """Determine if position is against the end of the track"""
        direction = self.direction
        length = len(self.track_positions)
        return direction > 0 and place == length or direction < 0 and place == 0

    def advance(self):
        """Update current position, and the previous/next _xy dictionaries"""
        if self.does_pos_exist(self.place_cur):
            self.prev_xy = self.get_pos_dict(self.place_cur)
        self.place_cur += self.direction
        if self.does_pos_exist(self.place_cur+self.direction):
            self.next_xy = self.get_pos_dict(self.place_cur+self.direction)
        else:
            self.next_xy = self.get_pos_dict(self.place_cur-self.direction)

    def refresh(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        place_cur = self.place_cur
        self.print_racer(place_cur)
        if self.is_at_wall(place_cur):
            self.direction *= -1
        self.advance()
        return self.get_term_input()

    def does_pos_exist(self, position):
        """Determine if position is available in track_positions dictionary"""
        if position < 0 or position >= len(self.track_positions):
            return False
        return True

    def get_pos_dict(self, position):
        """Return xy coordinate object for a position"""
        if self.does_pos_exist(position):
            return self.track_positions[position]
        return {"x": -1, "y": -1}

    def print_racer(self, position):
        """Display the racer character on the track"""

        print(term.move_xy(position - 1, row_track) + TRACK_CHARACTER)
        print(term.move_xy(position, row_track) + regular + RACER_CHARACTER + reverse)
        if position < term.width and position > 0:
            print(term.move_xy(position + 1, row_track) + TRACK_CHARACTER)
