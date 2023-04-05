
from enum import Enum
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

class Directions(Enum):
    STOP = (0, 0)    # STOP
    UP = (1, 0)    # UP
    RIGHT = (0, 1)    # RIGHT
    DOWN = (-1, 0)   # DOWN
    LEFT = (0, -1)   # LEFT

class ActionOutput(Enum):
    STOP = 0
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    FOWARD = 5
    BACKWARDS = 6
    ROTATE_RIGHT = 7
    ROTATE_LEFT = 8


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
            Directions.STOP.value,
            Directions.UP.value,
            Directions.RIGHT.value,
            Directions.DOWN.value,
            Directions.LEFT.value,
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

        if output_index == 0:
            self.move(*Directions.STOP.value)
        elif output_index == 1:
            self.move(*Directions.UP.value)
        elif output_index == 2:
            self.move(*Directions.RIGHT.value)
        elif output_index == 3:
            self.move(*Directions.DOWN.value)
        elif output_index == 4:
            self.move(*Directions.LEFT.value)
        elif output_index == 5:
            direct = DIRECTIONS[self.direction]
            self.move(*direct)
        elif output_index == 6:
            direct = DIRECTIONS[(self.direction + 2) % 4]
            self.move(*direct)
        elif output_index == 7:
            self.rotate(1)
        elif output_index == 8:
            self.rotate(-1)

        # func = output_func[output_index]
        # params = output_params[output_index]
        # if isinstance(params, Iterable):
        #     func(*params)
        # else:
        #     func(params)

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

