from random import randint
import sys
import numpy as np
import pygame, neat
from functions import create_neat_config, run_neat
from pygame.time import get_ticks
from pygame.transform import scale

from sprites.Cell import Cell
from config import configs


def main(genomes, config):
    pygame.init()
    WIDTH = configs["screen"]["width"]
    HEIGHT = configs["screen"]["height"]
    UPSCALE = configs["screen"]["upscale"]

    cells_list = []

    screen = pygame.display.set_mode((WIDTH*UPSCALE, HEIGHT*UPSCALE))
    screen.set_alpha(None)
    down_scale_screen = pygame.Surface((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    current_tick = get_ticks()
    ticks_to_finish = 5000 + get_ticks()

    rect_surface = pygame.Surface((WIDTH*.5, HEIGHT))
    rect_surface.set_alpha(50)
    rect_surface.fill("green")



    for genomed_id, genome in genomes:
        brain = neat.nn.FeedForwardNetwork.create(genome, config)
        x = randint(0, WIDTH-1)
        y = randint(0, WIDTH-1)

        cell = Cell((x,y), genome, brain, cells_list)
        cells_list.append(cell)


    while 1:
        down_scale_screen.fill("gray")
        down_scale_screen.blit(rect_surface, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        
        for c in cells_list:
            c.update(down_scale_screen)
            c.draw(down_scale_screen)

        scaled_win = scale(down_scale_screen, screen.get_size())
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        clock.tick(60)

        current_tick = get_ticks()
        if current_tick >= ticks_to_finish:
            rect_area = rect_surface.get_rect()
            for c in cells_list:
                collided = rect_area.collidepoint(c.pos)
                if collided:
                    c.genome.fitness += 10
            break

def eval_genomes(genomes, config):
    main(genomes, config)


if __name__ == "__main__":
    config = create_neat_config()
    run_neat(config, eval_genomes)