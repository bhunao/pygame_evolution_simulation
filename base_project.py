import sys
import pygame

from random import randint

from neat.nn import FeedForwardNetwork
from pygame import display, Surface, init
from pygame.time import Clock ,get_ticks
from pygame.transform import scale


from config import configs
from functions import add_winners_fitness, create_neat_config, run_neat
from sprites.Cell import Cell


def main(genomes, config):
    init()
    WIDTH = configs["screen"]["width"]
    HEIGHT = configs["screen"]["height"]
    UPSCALE = configs["screen"]["upscale"]

    cells_list = []

    screen = display.set_mode((WIDTH*UPSCALE, HEIGHT*UPSCALE))
    screen.set_alpha(None)
    down_scale_screen = Surface((WIDTH, HEIGHT))
    clock = Clock()
    end_tick = 5000 + get_ticks()

    rect_surface = Surface((WIDTH*.5, HEIGHT))
    rect_surface.set_alpha(50)
    rect_surface.fill("green")

    for genomed_id, genome in genomes:
        brain = FeedForwardNetwork.create(genome, config)
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
        
        for cell in cells_list:
            cell.update(down_scale_screen)

        if get_ticks() >= end_tick:
            add_winners_fitness(rect_surface, cells_list)
            break

        scaled_win = scale(down_scale_screen, screen.get_size())
        screen.blit(scaled_win, (0, 0))
        pygame.display.flip()
        clock.tick(60)

def eval_genomes(genomes, config):
    main(genomes, config)


if __name__ == "__main__":
    config = create_neat_config()
    run_neat(config, eval_genomes)