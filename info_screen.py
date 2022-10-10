import pygame


WHITE = (255, 255, 255)

class InfoScreen:
    def __init__(self, screen, x, y, text, color=WHITE):
        self.screen = screen
        self.text = text
        self.font = pygame.font.SysFont("arial", 30)
        self.color = color
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.rect.center = (x, y)

    def draw(self):
        self.screen.blit(self.text_surface, self.rect)

    def update(self, text):
        self.text = text
        self.text_surface = self.font.render(self.text, True, self.color)
        self.rect = self.text_surface.get_rect()
        self.draw()