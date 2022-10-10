import os
import neat
import pickle
from game import GameG
from screen import App


tst = True

def eval_genomes(genomes, config):
    # for i, (genome_id, genome) in enumerate(genomes):
    #     net = neat.nn.FeedForwardNetwork.create(genome, config)
    #     genome.fitness = 0

    sim = App(genomes, config)
    sim.run()

    if tst:
        return

    game = GameG()
    game.game_loop(genomes, config)


def run_neat(config):
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
    winner = p.run(eval_genomes, 300)

    with open("best.pkl", "wb") as f:
        pickle.dump(winner, f)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

def run_best(config):
    with open("best.pkl", "rb") as f:
        winner = pickle.load(f)
    n_cells = 30
    genomes = [
        (i, winner) for i in range(n_cells)
    ]
    sim = App(genomes, config)
    sim.run()

def create_neat_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                            neat.DefaultSpeciesSet, neat.DefaultStagnation,
                            config_path)
    return config
