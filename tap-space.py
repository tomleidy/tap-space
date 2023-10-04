"""The game itself."""
import time
from blessed import Terminal
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER, GOAL_UPPER, GOAL_LOWER
from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
#from constants.terminal_strings import TIMEOUT_MESSAGE
import titlebar
term = Terminal()

# Groupings to turn into classes: screen setup (track, goals, titlebar)
# eventually will update all with screen.update() instead of 
# individually calling indvidual refresh buttons?
# 

# This is the variable that controls the speed of the game. Higher? slower game.
# This is as fast as it can go and still be cross-platform to my current understanding.
# Windows can only do 15.6ms timeouts. macOS can do it much faster.
INPUT_TIMEOUT = 0.0156
STARTING_LIVES = 10

row_track = term.height // 2
column_goal = term.width // 2
message_row = row_track - 5


# score = (remaining_lives / elapsed_time) * some_constant_factor
lives = STARTING_LIVES

class Game:
    """Primary class for running game instances"""
    def __init__(self, starting_lives):
        self.lives = starting_lives
        self.score = 0
        self.difficulty = 0 # constant speed, (30ms input timeout?)
        self.input_key = ""
        self.prep_screen()

    def end_game(self, message):
        """End game and send end game message"""
        print(term.move_xy(0, row_track + 4) + term.normal + message)
        self.input_key = "q"

    def prep_screen(self):
        """Prepare terminal for playing: clear, set goals, set track"""
        print(term.home + term.clear)
        print(term.move_y(row_track))
        print(regular)
        print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
        print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)
        print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
        for x in range(0, term.width):
            print(term.move_y(row_track) + term.move_x(x) + TRACK_CHARACTER)

    def run_game(self):
        while self.input_key != "q":
            self.run_racer()

    def print_racer(self, x):
        """Display the racer character on the track"""
        if x > 0 and x < term.width:
            print(term.move_xy(x - 1, row_track) + TRACK_CHARACTER)
        print(term.move_xy(x, row_track) + regular + RACER_CHARACTER + reverse)
        if x < term.width and x > 0:
            print(term.move_xy(x + 1, row_track) + TRACK_CHARACTER)

    def space_message(self, message):
        """Print message to message row"""
        print(term.move_y(message_row) + regular + term.center(message) + reverse)

    def clear_message(self):
        """Clear message from message row"""
        print(term.move_y(message_row) + term.normal + term.center("") + reverse)

    def run_racer(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        place = 0
        countdown = -1
        direction = 1
        title_instance = titlebar.TitleBar(time.time(), lives)
        while True:
            title_instance.refresh()
            self.print_racer(place)
            if direction > 0 and place == term.width or direction < 0 and place == 0:
                direction *= -1
            place += direction
            if countdown == 0:
                self.clear_message()
            if countdown >= 0:
                countdown -= 1
            with term.cbreak(), term.hidden_cursor():
                self.input_key = term.inkey(INPUT_TIMEOUT).lower()

                if self.input_key == "q":
                    return "q"
                elif self.input_key == " ":
                    if place == column_goal:
                        self.space_message(WIN_MESSAGE)
                        countdown = 50
                    else:
                        self.space_message(LOSE_MESSAGE)
                        countdown = 50

game = Game(9)
game.run_game()

# do we need to reset the terminal to normal? we do.
print(term.normal)