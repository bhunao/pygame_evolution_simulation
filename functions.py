import os
import neat
import pickle

from typing import List
from pygame import Rect, Surface
from pygame.font import SysFont


def survive_condition(entity , rect: Rect):
    return rect.collidepoint(*entity.pos)

def draw_text(surface: Surface, text: str | int, pos, size=15, color=(255, 255, 255), bold: bool = False):
    font = SysFont("Arial", size, bold)
    font.set_bold(True)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    surface.blit(text, text_rect)
    return text_rect

def create_neat_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    return config

def run_neat(config, eval_genomes):
    # Load the config file for the NEAT algorithm
    config = create_neat_config()

    # Create the population, which is the top-level object for a NEAT run
    p = neat.Population(config)
    # Load last population if exists
    # p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-998')

    # Add a stdout reporter to show progress in the terminal
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(499))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 5000)

    with open("best.pkl", "wb") as f:
        pickle.dump(winner, f)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

def get_max_position(n_list: List[int]):
    m = max(n_list)
    for i, value in enumerate(n_list):
        if value == m:
            return i
    raise ValueError

def add_winners_fitness(win_area, cells):
    win_rect = win_area.get_rect()
    for cell in cells:
        collided = win_rect.collidepoint(cell.pos)
        if collided:
            cell.genome.fitness += 10
