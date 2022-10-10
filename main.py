from venv import create
from neat_functions import create_neat_config, run_neat, run_best


if __name__ == '__main__':
    config = create_neat_config()
    run_neat(config)
    # run_best(config)
