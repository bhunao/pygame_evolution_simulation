import math
import config as c
import neat
from matplotlib.pyplot import draw
import pygame

from organisms.food import Food

GREEN = (0, 255, 0)
max_dist = 30


class Cell:
    def __init__(self, screen, x, y, width, height, size, energy, color=GREEN):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.size = size
        self.velocity_x = 0
        self.velocity_y = 0
        self.max_velocity = 2
        self.size = 1
        self.energy = energy
        self.max_vision = 40
        self.eating = False
        self.vision = {'up': False, 'down': False, 'left': False, 'right': False}
        self.color = color
        self.sprite = pygame.Rect(self.x, self.y, self.width, self.height)

        self.angle = 0
        self.draw_angle()

        self.velocity = 1

    def draw_angle(self):
        size = 15
        p1 = (self.x, self.y)
        x2 = p1[0] + math.cos(math.radians(self.angle)) * size
        y2 = p1[1] + math.sin(math.radians(self.angle)) * size
        p2 = x2, y2
        pygame.draw.line(self.screen, "white", p1, p2, 3)
    
    def die(self):
        self.energy = 0
    
    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.center = (self.x, self.y)
        # self.size = self.energy / 1.5
        # self.sprite.width = self.size
        # self.sprite.height = self.size
        pygame.draw.rect(self.screen, self.color, self.sprite)
        self.draw_angle()
    
    def energy_consumption(self):
        self.energy -= .1 if self.velocity > 0 else .05
    
    def _update(self):
        pass

    def wall_limits(self):
        limit_x, limit_y = c.SCREEN_WIDTH, c.SCREEN_HEIGHT
        if self.x < 0:
            self.die()
            self.x = 0
        elif self.x > limit_x:
            self.x = limit_x
            self.die()
        if self.y < 0:
            self.y = 0
            self.die()
        elif self.y > limit_y:
            self.y = limit_y
            self.die()

    
    def update(self, collider_list):
        self.x += math.cos(math.radians(self.angle)) * self.velocity
        self.y += math.sin(math.radians(self.angle)) * self.velocity

        self._update_vision(collider_list)
        self.wall_limits()
        self.near_food(collider_list)
        self.collide_and_eat(collider_list)
        self.draw_vision(collider_list)
        self.energy_consumption() 
        self.draw()
        self.draw_angle()

        if self.energy <= 0:
            self.die()

        self._update()
    
    def move(self, direction):
        max_speed = self.max_velocity
        if direction == 'up':
            self.velocity += 1 if self.velocity < 3 else 3
            # self.velocity_y = -1 if self.velocity_y < max_speed else 0
        elif direction == 'down':
            self.velocity -= 1 if self.velocity > -3 else -3
            # self.velocity_y = 1 if self.velocity_y < max_speed else 0
        elif direction == 'left':
            # self.velocity_x = -1 if self.velocity_y < max_speed else 0
            self.angle -= 15
        elif direction == 'right':
            # self.velocity_x = 1 if self.velocity_y < max_speed else 0
            self.angle += 15
        else:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def eat(self, food: Food):
        energy_transfer = 1
        self.energy += energy_transfer
        food.energy -= energy_transfer
    
    def collide_and_eat(self, food_list):
        count = 0
        for i, collider in enumerate(food_list):
            if self.sprite.colliderect(collider.sprite):
                self.eat(collider)
                collider.collor = (255, 255, 0)
                self.eating = True
                count += 1
            else:
                self.eating = False
                self.color = GREEN
        self.food_nearby = count
    
    def collide(self, collider_list):
        for i, collider in enumerate(collider_list):
            if math.hypot(self.x - collider.x, self.y - collider.y) < max_dist:
                return i
            if self.sprite.colliderect(collider.sprite):
                return i
        return -1
    
    def draw_vision(self, collider_list):
        for collider in collider_list:
            if math.hypot(self.x - collider.x, self.y - collider.y) < self.max_vision:
                # pygame.draw.line(self.screen, self.color, (self.x, self.y), (collider.x, collider.y))
                # collider.color = (0, 255, 255)
                pass
    
    def _update_vision(self, collider_list):
        vision = {'up': False, 'down': False, 'left': False, 'right': False}
        for collider in collider_list:
            distance = math.hypot(self.x - collider.x, self.y - collider.y)
            if distance > self.max_vision:
                continue
            if self.x < collider.x:
                vision['right'] = True
            elif self.x > collider.x:
                vision['left'] = True
            if self.y < collider.y:
                vision['down'] = True
            elif self.y > collider.y:
                vision['up'] = True
        self.vision = vision
        return vision

    
    def near_food(self, food_list):
        # function draw line from cell to food
        def draw_line(cell, food):
            pygame.draw.line(self.screen, self.color, (cell.x, cell.y), (food.x, food.y), 1)
        

        up = False
        down = False
        left = False
        right = False

        for i, food in enumerate(food_list):
            if math.hypot(self.x - food.x, self.y - food.y) < self.size:
                # draw_line(self, food)
                if food.x > self.x:
                    right = True
                elif food.x < self.x:
                    left = True
                if food.y > self.y:
                    down = True
                elif food.y < self.y:
                    up = True
        return up, down, left, right


# class CellG inherits from Cell
# has an extra attribute called genome
# has a method called get_data()
class CellG(Cell):
    def __init__(self, screen, x, y, width, height, size, energy, config=None, genome=None, color=GREEN):
        super().__init__(screen, x, y, width, height, size, energy, color)
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.config = config
        self.genome = genome
    
    def _update(self):
        self.genome.fitness += 1
        # self.show_cell_info_on_screen()
        output = self.get_output()
        activate = self.net.activate(output)
        # move based on activate
        min_threshold = 1
        if activate[0] >= min_threshold:
            self.move('up')
        if activate[1] >= min_threshold:
            self.move('down')
        if activate[2] >= min_threshold:
            self.move('left')
        if activate[3] >= min_threshold:
            self.move('right')
        if activate[0] < min_threshold and activate[1] < min_threshold and activate[2] < min_threshold and activate[3] < min_threshold:
            self.move('none')

    
    def show_cell_info_on_screen(self):
        font = pygame.font.SysFont('Arial', 20)
        text = str(int(self.energy))
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.x, self.y))
        self.screen.blit(text, text_rect)
        # center text on cell
        # text.center = self.sprite.center
        # self.screen.blit(text, text.center)

    
    def get_output(self):
        data = [
            int(self.energy),
            (abs(self.velocity_x) + abs(self.velocity_y)) / 2,
            self.eating,
            self.food_nearby,
            self.x,
            self.y,
            *self.vision.values() # 5 values
        ]
        return data
    
    def set_fitness(self, n):
        self.net[1].fitness += n
    
    def output_to_movement(self):
        self.output = self.net[0].activate(self.get_output())
        if self.output == 0:
            self.move('left')
        elif self.output == 1:
            self.move('right')
        elif self.output == 2:
            self.move('up')
        elif self.output == 3:
            self.move('down')
    
    def draw_line_from_cell_to_food(self, food):
        pygame.draw.line(self.screen, self.color, (self.x, self.y), (food.x, food.y), 1)
        
    def eat(self, food: Food):
        energy_transfer = 1
        self.energy += energy_transfer
        food.energy -= energy_transfer
        food.color = (255, 255, 0)
        self.genome.fitness += 1
    
    def __str__(self):
        return f"CellG at ({self.x}, {self.y})"

