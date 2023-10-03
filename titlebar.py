from blessed import Terminal
import time

term = Terminal()


def pad_to_two_digits(num):
    """Pad numbers. Max 99. Negative numbers converted to absolute value"""
    if not isinstance(num, (int)):
        return "tt" # type test error
    if num > 99:
        return "99"
    if num < 0:
        return "nn" # negative number, why?
    return f"{num:02}"


def seconds_to_mmss(gametime):
    """Take time in seconds and convert it into time playing in mm:ss"""
    if gametime > 3600:
        # end_game(timeout_message)
        pass
    hours = pad_to_two_digits(gametime // 3600)
    minutes = pad_to_two_digits(gametime % 3600 // 60)
    seconds = pad_to_two_digits(gametime % 60)
    
    return pad_to_two_digits(minutes) + ":" + pad_to_two_digits(seconds)


def print_gametime(start_time):
    duration = int(time.time()) - start_time
    duration_string = seconds_to_mmss(duration) + " "
    start_duration_x = term.width - len(duration_string)
    print(term.move_xy(start_duration_x, 0) + duration_string)


def print_lives_remaining(lives):
    pass


def print_header(lives, start_time, score):
    """Print header row, including ANSI, etc."""
    print(term.move_xy(0,0) + reversed)
    #print(term.move(xy(1,0) + f"Score: {score}"))
    

# Score is going to be calculated per round, and added to a cumulative game score.
#


def get_current_score():
    pass


def score_ratio():
    pass


def lives_decrement(lives):
    pass


def highscores_load():
    """Load highscores from file on start"""
    pass


def highscores_save():
    """Save highscores to file on quit"""
    pass


def speed_tweaker():
    """To change speed for hardest difficulty mode."""
    pass
