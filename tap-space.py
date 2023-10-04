"""The game itself."""
import time
from blessed import Terminal
from constants.terminal_colors import regular, reverse
from constants.terminal_strings import TRACK_CHARACTER, RACER_CHARACTER, GOAL_UPPER, GOAL_LOWER
from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
from constants.game import INPUT_TIMEOUT, STARTING_LIVES
from screen.messages import message_send, message_row_clear
from screen.locations import row_track, column_goal
#from constants.terminal_strings import TIMEOUT_MESSAGE
import titlebar
term = Terminal()

# Groupings to turn into classes: screen setup (track, goals, titlebar)
# eventually will update all with screen.update() instead of 
# individually calling indvidual refresh buttons?
# 

# score = (remaining_lives / elapsed_time) * some_constant_factor

class Game:
    """Primary class for running game instances"""
    def __init__(self, starting_lives=STARTING_LIVES):
        self.lives = starting_lives
        self.score = 0
        self.difficulty = 0 # constant speed, (30ms input timeout?)
        self.input_key = ""
        self.prep_screen()

    def prep_screen(self):
        """Prepare terminal for playing: clear, set goals, set track"""
        print(term.home + term.clear)
        print(term.move_y(row_track))
        print(regular)
        print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
        print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)
        print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
        print(term.move_xy(0, row_track) + TRACK_CHARACTER*term.width)

    def run_game(self):
        """Runs the sentinel pattern loop"""
        while self.input_key != "q":
            self.run_racer()

    def print_racer(self, position):
        """Display the racer character on the track"""
        if position > 0 and position < term.width:
            print(term.move_xy(position - 1, row_track) + TRACK_CHARACTER)
        print(term.move_xy(position, row_track) + regular + RACER_CHARACTER + reverse)
        if position < term.width and position > 0:
            print(term.move_xy(position + 1, row_track) + TRACK_CHARACTER)

    def space_miss(self):
        """Player hit spacebar, it was a miss"""
        pass
    
    def run_racer(self):
        """Loop print_racer() for the row: bounce racer character on edges of terminal"""
        place = 0
        countdown = -1
        direction = 1
        title_instance = titlebar.TitleBar(time.time(), self.lives)
        while True:
            title_instance.refresh()
            self.print_racer(place)
            if direction > 0 and place == term.width or direction < 0 and place == 0:
                direction *= -1
            place += direction
            if countdown == 0:
                message_row_clear()
            if countdown >= 0:
                countdown -= 1
            with term.cbreak(), term.hidden_cursor():
                self.input_key = term.inkey(INPUT_TIMEOUT).lower()

                if self.input_key == "q":
                    return "q"
                elif self.input_key == " ":
                    if place == column_goal:
                        message_send(WIN_MESSAGE)
                        countdown = 50
                    else:
                        message_send(LOSE_MESSAGE)
                        countdown = 50

game = Game(9)
game.run_game()

# do we need to reset the terminal to normal? we do.
print(term.normal)
