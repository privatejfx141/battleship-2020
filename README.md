# battleship-2020
Yet another _Battleship_ implementation, but this time with decent AI.

## Files

* `game.py`: to be implemented, will contain the game itself built with Pygame.
* `grid.py`: contains the game grid and ships.
* `player.py`: contains the computer player logic. Currently two AI modes are implemented: the 'dumb' random shots and the hunting-targeting shots.

## Hunting-Targeting Algorithm

Credits to [DataGenetics](http://www.datagenetics.com/blog/december32011/) for explaining the algorithm.

The Hunting-Targeting algorithm is implemented using a stack of potential targets for the computer fire at. The computer can be in one of two modes: Hunt mode and Target mode. **Hunt** mode is the usually randomized firing to find a target. Once a ship is hit, the computer switches to **Target** mode, where it would add the surrounding grid squares to its stack to attack next.

Since the official rules of _Battleship_ state that you must tell your opponent if they have sunken your ship, the algorithm has been modified to reflect that. If a ship is sunk, the computer cannot just switch back to Hunt mode, as there may be another ship touching the previous ship. To solve this, a set is added for the computer to keep track of which ships it is currently attacking. Only when the set is empty (i.e. all targeted ships are sunk), will the computer go back to Hunt mode.
