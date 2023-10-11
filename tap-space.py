"""The game itself."""
import time
import os
import platform
import sys
import argparse
from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
from constants.game import STARTING_LIVES, LEVELS
from screen.track import Track
from screen.messages import Message
from screen.racer import Racer
from screen.locations import term
from screen.titlebar import TitleBar

level_names = []
for level in LEVELS:
    level_names.append(level["name"].lower())
parser = argparse.ArgumentParser(prog="tap-space",
                                 description="a terminal tap game",
                                 epilog="the name tells you how to interact")
parser.add_argument("-s", "--shape", default="hyphen", choices=level_names)

args = parser.parse_args()

# eventually will update all with screen.update() instead of track, message, racer updates

# score = (remaining_lives / elapsed_time) * some_constant_factor

if platform.system() == 'Windows' and os.getenv('MSYSTEM') == 'MINGW64':
    print("Please run from Windows PowerShell, macOS, Linux, or WSL")
    sys.exit()
    # I haven't figured out how to get this to work properly in Git Bash terminals.
    # They don't handle the ANSI as intended.

class Game:
    """Primary class for running game instances"""
        self.shape = shape
        self.lives = starting_lives
        self.goals = 0
        self.misses = 0
        self.difficulty = 0  # constant speed, (30ms input timeout?)
        self.racer_feedback = ""
        self.track = Track(self.shape)
        self.message = Message()
        self.track_positions = self.track.get_track()
        self.racer = Racer(self.track_positions, self.shape)
        self.titlebar = TitleBar(time.time(), self.lives)

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
                self.titlebar.add_miss()
                self.message.send(LOSE_MESSAGE)

    def space_miss(self):
        """Player hit spacebar, it was a miss"""
        self.message.send(WIN_MESSAGE)


game = Game(9, args.shape)
game.run_game()

# do we need to reset the terminal to normal? we do.
#print(term.normal + term.clear)
print(term.normal_cursor() + term.normal)