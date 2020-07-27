from grid import WATER, SHIPS, HITS, SUNK_SHIP, SHIP_NAME, generate_grid
from random import randint, shuffle

HUNTING = 0
TARGETING = 1

DEBUG = True

def log(message):
    print(message)
        

class Player(object):
    """A computer player for battleship."""

    def __init__(self, grid, name):
        self._grid = grid
        self.name = name
        self.shots = set()

    def fire(self):
        return None

class DumbPlayer(Player):
    """A player that only fires at random positions"""

    def __init__(self, grid, name):
        Player.__init__(self, grid, name)

    def fire(self):
        grid = self._grid
        width, height = grid.dimensions()

        valid_hit = False
        while not valid_hit:
            pos = (randint(0, width-1), randint(0, height-1))
            hit = grid.shoot(pos)
            valid_hit = hit not in HITS
            # if hit is valid
            if hit in SHIPS:
                log("Hit a ship at " + str(pos))
            elif hit == WATER:
                log("Missed at " + str(pos))
            if valid_hit:
                self.shots.add(pos)
        return hit


class HuntingTargetingPlayer(Player):
    """
    A player that uses randomized hunting and targeting approach, remembering
    the next positions to attack using a stack.
    """
    def __init__(self, grid, name):
        Player.__init__(self, grid, name)
        self._stack = list()
        self._mode = HUNTING
        self._target_ships = set()

    def _get_neighbours(self, position):
        """(HuntingPlayer, (int, int)) -> [(int, int)]
        Returns a list of unhit neighbour positions around the given position.
        """
        grid = self._grid
        x, y = position
        neighbours = []
        offsets = [(0,1),(1,0),(0,-1),(-1,0)]
        shuffle(offsets)
        for offset in offsets:
            i, j = offset
            position = (x + i, y + j)
            if grid.valid_position(position) and position not in self.shots:
                neighbours.append(position)
        return neighbours

    def _hunting_mode(self):
        """(HuntingPlayer) -> NoneType
        Hunting mode; the player shoots at random cells until it hits a ship.
        """
        grid = self._grid
        width, height = grid.dimensions()
        valid_shot = False
        while not valid_shot:
            pos = (randint(0, width-1), randint(0, height-1))
            hit = grid.shoot(pos)
            shot = hit.cell
            valid_shot = shot not in HITS
            # if shot is valid
            if shot in SHIPS:
                self._stack += self._get_neighbours(pos)
                self._mode = TARGETING
                log("[HUNT]: Hit a ship at " + str(pos) + ", going into targeting.")
            elif shot == WATER:
                log("[HUNT]: Missed at " + str(pos))
            if valid_shot:
                self.shots.add(pos)
        return shot

    def _targeting_mode(self):
        """(HuntingPlayer) -> NoneType
        Targeting mode; the player uses a stack of potential targets to shoot
        at. Once the stack is empty, the player returns to hunting mode. 
        """
        if self._stack:
            pos = self._stack.pop(0)
            hit = grid.shoot(pos)
            shot = hit.cell
            # if we hit a ship
            if shot in SHIPS:
                self._target_ships.add(shot)
                self._stack += self._get_neighbours(pos)
                # if we sunk a ship
                if hit.result == SUNK_SHIP:
                    self._target_ships.remove(shot)
                    log("[TARGET]: Sunk " + SHIP_NAME[shot] + " at " + str(pos))
                    if not self._target_ships:
                        self._stack = []
                        self._mode = HUNTING
                        log("[TARGET]: All targets destroyed, return to hunt.")
                # if we just hit a ship
                else:
                    log("[TARGET]: Hit a ship at " + str(pos))
            elif shot == WATER:
                log("[TARGET]: Missed at " + str(pos))
            # if we already hit the position
            if shot in HITS:
                shot = self.fire()
            else:
                self.shots.add(pos)
            return shot
        # if stack is empty, go back to hunting mode
        else:
            self._mode = HUNTING
            return self.fire()

    def fire(self):
        shot = None
        width, height = self._grid.dimensions()
        if len(self.shots) >= width * height:
            log("Cannot fire any more shots.")
            return shot
        if self._mode == HUNTING:
            shot = self._hunting_mode()
        else:
            shot = self._targeting_mode()
        return shot


if __name__ == "__main__":
    from pprint import pprint
    import time

    grid = generate_grid()
    player = HuntingTargetingPlayer(grid, "Tester")
    for i in range(101):
        player.fire()
        grid.print()
