import pickle
from pprint import pprint as print
from neat_functions import create_neat_config


with open("best.pkl", "rb") as f:
    winner = pickle.load(f)

w = winner
n = w.nodes
c = w.connections
config = create_neat_config()
i = config.genome_config.input_keys
o = config.genome_config.output_keys

print(w.fitness)
print(n)
print(c)