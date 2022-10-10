import pygame

RED = (255, 0, 0)
BASE_ENERGY_VALUE = 10

class Food:
    def __init__(self, screen, x, y, width, height, color=RED ,energy=BASE_ENERGY_VALUE):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.energy = energy
        self.sprite = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        self.width = self.energy
        self.height = self.energy
        self.sprite.center = (self.x, self.y)
        self.sprite.width = self.width
        self.sprite.height = self.height
        pygame.draw.rect(self.screen, self.color, self.sprite)
        self.color = RED
    
    def die(self):
        self.energy = 0 
    
    def update(self):
        self.draw()
        if self.energy <= 0:
            self.die()