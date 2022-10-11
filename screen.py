import math
from random import randint
from typing import Any, Dict, List

import pygame
from pygame.locals import *
from pygame.sprite import Group, RenderUpdates
from pygame.surface import Surface

from neat.nn import FeedForwardNetwork


MAX_DIST = 200


def draw_text(_screen, text, pos, size=15, color=(255, 255, 255), bold=False):
    font = pygame.font.SysFont("Arial", size, bold)
    font.set_bold(True)
    text = font.render(str(text), True, color)
    text_rect = text.get_rect()
    text_rect.center = pos
    _screen.blit(text, text_rect)
    return text_rect


class App:
    def __init__(self, genomes=None, config=None):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 800))
        self.clock = pygame.time.Clock()
        self.running = True
        self.groups: Dict[str, Group] = dict()

        self.create_sprites(genomes, config)

        # parts
        self.side = Side(self.groups)
        first = self.groups["main"].sprites()[0]
        self.sprite_attributes = SpriteAttributes(first, self.clock)

    def stop_on_extinctin(self):
        if len(self.groups["main"].sprites()) <= 0:
            print("exinct!")
            self.running = False

    def run(self):
        self.screen.fill("darkgreen")
        pygame.display.flip()

        while self.running:
            self.event_manager()
            self.update_and_display()
            self.stop_on_extinctin()
            # print(self.clock.tick(60))
            # print(self.clock.get_fps())

    def event_manager(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.quit()
        if pygame.mouse.get_pressed()[0]:
            sprites = self.groups["main"].sprites()
            mouse_rect = Rect(0, 0, 1, 1)
            mouse_rect.center = mouse_pos
            index = mouse_rect.collidelist(sprites)
            if index >= 0:
                selected_sprite = sprites[index]
                self.sprite_attributes = SpriteAttributes(selected_sprite, self.clock)


    def update_and_display(self):
        self.screen.fill("darkgreen")
        dirt = self.update()
        pygame.display.update(dirt)
        pygame.display.flip()

    def quit(self):
        print(f"quiting... {self.running=}")
        pygame.quit()

    def update(self):
        rect = Rect(
            self.screen.get_rect().width // 2,
            self.screen.get_rect().height // 2,
            MAX_DIST,
            MAX_DIST,
        )
        rect.center = self.screen.get_rect().width // 2, self.screen.get_rect().height // 2,
        pygame.draw.rect(self.screen, "blue", rect)

        side = self.side.update(self.screen)
        attrs = self.sprite_attributes.update(self.screen)
        dirt = [
            side,
            attrs,
            rect,
        ]
        for group in self.groups.values():
            group_dirt = group.draw(self.screen)
            group.update()
            dirt.extend(group_dirt)
        return dirt

    def create_sprites(self, genomes: List, config):
        max_x, max_y = self.screen.get_size()
        for genome_id, genome in genomes:
            org = Organism()
            org.create_network(genome, config)
            org.rect.center = randint(0, max_x), randint(0, max_y)
            self.add_to_group(org, "main")
        for _ in range(1):
            org = Food()
            self.add_to_group(org, "food")

    def add_to_group(self, sprite, group_name):
        group = self.groups.get(group_name, RenderUpdates())
        group.add(sprite)
        self.groups[group_name] = group


class Food(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((10, 10))
        self.image.fill("orange")
        self.rect = self.image.get_rect()
        self.rect.center = randint(0, 350), randint(0, 350)


class Organism(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = 250, 250

        self.angle = 0
        self.velocity = 0
        self.max_velocity = 3

        self.energy = 100

    def create_network(self, genome, config):
        self.net = FeedForwardNetwork.create(genome, config)
        self.genome = genome
        self.genome.fitness = 0
    
    def network_move(self):
        if not hasattr(self, "net"):
            raise BaseException("theres no network in this organism")
        
        inp = self.network_inputs()
        self.inputs = inp
        activate = self.net.activate(inp)

        possible_moves = [
            "accelerate",
            "deacelereate",
            "left",
            "right",
        ]

        min_threshold = 0.6
        if activate[0] >= min_threshold:
            self.move(possible_moves[0])
        if activate[1] >= min_threshold:
            self.move(possible_moves[1])
        if activate[2] >= min_threshold:
            self.move(possible_moves[2])
        if activate[3] >= min_threshold:
            self.move(possible_moves[3])
    
    def network_inputs(self):
        _screen = self.get_screen()
        mid = _screen[0] // 2, _screen[1] // 2


        x ,y = self.rect.center
        dist = int(math.hypot(mid[0] - x, mid[1] - y))
        return [
            self.rect.x,
            self.rect.y,
            dist,
            dist < MAX_DIST // 2,
        ]
    
    @staticmethod
    def get_screen():
        return pygame.display.get_surface().get_rect().size

    def _energy_update(self):
        self.energy -= 1
        
        _screen = self.get_screen()
        mid = _screen[0] // 2, _screen[1] // 2


        dist = int(math.hypot(mid[0] - self.rect.x, mid[1] - self.rect.y))
        # print(self.energy)

        half_size = self.rect.width // 2
        # draw_text(self.image, dist, (half_size, half_size), 10)

        self.fitness_function()

    def get_dist_from_center(self):
        _screen = self.get_screen()
        mid = _screen[0] // 2, _screen[1] // 2
        return int(math.hypot(mid[0] - self.rect.x, mid[1] - self.rect.y))
    
    def fitness_function(self):
        # if self.energy >= 0:
        #     return


        if self.get_dist_from_center() < MAX_DIST:
            self.genome.fitness += .1

        if self.energy <= 0:
            self.genome.fitness += 100
            self.kill()


    
    def eat(self, target: pygame.sprite.Sprite):
        if not hasattr(target, "life"):
            raise TypeError("target has no life attribute.")
        
        if target.life > 0:
            target.life -= 1
            self.energy += 1
        if target.life <= 0:
            target.kill()
    
    def _draw(self):
        _screen = pygame.display.get_surface()
        scr = self.get_screen()
        mid = scr[0] // 2, scr[1] // 2
        half_size = self.rect.width // 2

        self.image.fill("darkred")
        x = half_size + math.cos(math.radians(self.angle)) * half_size
        y = half_size + math.sin(math.radians(self.angle)) * half_size
        pygame.draw.line(self.image, "white", (half_size, half_size), (x, y), 3)
        # pygame.draw.line(_screen, "black", self.rect.center, mid, 1)
    
    def move(self, movement: str):
        if movement == "accelerate":
            self.velocity += 1 if self.velocity <= self.max_velocity else 0
        if movement == "deacelereate":
            self.velocity -= 1 if self.velocity >= -self.max_velocity else 0
        if movement == "left":
            self.angle = (self.angle + 15) % 360
        if movement == "right":
            self.angle = (self.angle - 15) % 360
        if movement == "rand":
            self.velocity += randint(-1, 1)
            if self.velocity > self.max_velocity:
                self.velocity = self.max_velocity
            if self.velocity < -self.max_velocity:
                self.velocity = -self.max_velocity
            self.angle = (self.angle + randint(-15, 15)) % 360

    def get_polar_pos(self):
        return (math.cos(math.radians(self.angle)) * self.velocity,
                math.sin(math.radians(self.angle)) * self.velocity)
    

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.rect.move_ip(self.get_polar_pos())
        self._draw()
        self._energy_update()
        # self.move("rand")
        self.network_move()
        return super().update(*args, **kwargs)




class Side:
    def __init__(self, parent_groups):
        pygame.init()
        width = pygame.display.get_surface().get_width() * 0.4
        self.screen = Surface((width, 320))
        self.running = True
        self.groups: Dict[str, Group] = dict()
        self.parent_groups = parent_groups
        self.pos = 0,0

    def list_parent_groups(self):
        for group_i, (group_name, group) in enumerate(self.parent_groups.items()):
            for spr_i, sprite in enumerate(group.sprites()):
                self.draw_list_item(group_i, group_name, group, spr_i, sprite)

    def update(self, screen: Surface):
        self.screen.fill("#394f7b")
        self.pos = screen.get_width() - self.screen.get_width(), 0
        self.list_parent_groups()
        return screen.blit(self.screen, self.pos)

    def add_to_group(self, sprite, group_name):
        group = self.groups.get(group_name, Group())
        group.add(sprite)
        self.groups[group_name] = group

    def draw_list_item(self, group_i, group_name, group, spr_i, sprite):
        item_height = 40
        rect = Rect(0, spr_i*item_height, self.screen.get_width(), item_height-5)
        text = f"{sprite.__class__.__name__}, {sprite.rect.center}"
        pygame.draw.rect(self.screen, "darkblue", rect)
        draw_text(self.screen, text, rect.center)


class SpriteAttributes:
    def __init__(self, sprite, clock):
        pygame.init()
        width = pygame.display.get_surface().get_width() * 0.4
        self.screen = Surface((width, 320))
        self.running = True
        self.sprite = sprite
        self.clock = clock
        self.pos = 0,0

    def update(self, screen: Surface):
        self.screen.fill("#3b8f9a")
        self.draw_attributes()
        self.pos = screen.get_width() - self.screen.get_width(), screen.get_height() - self.screen.get_height()
        return screen.blit(self.screen, self.pos)

    def draw_attributes(self):
        item_height = 30
        last = None
        d = dict()
        d.update(self.sprite.__dict__)
        d.update(self.sprite.genome.__dict__)
        # d.update(self.sprite.genome.connections)
        # d.update(self.sprite.genome.nodes)
        for i, (key, value) in enumerate(d.items()):
            if len(str(key)) > 25:
                key = str(key)[:25]
            text = f"{key} : {value} |"
            rect = Rect(0, i*item_height, self.screen.get_width(), item_height-5)
            pygame.draw.rect(self.screen, "black", rect)
            draw_text(self.screen, text, rect.center)
        # rect = Rect(0, i+1*item_height, self.screen.get_width(), item_height-5)
        # pygame.draw.rect(self.screen, "black", rect)
        # draw_text(self.screen, self.sprite.genome.fitness, rect.center)


if __name__ == "__main__":
    App().run()
