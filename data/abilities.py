from grid import SUNK_SHIP, SHIPS, Ship, Grid
import random

ABILITY = {
    "REPAIR": 1,
    "HITNRUN": 2,
    "TORPEDO": 3,
    "SCAN": 4, 
    "AIRSTRIKE": 5
}


class AbilityResult():

    def __init__(self, positions=[]):
        self.positions = positions


class AbilityController():

    def __init__(self, grid):
        self.grid = grid

    def repair(self, shipid):
        """
        Repairs a damaged ship to full health.
        """
        shipcells = self.grid.get_ship_status()[shipid]
        changed = []
        if SUNK_SHIP not in shipcells.values():
            changed = self.grid.repair_ship(shipid)
        return AbilityResult(changed)

    def hit_n_run(self):
        """
        A random enemy cell is damaged.
        There is a 25% chance the patrol boat is revealed.
        """
        statuses = self.grid.get_ship_status()
        positions = []
        for shipid in statuses:
            cells = statuses[shipid]
            for pos in cells:
                if cells[pos] == shipid:
                    positions.append(pos)
        if positions:
            attack = random.choice(positions)
            self.grid.shoot(attack)
            positions = [attack]
        return AbilityResult(positions)

    def emp(self, position):
        """
        Causes the enemy to skip a turn.
        This ability reveals the destroyer.
        """

    def torpedo(self, position):
        """
        If a ship is hit with this ability, the whole ship is sunk.
        This ability reveals the submarine.
        """
        hit = self.grid.shoot(position)
        if hit.cell in SHIPS:
            statuses = self.grid.get_ship_status()[hit.cell]
            for position in statuses:
                self.grid.shoot(position)
            positions = list(statuses.keys())
            return AbilityResult(positions)
        return AbilityResult([position])

    def scan(self, position):
        """
        Scans a 3x3 area around the position.
        This ability reveals the cruiser.
        """
        pass

    def airstrike(self, position):
        """
        Attacks 8 random cells in a 5x5 radius.
        This ability reveals the aircraft carrier.
        """
        x, y = position
        w, h = self.grid.dimensions()
        if x < 2: x = 2
        if x > w-3: x = w-3
        if y < 2: y = 2
        if y > h-3: y = h-3
        targets = set()
        while len(targets) < 8:
            rx = random.randint(x-2, x+2)
            ry = random.randint(y-2, y+2)
            targets.add((rx, ry))
        for pos in targets:
            self.grid.shoot(pos)
        return AbilityResult(list(targets))


if __name__ == "__main__":
    from pprint import pprint
    carrier = Ship(SHIPS[0], "Carrier", 5)
    cruiser = Ship(SHIPS[1], "Cruiser", 4)
    destroyer = Ship(SHIPS[2], "Destroyer", 3)

    grid = Grid(10, 10)
    grid.add_ship(carrier, (1,2), 1)
    grid.add_ship(cruiser, (1,4), 1)
    grid.add_ship(destroyer, (1,6), 1)

    abilities = AbilityController(grid)
    result = abilities.airstrike((1, 5))

    print(result.positions)

    grid.print()
