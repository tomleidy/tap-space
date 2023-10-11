from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
from constants.game import INPUT_TIMEOUT
from screen.locations import column_goal, term #, row_track

from screen.messages import Message

DEBUG = True


class Racer:
    def __init__(self, track_positions, shape="pipe"):
        self.input_key = ""
        self.place_cur = min(track_positions.keys())
        self.place_prev = 0
        self.shape = shape
        self.prev_xy = {}
        self.cur_xy = {}
        self.next_xy = {}
        self.direction = 1
        self.message = Message()
        self.track_positions = track_positions
        self.min_x = -1
        self.max_x = -1
        self.min_y = -1
        self.max_y = -1

    def get_track_ends(self):
        min_x = -1
        max_x = -1
        min_y = -1
        max_y = -1
        for position in self.track_positions.values():
            if min_x == -1 or position["x"] < min_x:
                min_x = position["x"]
            if position["x"] > max_x:
                max_x = position["x"]
            if min_y == -1 or position["y"] < min_y:
                min_y = position["y"]
            if position["y"] > max_y:
                max_y = position["y"]
        return {"min": (min_x, min_y), "max": (max_x, max_y)}

    def print_location(self, x, y):
        if DEBUG == True:
            if self.min_x == -1 or x < self.min_x:
                self.min_x = x
            if x > self.max_x:
                self.max_x = x
            if self.min_y == -1 or x < self.min_y:
                self.min_y = y
            if y > self.max_y:
                self.max_y = y
            with term.hidden_cursor():
                print(term.move_xy(1, 2) + f"({x},{y})")
                print(term.move_xy(1, 3) + f"({self.min_x},{self.min_y})")
                print(term.move_xy(1, 4) + f"({self.max_x},{self.max_y})")
                print(term.move_xy(1, 5) + f"{self.get_track_ends()}")

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

    def advance_position(self):
        """Update current position, and the previous/next _xy dictionaries"""
        if self.does_pos_exist(self.place_cur+self.direction):
            self.place_prev = self.place_cur
            self.place_cur += self.direction

    def refresh(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
            self.advance_position()
        return self.get_term_input()

    def does_pos_exist(self, position):
        """Determine if position is available in track_positions dictionary"""
        if position not in self.track_positions:
            return False
        return True
        

    def get_pos_dict(self, position):
        """Return xy coordinate object for a position"""
        # if DEBUG == True:
        #     print(term.move_xy(1, 3) + "position:",
        #           position, self.track_positions)
        #    sys.exit()
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
        
