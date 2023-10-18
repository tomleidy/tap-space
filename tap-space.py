"""The game itself."""
import time
import os
import platform
import sys
import argparse
from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
from constants.game import LEVELS
from screen.track import Track
from screen.messages import Message
from screen.racer import Racer
from screen.locations import term
from screen.titlebar import TitleBar

GAME_OVER_MESSAGE = "You were luckier than a cat. Sorry to say, you've run out of lives."

level_names = []
for level in LEVELS:
    level_names.append(level["name"].lower())
parser = argparse.ArgumentParser(prog="tap-space",
                                 description="a terminal tap game",
                                 epilog="the name tells you how to interact")
parser.add_argument("-s", "--shape", default="hyphen", choices=level_names)
parser.add_argument("-d", "--difficulty", type=int,
                    default=1, choices=[1, 2, 3, 4, 5])

args = parser.parse_args()

# eventually will update all with screen.update() instead of track, message, racer updates

# score = (remaining_lives / elapsed_time) * some_constant_factor

if platform.system() == 'Windows' and os.getenv('MSYSTEM') == 'MINGW64':
    print("Please run from Windows PowerShell, macOS, Linux, or WSL")
    sys.exit()
    # I haven't figured out how to get this to work properly in Git Bash terminals.
    # They don't handle the ANSI as intended.


def shape_menu():
    print("1. Hyphen")
    print("2. Pipe")


def difficulty_menu():
    print("1. Normal")
    print("5. Impossible")


class Game:
    """Primary class for running game instances"""

    def __init__(self, starting_lives, shape="hyphen", difficulty=1):
        self.shape = shape
        self.lives = starting_lives
        self.difficulty = difficulty  # constant speed, (30ms input timeout?)
        self.goals = 0
        self.misses = 0
        self.racer_feedback = ""
        self._screen_clear()
        self.track = Track(self.shape, self.difficulty)
        self.message = Message()
        self.track_positions = self.track.get_track()
        self.racer = Racer(self.track_positions,
                           self.track.get_goal_center(), self.shape, self.difficulty)
        self.titlebar = TitleBar(time.time(), self.lives)

    def _screen_clear(self):
        """Clear the screen in preparation for track"""
        print(term.home + term.normal + term.clear)

    def run_game(self):
        """Runs the sentinel pattern loop"""

        while self.racer_feedback != "q":
            self.titlebar.refresh()
            self.message.refresh()
            self.racer_feedback = self.racer.refresh()
            if self.racer_feedback == "goal":
                self.titlebar.add_goal()
                self.message.send(WIN_MESSAGE)
            elif self.racer_feedback == "miss":
                lives = self.titlebar.add_miss()
                self.message.send(LOSE_MESSAGE)
                if lives == 0:
                    self.message.send(GAME_OVER_MESSAGE)
                    self.racer_feedback = "q"

        self.track.wipe_track_normal()

    def space_miss(self):
        """Player hit spacebar, it was a miss"""
        self.message.send(WIN_MESSAGE)


game = Game(99, args.shape, args.difficulty)
game.run_game()

# do we need to reset the terminal to normal? we do.
# print(term.normal + term.clear)
print(term.normal_cursor() + term.normal)
