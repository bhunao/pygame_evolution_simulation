import math
import random
import pygame
import sys

from typing import Any


class Food(pygame.sprite.Sprite):
    def __init__(self, *groups):
        print(groups)
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = random.randint(0, 350), random.randint(0, 350)

class Organism(pygame.sprite.Sprite):
    def __init__(self, *groups):
        print(groups)
        super().__init__(*groups)
        self.image = pygame.Surface((25, 25))
        self.rect = self.image.get_rect()
        self.rect.center = 250, 250

        self.angle = 0
        self.velocity = 0
        self.max_velocity = 3

        self.energy = 500
    
    def _energy_update(self):
        self.energy -= 0.1 * (abs(self.velocity) + 1)
    
    def eat(self, target: pygame.sprite.Sprite):
        if not hasattr(target, "life"):
            raise TypeError("target has no life attribute.")
        
        if target.life > 0:
            target.life -= 1
            self.energy += 1
        if target.life <= 0:
            target.kill()
    
    def _draw(self):
        half_size = self.rect.width // 2

        self.image.fill("darkred")
        x = half_size + math.cos(math.radians(self.angle)) * half_size
        y = half_size + math.sin(math.radians(self.angle)) * half_size
        pygame.draw.line(self.image, "white", (half_size, half_size), (x, y), 3)
    
    def move(self, movement: str):
        if movement == "accelerate":
            self.velocity += 1 if self.velocity <= self.max_velocity else 0
        if movement == "deacelereate":
            self.velocity -= 1 if self.velocity >= -self.max_velocity else 0
        if movement == "left":
            self.angle = (self.angle + 15) % 360
        if movement == "right":
            self.angle = (self.angle - 15) % 360

    def get_polar_pos(self):
        return (math.cos(math.radians(self.angle)) * self.velocity,
                math.sin(math.radians(self.angle)) * self.velocity)
    

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.get_polar_pos())
        self._energy_update()
        self._draw()
        print(f"{self.angle} | {self.velocity} | {self.rect}")
        return super().update(*args, **kwargs)


pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

groups = {
    "organisms": pygame.sprite.Group(),
    "food": pygame.sprite.Group(),
}

group = pygame.sprite.Group()
organism = Organism(groups["organisms"])
food = Food(groups["food"])


# game loop
while 1:
    # background
    screen.fill("gray")

    # get mouse position
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for group in groups.values():
        group.draw(screen)
        group.update()

    organism.move("accelerate")
    organism.move("left")

    pygame.display.flip()
    clock.tick(60)
