import logging

# setup logging messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# constants

# screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TITLE = 'Game'
FPS = 60

# colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)

# cell
CELL_BASE_SIZE = 20
CELL_BASE_ENERGY = 15
CELL_COUNT = 10

# food
FOOD_BASE_SIZE = 3
FOOD_COUNT = 1000