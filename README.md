# Q-learning

This repository contains a basic Q-learning algorithm implemented in Python

It learns by pitting two opposing Q-learners against each other in a game of tic-tac-toe

# Coordinate System
    r0c0|r0c1|r0c2
    --------------
    r1c0|r1c1|r1c2
    --------------
    r2c0|r2c1|r2c2

# Example
Below is one entry from the final Q-Matrix from 10000 training games:

    ((('o', 'x', ''),
    ('', 'x', 'o'),
    ('', '', '')),

    {Move(r=2, c=0): 80.0, Move(r=1, c=0): 0.0, Move(r=0, c=2): 80.0, Move(r=2, c=1): 100.0, Move(r=2, c=2): 0.0}),

This Q-matrix ranks X's moves, and it does so by assigning a score to each possible move coordinate.

Here we see that it ranks the winning move r2c1 as being the highest from this board state with a score of 100.
The two moves which lead to a possible win in one move, r2c0 and r0c2, are ranked lower with 80s.
The remaining moves which don't lead to immediate victories and are ranked 0.