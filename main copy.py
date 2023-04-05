import sys
import pygame

from random import randint

from neat.nn import FeedForwardNetwork
from pygame import Rect, display, Surface, init
from pygame.time import Clock, get_ticks
from pygame.transform import scale


from config import configs
from functions import create_neat_config, draw_text, run_neat, survive_condition
from system import System, Entity


class Cell(Entity):
    def __init__(self, brain, genome, pos=[0,0]) -> None:
        self.brain = brain
        self.genome = genome
        self.genome.fitness = 0
        self.pos = pos

def main(genomes, config):
    init()
    WIDTH = configs["screen"]["width"]
    HEIGHT = configs["screen"]["height"]
    UPSCALE = configs["screen"]["upscale"]

    X = 256
    WIDTH = X
    HEIGHT = X
    UPSCALE = 2

    screen = display.set_mode((WIDTH*UPSCALE, HEIGHT*UPSCALE))
    down_scale_screen = Surface((WIDTH, HEIGHT))
    step = 0
    max_step = X * 2

    survive_surf = Surface((WIDTH*.20, HEIGHT*.20))
    survive_surf.set_alpha(50)
    survive_surf.fill("green")
    survive_rect =  survive_surf.get_rect()


    s = System(down_scale_screen)

    for genomed_id, genome in genomes:
        brain = FeedForwardNetwork.create(genome, config)
        MARGIN = int(X * 0.25)
        x = randint(0 + MARGIN, WIDTH-1 - MARGIN)
        y = randint(0 + MARGIN, WIDTH-1 - MARGIN)

        entity = Cell(brain, genome, [x, y])
        s._entities.append(entity)

    down_scale_screen.blit(survive_surf, (0, 0))
    while True:
        down_scale_screen.fill("gray")
        down_scale_screen.blit(survive_surf, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        # if get_ticks() >= end_tick:
        step += 1
        if step >= max_step:
            # TODO: increase fitness of "winning" cells
            survivors = filter(lambda e: survive_condition(e, survive_rect), s._entities)

            def add_fitness(entity: Cell):
                entity.genome.fitness += 10

            [_ for _ in map(add_fitness, survivors)]
            s._entities.clear()
            break
        
        for entity in s._entities:
            s.draw(entity)
            s.action_output(entity, (WIDTH, HEIGHT), survive_condition(entity, survive_rect))

        scaled_win = scale(down_scale_screen, (WIDTH*UPSCALE, HEIGHT*UPSCALE))
        draw_text(scaled_win, max_step - step, (20, 20), 15)
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        # clock.tick(30)

def eval_genomes(genomes, config):
    main(genomes, config)


if __name__ == "__main__":
    config = create_neat_config()
    run_neat(config, eval_genomes)