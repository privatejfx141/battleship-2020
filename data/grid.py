from random import randint, choice

# orientation enums
VERTICAL = 0
HORIZONTAL = 1

# battleship type enums
CARRIER = 1
CRUISER = 2
DESTROYER = 3
SUBMARINE = 4
BOAT = 5
SHIPS = [CARRIER, CRUISER, DESTROYER, SUBMARINE, BOAT]
SHIP_NAME = {
    CARRIER: "Carrier",
    CRUISER: "Cruiser",
    DESTROYER: "Destroyer",
    SUBMARINE: "Submarine",
    BOAT: "Boat"
}

# tile type enums
WATER = 0
HIT_WATER = -1
HIT_SHIP = -2
SUNK_SHIP = -3
HITS = [HIT_WATER, HIT_SHIP, SUNK_SHIP]


class OutOfBoundsException(Exception):
    pass


class Ship(object):

    def __init__(self, shipid, name, length):
        self.id = shipid
        self.name = name
        self.length = length
        self.positions = None

class HitResult(object):
    
    def __init__(self, position, cell, result):
        self.cell = cell
        self.position = position
        self.result = result


class Grid(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        # empty dict means all water
        self.cells = dict()
        self.ships = list()

    def dimensions(self):
        return self._width, self._height

    def valid_position(self, position):
        x, y = position
        width, height = self._width, self._height
        return x >= 0 and x < width and y >= 0 and y < height

    def add_ship(self, ship, position, orientation=VERTICAL):
        # check if placable
        positions = []
        x, y = position
        for i in range(ship.length):
            x0 = x
            y0 = y
            if orientation == VERTICAL:
                y0 = y + i
            else:
                x0 = x + i
            position = (x0, y0)
            if self.valid_position(position) and position not in self.cells:
                positions.append((x0, y0))
            else:
                return []
        # place ship
        ship.positions = positions
        for position in positions:
            self.cells[position] = ship.id
        self.ships.append(ship)
        return positions

    def repair_ship(self, shipid):
        """(Grid, int) -> [(int, int)]
        Repairs a ship back to full health.
        Returns a list of affected cells.
        """
        ship = None
        for s in self.ships:
            if s.id == shipid:
                ship = s
                break
        changed = []
        for pos in ship.positions:
            if self.cells[pos] != shipid:
                changed.append(pos)
                self.cells[pos] = shipid
        return changed

    def get_ship_status(self):
        ship_data = dict()
        for ship in self.ships:
            cell_data = dict()
            for pos in ship.positions:
                cell_data[pos] = self.cells[pos]
            ship_data[ship.id] = cell_data
        return ship_data

    def shoot(self, position):
        if not self.valid_position(position):
            msg = str(position) + " is not a valid position."
            raise OutOfBoundsException(msg)
        cells = self.cells
        cell = None
        if position not in cells:
            cell = WATER
            cells[position] = HIT_WATER
        else:
            cell = cells[position]
            # if we hit a ship
            if cell in SHIPS:
                cells[position] = HIT_SHIP
                # check if ship is destroyed
                ship_status = self.get_ship_status()[cell]
                sunken = True
                for pos in ship_status:
                    sunken = sunken and ship_status[pos] == HIT_SHIP
                if sunken:
                    for pos in ship_status:
                        cells[pos] = SUNK_SHIP
        return HitResult(position, cell, cells[position])

    def print(self):
        cells = self.cells
        for y in range(self._height):
            row = ""
            for x in range(self._width):
                if (x,y) not in cells:
                    row += " ~"
                else:
                    cell = cells[(x,y)]
                    # if cell is a ship
                    if cell in SHIPS:
                        row += " ="
                    # if cell is a water hit
                    elif cell == HIT_WATER:
                        row += " ."
                    # if cell is a ship hit
                    elif cell == HIT_SHIP:
                        row += " x"
                    # if cell is a sunk ship:
                    else:
                        row += " X"
            print(row)


def generate_grid():
    grid = Grid(10, 10)
    carrier = Ship(CARRIER, "Carrier", 5)
    cruiser = Ship(CRUISER, "Cruiser", 4)
    destroyer = Ship(DESTROYER, "Destroyer", 3)
    sub = Ship(SUBMARINE, "Submarine", 3)
    boat = Ship(BOAT, "Patrol Boat", 3)
    for ship in [carrier, cruiser, destroyer, sub, boat]:
        valid_placement = False
        while not valid_placement:
            pos = [randint(0, 9), randint(0, 9)]
            orient = choice([VERTICAL, HORIZONTAL])
            valid_placement = grid.add_ship(ship, pos, orient) != []
    return grid


if __name__ == "__main__":
    from pprint import pprint
    carrier = Ship(CARRIER, "Carrier", 5)
    cruiser = Ship(CRUISER, "Cruiser", 4)
    destroyer = Ship(DESTROYER, "Destroyer", 3)

    grid = Grid(10, 10)
    grid.add_ship(carrier, (1,2), HORIZONTAL)
    grid.add_ship(cruiser, (1,4), HORIZONTAL)
    grid.add_ship(destroyer, (1,6), HORIZONTAL)

    grid.shoot((1,2))
    grid.shoot((2,2))
    grid.shoot((3,2))
    grid.shoot((4,2))
    grid.shoot((5,2))
    grid.shoot((6,2))
    grid.shoot((1,4))
    grid.print()
