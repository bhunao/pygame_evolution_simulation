from typing import Iterable
import neat

from pygame import Surface
from pygame.math import Vector2
from config import configs

from functions import get_max_position

WIDTH = configs["screen"]["width"]
HEIGHT = configs["screen"]["height"]
DIRECTIONS = [
(0, 0),    # stop
(1, 0),    # up
(0, 1),    # right
(-1, 0),   # down
(0, -1),   # left
]


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
        self.direction = 0


    def move(self, x=0, y=0):
        max_x = WIDTH - 1
        max_y = HEIGHT - 1

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
    
    def rotate(self, angle):
        if angle == 0:
            return
        self.direction = (self.direction + angle) % 4
    


    def action_output(self):
        output = self.brain.activate(self.senser_neuron())
        output_index = get_max_position(output)


        output_params = [
            (0, 0),                             # stop
            (1, 0),                             # up
            (0, 1),                             # right
            (-1, 0),                            # down
            (0, -1),                            # left
            DIRECTIONS[self.direction],         # foward
            DIRECTIONS[(self.direction-2) % 4], # backwards
            1,                                  # rotate right
            -1,                                 # rotate left
        ]
        output_func = [
            self.move,
            self.move,
            self.move,
            self.move,
            self.move,
            self.move,
            self.move,
            self.rotate,
            self.rotate
        ]
        func = output_func[output_index]
        params = output_params[output_index]
        if isinstance(params, Iterable):
            func(*params)
        else:
            func(params)
        # print(func.__name__, params)

        # x, y = DIRECTIONS[output_index]
        # self.move(x, y)

    def update(self, surface: Surface):
        self.cellsor = "black"
        if self.brain is None:
            return

        self.action_output()
        self.draw(surface)

    def senser_neuron(self):
        normalized_x = (self.pos.x - 0) / (WIDTH - 0)
        normalized_y = (self.pos.y - 0) / (WIDTH - 0)
        data = [
                self.pos.x,
                self.pos.y,
                self.collided
        ]
        return data

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

