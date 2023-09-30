# Want the score on the top left, the time on the top right


def padding_two_digits(num):
    """Take a single digit number and turn it into a two digit number. Max 99. Negative numbers converted to absolute value"""
    if num < 0:
        num = abs(num)
    if num < 10:
        return "0" + str(abs(num))
    elif num > 99:
        return "99"
    elif num >= 10 and num <= 99:
        return str(num)
    else:
        return "dd"


def seconds_to_mmss(gametime):
    """Take time in seconds and convert it into time playing in mm:ss"""
    if gametime > 3600:
        # end_game(timeout_message)
        pass
    minutes = gametime % 60
    seconds = gametime - (minutes * 60)
    return padding_two_digits(minutes) + ":" + padding_two_digits(seconds)


def print_gametime(start_time):
    pass


def print_lives_remaining(lives):
    pass


def print_header(lives, start_time, score):
    """Print header row, including ANSI, etc."""
    remaining_lives = "Lives: " + lives


# Score is going to be calculated per round, and added to a cumulative game score.
#


def get_current_score():
    pass


def score_ratio():
    pass


def lives_decrement(lives):
    """Don't have a class or anything to do this with. Refactor someday."""
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
