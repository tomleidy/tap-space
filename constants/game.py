"""Constants and defaults for the game itself"""

STARTING_LIVES = 10

# This is the variable that controls the speed of the game. Higher? slower game.
# This is as fast as it can go and still be cross-platform to my current understanding.
# Windows can only do 15.6ms timeouts. macOS can do it much faster.
INPUT_TIMEOUT = 0.0156
