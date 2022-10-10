import random
import neat
import pygame
import config
from info_screen import InfoScreen
from network_info import draw_network
from organisms.cell import CellG as Cell
from organisms.cell import Cell as C
from organisms.food import Food


class Game:
    def __init__(self):
        self.running = True

    def run(self):
        self.game_loop()

    def create_window(self):
        pygame.init()
        screen = pygame.display.set_mode((config.SCREEN_WIDTH + 300, config.SCREEN_HEIGHT))
        pygame.display.set_caption(config.TITLE)
        return screen

    def create_cells(self, screen):
        cells = []
        for i in range(config.CELL_COUNT):
            cells.append(
                Cell(screen,
                    x=400,
                    y=350,
                    width=config.CELL_BASE_SIZE,
                    height=config.CELL_BASE_SIZE,
                    size=config.CELL_BASE_SIZE,
                    energy=config.CELL_BASE_ENERGY
                    )
            )
        return cells

    # fuinction that create the food objects randomly and return them
    def create_food(self, screen):
        food = []
        for i in range(config.FOOD_COUNT):
            rand_x = random.randint(0, config.SCREEN_WIDTH)
            rand_y = random.randint(0, config.SCREEN_HEIGHT)
            food.append(
                Food(screen,
                    x=rand_x,
                    y=rand_y,
                    width=config.FOOD_BASE_SIZE,
                    height=config.FOOD_BASE_SIZE,
                    energy=config.FOOD_BASE_SIZE
                    )
            )
        return food

    # create infos screen from info_screen.py and return it
    def create_infos_screen(self, screen):
        return InfoScreen(screen, 50, 50, "abulabula")

    def movement_events(self, event, cell):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                cell.move('up')
            elif event.key == pygame.K_DOWN:
                cell.move('down')
            elif event.key == pygame.K_LEFT:
                cell.move('left')
            elif event.key == pygame.K_RIGHT:
                cell.move('right')

    def game_update(self, screen, clock, cells, foods, info_screen):
        # update screen
        screen.fill(config.BLACK)
        for i, cell in enumerate(cells):
            cell.update(foods)

            if cell.energy <= 0:
                cell.die()
                cells.pop(i)

            cell.near_food(foods)
            cell.collide_and_eat(foods)
            cell.draw_vision(foods)

        for food in foods:
            if food.energy <= 0:
                foods.pop(foods.index(food))
                continue
            food.update()

        if cells:
            first = cells[0]
            pygame.draw.rect(screen,  "pink", cell.sprite, 3)
            draw_network(screen, first)
            # print(first)
            info_screen_text = f'{int(first.energy)}|{first.x}, {first.y}\n{len(cells)} cells\n{len(foods)} foods'
            info_screen.update(info_screen_text)
        else:
            self.running = False

        pygame.display.update()
        # set FPS
        # clock.tick(config.FPS)

    def game_event_handler(self, cells):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            for cell in cells:
                self.movement_events(event, cell)


    def game_loop(self):
        clock = pygame.time.Clock()
        screen = self.create_window()
        cells = self.create_cells(screen)
        foods = self.create_food(screen)
        info_screen = self.create_infos_screen(screen)
        # main game loop
        while self.running:
            # event handling loop
            self.game_event_handler(cells)
            # update game objects
            self.game_update(screen, clock, cells, foods, info_screen)


class GameG(Game):
    def game_loop(self, genomes, config):
        clock = pygame.time.Clock()
        screen = self.create_window()
        cells = self.create_cells(screen, config, genomes)
        foods = self.create_food(screen)
        info_screen = self.create_infos_screen(screen)
        # main game loop
        while self.running:
            # event handling loop
            self.game_event_handler(cells)
            # update game objects
            self.game_update(screen, clock, cells, foods, info_screen)

    def create_cells(self, screen, g_config, genomes):
        cells = []
        # for i in range(config.CELL_COUNT):
        for genome_id, genome in genomes:
            genome.fitness = 0
            x = random.randint(0, config.SCREEN_WIDTH)
            y = random.randint(0, config.SCREEN_HEIGHT)
            cells.append(
                Cell(screen,
                    x=x,
                    y=y,
                    width=config.CELL_BASE_SIZE,
                    height=config.CELL_BASE_SIZE,
                    size=config.CELL_BASE_SIZE,
                    energy=config.CELL_BASE_ENERGY,
                    config=g_config,
                    genome=genome
                    )
            )
        return cells

    def create_food(self, screen):
        food = []
        for i in range(config.FOOD_COUNT):
            rand_x = random.randint(config.SCREEN_WIDTH/10, config.SCREEN_WIDTH/10*9)
            rand_y = random.randint(config.SCREEN_HEIGHT/10, (config.SCREEN_HEIGHT/10)*9)
            food.append(
                Food(screen,
                    x=rand_x,
                    y=rand_y,
                    width=config.FOOD_BASE_SIZE,
                    height=config.FOOD_BASE_SIZE,
                    energy=config.FOOD_BASE_SIZE
                    )
            )
        return food

