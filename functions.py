import os
from typing import List
import neat
import pickle

from pygame.math import Vector2


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
    p.add_reporter(neat.Checkpointer(50))

    # Run for up to 300 generations.
    winner = p.run(eval_genomes, 1000)

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
