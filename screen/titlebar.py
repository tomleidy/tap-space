"""TitleBar class module for initiating, displaying, and updating titlebar."""
import time
from blessed import Terminal
from constants.terminal_colors import reverse


term = Terminal()
MAX_LEVEL_SCORE = 70000


class TitleBar:
    """Class for titlebar display. Primary external method is refresh() to have it 
    calculate/update to current values."""
    # I'm not happy with duplicating some of these things here and in Game (e.g. lives).
    # The goal is to create a module for the numbers, to keep track of the goals,
    # misses, score, etc. And that will be the repository of the data for this.

    def __init__(self, start_time, lives):
        self.start_time = start_time
        self.goals = 0
        self.misses = 0
        self.lives = lives
        self.potential_score = MAX_LEVEL_SCORE
        self.level_name = "level_name_placeholder"
        print(term.move_xy(0, 0) + reverse + term.center("tap space"))

    def pad_to_two_digits(self, num):
        """Pad numbers. Max 99. Negative numbers converted to absolute value"""
        if not isinstance(num, (int, float)):
            return "tt"  # type test error
        if num > 99:
            return "99"
        if num < 0:
            return "nn"  # negative number, why?
        return f"{num:02}"

    def print_gametime(self):
        """Print time in game to title bar"""
        duration = int(time.time()) - int(self.start_time)
        minutes = self.pad_to_two_digits(duration // 60)
        seconds = self.pad_to_two_digits(duration % 60)
        duration_string = f"{minutes}:{seconds}"
        position_duration_x = term.width - (len(duration_string) + 1)
        self.print_statusbar(position_duration_x, reverse + duration_string)

    def refresh(self):
        """Run methods in class to update titlebar with every iteration"""
        self.print_gametime()
        self.print_current_goals_lives()

    def print_retries_remaining(self):
        """Display retries remaining in titlebar"""

    def print_statusbar(self, start_x, content):
        """Print content to the status bar."""
        print(f"{term.move_xy(start_x, 0)}{content}")

    def print_current_goals_lives(self):
        "Display current game score in title bar"
        goals = f"Goals: {self.pad_to_two_digits(self.goals)}"
        lives = f"Lives: {self.pad_to_two_digits(self.lives)}"
        self.print_statusbar(1, f"{reverse}{goals} {lives}")

    def add_goal(self):
        """Update class with game score"""
        self.goals += 1

    def add_miss(self):
        """Update class with misses count"""
        self.misses += 1
        self.lives -= 1
        return self.lives

    def highscores_load(self):
        """Load highscores from file on start"""
        # score stuff needs to go to a score module

    def highscores_save(self):
        """Save highscores to file on quit"""

    def speed_tweaker(self):
        """To change speed for hardest difficulty mode."""
