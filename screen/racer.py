from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
from constants.game import INPUT_TIMEOUT
from screen.locations import column_goal, term #, row_track

from screen.messages import Message

class Racer:
    def __init__(self, track_positions, shape="pipe"):
        self.input_key = ""
        self.place_cur = 0
        self.place_prev = 0
        self.shape = shape
        self.prev_xy = {}
        self.cur_xy = {}
        self.next_xy = {}
        self.direction = 1
        self.message = Message()
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

    def is_at_wall(self):
        """Determine if position is against the end of the track"""
        return not self.does_pos_exist(self.place_cur+self.direction)

    def advance(self):
        """Update current position, and the previous/next _xy dictionaries"""
        if self.does_pos_exist(self.place_cur+self.direction):
            self.place_prev = self.place_cur
            self.place_cur += self.direction

    def refresh(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        self.print_racer()
        if self.is_at_wall():
            self.direction *= -1
        self.advance()
        return self.get_term_input()

    def does_pos_exist(self, position):
        """Determine if position is available in track_positions dictionary"""
        if position not in self.track_positions:
            return False
        return True
        

    def get_pos_dict(self, position):
        """Return xy coordinate object for a position"""
        if self.does_pos_exist(position):
            #print("position:", position, self.track_positions)
            return self.track_positions[position]
        return {"x": -1, "y": -1}

    def print_to_pos(self, position, content):
        """Print content to x,y coordinates according to position from track_positions"""
        xy_pos = self.get_pos_dict(position)
        x_pos = xy_pos["x"]
        y_pos = xy_pos["y"]
        if x_pos == -1 or y_pos == -1:
            return None
        print(term.move_xy(x_pos, y_pos) + content)

    def print_racer(self):
        """Display the racer character on the track"""
        
        if self.shape == "pipe":
            self.print_to_pos(self.place_prev, f"{term.normal}{reverse}{TRACK_CHARACTER}{term.normal}")
            self.print_to_pos(self.place_cur, f"{term.normal}{regular}{RACER_CHARACTER}{term.normal}")
        elif self.shape == "hyphen":
            self.print_to_pos(self.place_prev, f"{reverse}{TRACK_CHARACTER}{reverse}")
            self.print_to_pos(self.place_cur, f"{reverse}{regular}{RACER_CHARACTER}{reverse}")
            
        #print(term.move_xy(position - 1, row_track) + TRACK_CHARACTER)
        #print(term.move_xy(position, row_track) + regular + RACER_CHARACTER + reverse)
        
