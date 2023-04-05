import sys
import pygame

import config

from abc import ABC
from typing import List, Sequence

from pygame import display, Surface, init
from pygame.time import Clock
from pygame.transform import scale

from functions import get_max_position


class Entity(ABC):
    pos: Sequence[int] = [0, 0]

class System(ABC):
    _entities: List[Entity] = []
    surface: Surface

    def __init__(self, surface: Surface) -> None:
        self.surface = surface

    def draw(self, entity: Entity) -> bool:
        self.surface.set_at(entity.pos, "red")
        return True

    # @staticmethod
    def move(self, entity: Entity, pos: Sequence[int], max=(400, 400)) -> bool:
        x, y = entity.pos
        px, py = pos
        new_pos = x+px, y+py

        for collid_entity in filter(lambda e: e.pos[0] == new_pos[0] and e.pos[1] == new_pos[1], self._entities):
            if collid_entity is not entity:
                return False

        x0, y0 = entity.pos
        x1, y1 = max
        if x0 > 0 and x0 < x1:
            entity.pos[0] += pos[0]
        if y0 > 0 and y0 < y1:
            entity.pos[1] += pos[1]

        return True
    
    def action_output(self, entity: Entity, max=None, survive=False):
        output = entity.brain.activate(self.neuron_input_data(entity, survive))
        output_index = get_max_position(output)
        mov = [0, 0]

        if output_index == 0:
            mov = [0, 0]
        elif output_index == 1:
            mov = [0, 1]
        elif output_index == 2:
            mov = [0, -1]
        elif output_index == 3:
            mov = [1, 0]
        elif output_index == 4:
            mov = [-1, 0]

        if max:
            self.move(entity, mov, max)
            return True
        self.move(entity, mov)
        return True

    @staticmethod
    def neuron_input_data(entity: Entity, survive: bool):
        return [
            entity.pos[0],
            entity.pos[1],
            survive
        ]

def main():
    init()
    UPSCALE = 5
    WIDTH = config.WIDTH / UPSCALE
    HEIGHT = config.HEIGHT / UPSCALE

    screen = display.set_mode((WIDTH*UPSCALE, HEIGHT*UPSCALE))
    down_scale_screen = Surface((WIDTH, HEIGHT))
    clock = Clock()

    s = System(down_scale_screen)
    p = Entity()

    while True:
        down_scale_screen.fill("gray")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        
        s.draw(p)
        s.move(p, [1, 1])
        scaled_win = scale(down_scale_screen, (WIDTH*UPSCALE, HEIGHT*UPSCALE))
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        clock.tick(15)

if __name__ == '__main__':
    main()