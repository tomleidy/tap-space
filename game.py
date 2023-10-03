from blessed import Terminal

term = Terminal()


INPUT_TIMEOUT = 0.0156
TRACK_CHARACTER = " "
RACER_CHARACTER = "*"
GOAL_UPPER = "=v="
GOAL_LOWER = "=^="
GOAL_LEFT = "|>|"  # this are going to take a multistep write
GOAL_RIGHT = "|<|"
STARTING_LIVES = 10
WIN_MESSAGE = "Goal!"
LOSE_MESSAGE = "You missed, try again or press q to quit"
TIMEOUT_MESSAGE = "Hey, are you there?"

regular = term.on_color_rgb(40, 40, 40) + term.color_rgb(255, 169, 0)
reverse = term.color_rgb(40, 40, 40) + term.on_color_rgb(255, 169, 0)
column_goal = term.width // 2
row_track = term.height // 2

column_track = term.width // 2
row_goal = term.height // 2

row_track = term.height // 2
column_goal = term.width // 2
message_row = row_track - 5


class Game:
    """The center of all this madness, where we setup our loop to run the game from"""

    message_row = row_track - 5

    def __init__(self, time, starting_lives):
        self.runtime = time
        self.inputkey = ""
        self.score = 0
        self.lives = starting_lives

    def prep_screen(self):
        """Prepare terminal for playing: clear, set goals, set track"""
        print(term.home + term.clear)
        print(term.move_y(row_track))
        print(regular)

    def prep_track_horizontal(self, column_goal, row_track):
        """Prepare a horizontal track, with a goal on the lines above and below row_track"""
        print(term.move_xy(column_goal - 1, row_track - 1) + GOAL_UPPER)
        print(term.move_xy(column_goal - 1, row_track + 1) + GOAL_LOWER)
        print(reverse + term.move_y(row_track) + TRACK_CHARACTER)
        for x in range(0, term.width):
            print(term.move_y(row_track) + term.move_x(x) + TRACK_CHARACTER)

    def prep_track_vertical(self, column_track, row_goal):
        """text goes here"""
        # will probably need to print ANSI characters to protect the color on either 
        # side of the track. just remembered that the line seems to get affected 
        # once a character is printed which will also be a thing I need to do
        # in the diagonal. Exciting.
        print(term.move_xy(row_goal - 1, row_goal - 1) + GOAL_LEFT)
        print(term.move_xy(row_goal - 1, row_goal + 1) + GOAL_RIGHT)
        print()
