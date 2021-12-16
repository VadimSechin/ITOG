import pygame
from decoration import Sky
items = ['Potion']
positions = [(100, 100)]

class Potion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graphics/character/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class BB(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graphics/character/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center = pos)

class Shop:
    def __init__(self, surface, create_overworld, change_coins):

        # setup
        self.display_surface = surface
        self.create_overworld = create_overworld


        # sprites
        self.sky = Sky(8, 'overworld')
        self.setup_back_btn()
        self.setup_potion()


    def setup_back_btn(self):
        self.back_btn = pygame.sprite.GroupSingle()
        shop_sprite = BB((50, 30))
        self.back_btn .add(shop_sprite)

    def setup_potion(self):
        self.potion = pygame.sprite.GroupSingle()
        shop_sprite = Potion((250, 250))
        self.potion.add(shop_sprite)

    def run(self):
        self.sky.draw(self.display_surface)
        self.back_btn.draw(self.display_surface)
        self.potion.draw(self.display_surface)


