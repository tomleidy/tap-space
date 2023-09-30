

def padding_two_digits(num):
    if num < 10:
        return "0" + str(num)
    elif num > 99:
        return "99"
    elif num >= 10 and num <= 99:
        return str(num)
    else:
        return "dd"


def seconds_to_mmss(gametime):
    if gametime > 3600:
        end_game(timeout_message)
    minutes = gametime % 60
    seconds = gametime - (minutes * 60)
    return padding_two_digits(minutes)+":"+padding_two_digits(seconds)


"""
def print_header(score):
    global lives
    remaining_lives = "Lives: " + lives
    time = "

    print(term.move_xy(0, 0) + reverse + )
def score_ratio()
def lives_decrement():
    global remaining_lives -= 1

def highscores_load
def highscores_save
def random
"""
