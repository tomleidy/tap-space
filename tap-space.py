import time
from blessed import Terminal
from terminal_colors import regular, reverse
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
TRACK_CHARACTER = " "
RACER_CHARACTER = "*"
GOAL_UPPER = "=v="
GOAL_LOWER = "=^="
STARTING_LIVES = 10
WIN_MESSAGE = "Goal!"
LOSE_MESSAGE = "You missed, try again or press q to quit"
TIMEOUT_MESSAGE = "Hey, are you there?"

row_track = term.height // 2
column_goal = term.width // 2
message_row = row_track - 5


# score = (remaining_lives / elapsed_time) * some_constant_factor
lives = STARTING_LIVES


def end_game(message):
    """End game and send end game message"""
    print(term.move_xy(0, row_track + 4) + term.normal + message)
    #inp = "q"


def prep_screen():
    """Prepare terminal for playing: clear, set goals, set track"""
    print(term.home + term.clear)
    print(term.move_y(row_track))
    print(regular)
    print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
    print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)
    print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
    for x in range(0, term.width):
        print(term.move_y(row_track) + term.move_x(x) + TRACK_CHARACTER)

def print_racer(x):
    """Display the racer character on the track"""
    if x > 0 and x < term.width:
        print(term.move_xy(x - 1, row_track) + TRACK_CHARACTER)
    print(term.move_xy(x, row_track) + regular + RACER_CHARACTER + reverse)
    if x < term.width and x > 0:
        print(term.move_xy(x + 1, row_track) + TRACK_CHARACTER)


def space_message(message):
    """Print message to message row"""
    print(term.move_y(message_row) + regular + term.center(message) + reverse)


def clear_message():
    """Clear message from message row"""
    print(term.move_y(message_row) + term.normal + term.center("") + reverse)


def run_racer():
    """Loop print_racer() for the row, bouncing the racer character from each edge of the terminal"""
    place = 0
    countdown = -1
    direction = 1
    title_instance = titlebar.TitleBar(time.time(), lives)
    while True:
        title_instance.refresh()
        print_racer(place)
        if direction > 0 and place == term.width or direction < 0 and place == 0:
            direction *= -1
        place += direction
        if countdown == 0:
            clear_message()
        if countdown >= 0:
            countdown -= 1
        with term.cbreak(), term.hidden_cursor():
            cur_inp = term.inkey(INPUT_TIMEOUT).lower()

            if cur_inp == "q":
                return "q"
            elif cur_inp == " ":
                if place == column_goal:
                    space_message(WIN_MESSAGE)
                    countdown = 50
                else:
                    space_message(LOSE_MESSAGE)
                    countdown = 50
            return cur_inp


prep_screen()
inp = ""
while inp != "q":
    inp = run_racer()

# do we need to reset the terminal to normal? we do.
print(term.normal)