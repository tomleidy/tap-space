"""Constants and defaults for the game itself"""

STARTING_LIVES = 10

# This is the variable that controls the speed of the game. Higher? slower game.
# This is as fast as it can go and still be cross-platform to my current understanding.
# Windows can only do 15.6ms timeouts. macOS can do it much faster.
INPUT_TIMEOUT = 0.0156

# descriptions will need updating once they're actually implemented
DIFFICULTIES = [
    {"name": "Easy",
        "desc": "speed reduced, racer & goal positions shown in (x,y) format"},
    {"name": "Normal", "desc": "maximum speed, positions hidden"},
    {"name": "Hard", "desc": "speed changes in a sine wave gradient"},
    {"name": "Ultra", "desc": "speed changes randomly every 3 places"},
    {"name": "Impossible", "desc": "goal moves off of track"}
]
# going to need to figure out custom goals for each of these
LEVELS = [
    {"name": "Hyphen", "desc": "horizontal line"},
    {"name": "Pipe", "desc": "vertical line"},
    {"name": "Plus", "desc": "plus sign shaped"},
    {"name": "Slash", "desc": "diagonal line, lower left to upper right"},
    {"name": "Backslash", "desc": "diagonal line, upper left to lower right"},
    {"name": "Multiplication", "desc": "a two diagonal lines, perpendicular"},
    {"name": "Asterisk", "desc": "star shaped"}
]
