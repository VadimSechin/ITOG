import pygame, sys
from settings import *
from overworld import Overworld
from level import Level
from shop import Shop
from ui import UI

class Game:
    def __init__(self):
        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.current_health = 100
        self.coins = 0
        # audio
        self.level_bg_music = pygame.mixer.Sound('./audio/level_music.wav')
        self.overworld_bg_music = pygame.mixer.Sound('./audio/overworld_music.wav')
        # overworld creation
        self.overworld = Overworld(0, self.max_level, screen, self.create_level, self.create_shop)
        self.status = 'overworld'
        #self.overworld_bg_music.play(loops = -1)
        # user interface
        self.ui = UI(screen)
        

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.create_overworld, self.change_coins, self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        #self.level_bg_music.play(loops = -1)

    def create_shop(self):
        self.shop = Shop(screen, self.create_overworld, self.change_coins)
        self.status = 'shop'
        self.overworld_bg_music.stop()
        #self.level_bg_music.play(loops = -1)

    def create_overworld(self, current_level, new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level, self.max_level, screen, self.create_level, self.create_shop)
        self.status = 'overworld'
        self.level_bg_music.stop()
        #self.overworld_bg_music.play(loops = -1)

    def change_coins(self, amount):
        self.coins += amount

    def change_health(self, amount):
        self.current_health += amount

    def buy_potion(self, price):
        if self.coins >= price:
            self.coins -= price
            if self.current_health <= 95:
                self.current_health += 5
            else:
                self.current_health += (100 - self.current_health)
            print('bought')
        else:
            print('hasnt bought')



    def check_game_over(self):
        if self.current_health <= 0:
            self.current_health = 100
            self.coins = 0
            self.max_level = 0
            self.overworld = Overworld(0, self.max_level, screen, self.create_level, self.create_shop)
            self.status = 'overworld'
            self.level_bg_music.stop()
            self.overworld_bg_music.play(loops = -1)
        
    def run(self):
        if self.status == 'overworld':
            self.overworld.run()
        if self.status == 'shop':
            self.shop.run()
            self.ui.show_coins(self.coins)
            self.ui.show_health(self.current_health, self.max_health)
        elif self.status == 'level':
            self.level.run()
            self.ui.show_health(self.current_health, self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
game = Game()


flag = 1
while True:
    for event in pygame.event.get():
        flag = 1
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if (game.status == 'overworld') and (event.type == pygame.MOUSEBUTTONDOWN) and (flag == 1):
            if (60>event.pos[0]>40) and (60>event.pos[1]>40):
                game.create_shop()
                flag = -flag
        if (game.status == 'shop') and (event.type == pygame.MOUSEBUTTONDOWN) and (flag == 1):
            if (1135>event.pos[0]>1105) and (65>event.pos[1]>35):
                game.create_overworld(0, game.max_level)
                flag = -flag

        if (game.status == 'shop') and (event.type == pygame.MOUSEBUTTONDOWN) and (flag == 1):
            if (65>event.pos[0]>35) and (45>event.pos[1]>15):
                game.buy_potion(5)
                flag = -flag



    game.run()
    pygame.display.update()
    clock.tick(75)
