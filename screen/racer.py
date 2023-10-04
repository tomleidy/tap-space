from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER
#from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
#from constants.game import STARTING_LIVES
from constants.game import INPUT_TIMEOUT
from screen.locations import row_track, column_goal, term

class Racer:
    def __init__(self):
        #print("wait a moment")
        self.input_key = ""
        self.place = 0
        self.direction = 1

    def refresh(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        direction = self.direction
        place = self.place
        self.print_racer(place)
        if direction > 0 and place == term.width or direction < 0 and place == 0:
            self.direction *= -1
        self.place += self.direction
        with term.cbreak(), term.hidden_cursor():
            self.input_key = term.inkey(INPUT_TIMEOUT).lower()
            if self.input_key == "q":
                return "q"
            elif self.input_key == " ":
                if self.place == column_goal:
                    return "goal"
                else:
                    return "miss"

    def print_racer(self, position):
        """Display the racer character on the track"""
        if position > 0 and position < term.width:
            print(term.move_xy(position - 1, row_track) + TRACK_CHARACTER)
        print(term.move_xy(position, row_track) + regular + RACER_CHARACTER + reverse)
        if position < term.width and position > 0:
            print(term.move_xy(position + 1, row_track) + TRACK_CHARACTER)
            
            