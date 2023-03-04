import sys
import pygame

from random import randint

from neat.nn import FeedForwardNetwork
from pygame import Rect, display, Surface, init, draw
from pygame.time import Clock ,get_ticks
from pygame.transform import scale


from config import configs
from functions import add_winners_fitness, create_neat_config, run_neat
from sprites.Cell import Cell


class BrainInterface:
    def __init__(self, cell: Cell, surface: Surface) -> None:
        self.cell = cell
        self.surface = surface
        
        for node in self.cell.brain.node_evals:
            _id = node[0]
            activation = node[1]
            agregation = node[2]
            weight = node[3]
            something = node[4]
            linked_nodes = node[5]
    
    def update(self):
        self.draw()

    def draw(self):
        layer1 = [-1, -2, -3]
        layer2 = [304]
        layer3 = [0, 1, 2 ,3 ,4]
        layers = layer1, layer2, layer3
        
        rect_list = []
        # for j, layer in enumerate(layers):
        #     print(j, layer)
        #     for i, node in enumerate(layer):
        #         x = 64*(j+1)
        #         y = 32*(i+1)
        #         rect = Rect(x, y, 16, 16)
        #         rect_list.append(rect)
        #         # draw.rect(self.surface, "white", rect)

        #         print((x, y), node, rect)
        
        # for i, n1 in enumerate(layer1):
        #     for j, n2 in enumerate(layer2):
        #         x = 64*(j+1)
        #         y = 32*(i+1)
        #         draw.line(self.surface, "red", (x, y), (x+32, y+32))
        
        for rect in rect_list:
            draw.rect(self.surface, "white", rect)


def main(genomes, config):
    init()
    WIDTH = configs["screen"]["width"]
    HEIGHT = configs["screen"]["height"]
    UPSCALE = configs["screen"]["upscale"]

    cells_list = []

    screen = display.set_mode((WIDTH*UPSCALE*2, HEIGHT*UPSCALE))
    side_panel = Surface((WIDTH, HEIGHT))
    down_scale_screen = Surface((WIDTH, HEIGHT))
    clock = Clock()
    end_tick = 10000 + get_ticks()

    win_rect = Surface((WIDTH*.35, HEIGHT*.35))
    win_rect.set_alpha(50)
    win_rect.fill("green")

    for genomed_id, genome in genomes:
        brain = FeedForwardNetwork.create(genome, config)
        x = randint(0, WIDTH-1)
        y = randint(0, WIDTH-1)

        cell = Cell((x,y), genome, brain, cells_list)
        cells_list.append(cell)
    
    brain_interface = BrainInterface(cells_list[-1], side_panel)


    while 1:
        down_scale_screen.fill("gray")
        down_scale_screen.blit(win_rect, (0, 0))

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
        brain_interface.update()

        if get_ticks() >= end_tick:
            add_winners_fitness(win_rect, cells_list)
            break

        scaled_win = scale(down_scale_screen, (WIDTH*UPSCALE, HEIGHT*UPSCALE))
        screen.blit(scaled_win, (0, 0))
        screen.blit(side_panel, (WIDTH*UPSCALE, 0))
        pygame.display.flip()
        # clock.tick(60)

def eval_genomes(genomes, config):
    main(genomes, config)


if __name__ == "__main__":
    config = create_neat_config()
    run_neat(config, eval_genomes)