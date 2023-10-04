"""The game itself."""
import time
from constants.terminal_strings import WIN_MESSAGE, LOSE_MESSAGE
from constants.game import STARTING_LIVES
from screen.track import Track
from screen.messages import Message
from screen.racer import Racer
from screen.locations import term
from screen.titlebar import TitleBar

# eventually will update all with screen.update() instead of 

# score = (remaining_lives / elapsed_time) * some_constant_factor

class Game:
    """Primary class for running game instances"""
    def __init__(self, starting_lives=STARTING_LIVES):
        self.lives = starting_lives
        self.score = 0
        self.difficulty = 0 # constant speed, (30ms input timeout?)
        self.racer_feedback = ""
        self.track = Track()
        self.message = Message()
        self.racer = Racer()
        self.titlebar = TitleBar(time.time(), self.lives)

    def run_game(self):
        """Runs the sentinel pattern loop"""
        while self.racer_feedback != "q":
            self.titlebar.refresh()
            self.message.refresh()
            self.racer_feedback = self.racer.refresh()
            if self.racer_feedback == "goal":
                self.message.send(WIN_MESSAGE)
            elif self.racer_feedback == "miss":
                self.message.send(LOSE_MESSAGE)

    def space_miss(self):
        """Player hit spacebar, it was a miss"""
        self.message.send(WIN_MESSAGE)

    
game = Game(9)
game.run_game()

# do we need to reset the terminal to normal? we do.
print(term.normal)
