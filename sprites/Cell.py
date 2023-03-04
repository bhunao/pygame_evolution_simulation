import neat

from pygame import Surface
from pygame.math import Vector2
from config import configs

from functions import get_max_position


class Cell:
    def __init__(self, pos, genome, brain, cells, *groups):
        super().__init__(*groups)
        self.pos = Vector2(pos)
        self.collided = False
        self.brain = brain
        self.genome = genome
        self.genome.fitness = 0
        self.cells = cells
        self.color = "black"

    def move(self, x=0, y=0):
        max_x = configs["screen"]["width"] - 1
        max_y = configs["screen"]["height"] - 1

        current_x = int(self.pos.x + x)
        current_y = int(self.pos.y + y)
        collided = self.collide(current_x, current_y)
        if (current_x < 0) or (current_x > max_x):
            return
        if (current_y < 0) or (current_y > max_y):
            return
            
        if collided is not None:
            self.colided = True
            return collided

        self.pos += Vector2(x, y)

    def update(self, surface: Surface):
        self.cellsor = "black"
        if self.brain is None:
            return

        output = self.brain.activate(self.senses())
        output_index = get_max_position(output)

        move_d = [
            (0, 0),    # stop
            (1, 0),    # up
            (0, 1),    # right
            (-1, 0),   # down
            (0, -1),   # left
        ]
        x, y = move_d[output_index]
        self.move(x, y)
        self.draw(surface)

    def senses(self):
        return self.pos.x, self.pos.y, self.collided

    def collide(self, x, y):
        self.color = "black"
        self.collided = False
        for cell in self.cells:
            if cell is not self and cell.pos == Vector2(x, y):
                self.color = "red"
                cell.color = "blue"
                self.collided = True
                return cell
        return None

    def draw(self, surface: Surface):
        x, y = int(self.pos.x), int(self.pos.y)
        surface.set_at((x, y), self.color)

