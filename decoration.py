import pygame

from settings import *
from support import import_folder
from tiles import AnimatedTile, StaticTile
from random import choice, randint


class Sky:
    """
    background sky

    :parameters :
    -----------
    horizon : int
        y-ковая координата линии горизонта(линии, с которой задний фон меняется).
    top : image
        Картинка верхней части неба.
    bottom : image
        Картинка нижней части неба.
    middle : image
        Картинка средней части неба (изображение горизонта).
    style : str
        Некоторый ключ в библиотеке.
    palms : list
        Список картинок пальм с соответствующими координатами.
    clouds : list
        Спикок картинок облаков с соответсвующими координатами.
    """

    def __init__(self, horison, style='level'):
        self.horison = horison
        self.top = pygame.image.load('./graphics/decoration/sky/sky_top.png').convert()
        self.bottom = pygame.image.load('./graphics/decoration/sky/sky_bottom.png').convert()
        self.middle = pygame.image.load('./graphics/decoration/sky/sky_middle.png').convert()

        # stretch, растягиваем квадратик в полоску.
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))

        self.style = style
        if self.style == 'overworld': #создаём фон карты уровней (поверхность)
            palm_surfaces = import_folder('./graphics/overworld/palms')
            self.palms = []

            for surface in [choice(palm_surfaces) for image in range(8)]:
                x = randint(0, screen_width)
                y = (self.horison * tile_size) + randint(50, 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.palms.append((surface, rect))

            cloud_surfaces = import_folder('./graphics/overworld/clouds')
            self.clouds = []

            for surface in [choice(cloud_surfaces) for image in range(8)]:
                x = randint(0, screen_width)
                y = randint(0, (self.horison * tile_size) - 100)
                rect = surface.get_rect(midbottom=(x, y))
                self.clouds.append((surface, rect))

    def draw(self, surface):
        """
        drawing objects
        Отрисовываем фон
        :param surface: Картинка, которую функция отображает.
        """
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horison:
                surface.blit(self.top, (0, y))
            elif row == self.horison:
                surface.blit(self.middle, (0, y))
            elif row > self.horison:
                surface.blit(self.bottom, (0, y))
        if self.style == 'overworld':
            for palm in self.palms:
                surface.blit(palm[0], palm[1])
            for cloud in self.clouds:
                surface.blit(cloud[0], cloud[1])


class Water:
    """
    background water

    :parameters :
    -------------
    water_sprites : Group
        Спрайт-группа картинок воды.
    """

    def __init__(self, top, level_width):
        water_start = - screen_width
        water_tile_width = 192
        tile_x_amount = (level_width + screen_width * 2) / water_tile_width
        self.water_sprites = pygame.sprite.Group()

        for tile in range(int(tile_x_amount)): #Создаём меняющуюся спрайт-группу воды, блоки которой склеены.
            x = tile * water_tile_width + water_start
            y = top
            sprite = AnimatedTile(192, x, y, './graphics/decoration/water')
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        """
        drawing objects
        Отрисовываем спрайт-группу воды при движении камеры.
        :param surface: Картинка, которую функция отображает.
        :param shift: Скорость движения камеры.
        """
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)


class Clouds:
    """
    background clouds

    :parameters :
    --------------
    cloud_sprites : Group
        Спрайт-группа облаков
    """

    def __init__(self, horison, level_width, cloud_number):
        cloud_surf_list = import_folder('./graphics/decoration/clouds')
        min_x = -screen_width
        max_x = level_width + screen_width
        min_y = 0
        max_y = horison
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number): #Выбираем одну картинку, для неё выбираем координаты и рисуем облако.
            cloud = choice(cloud_surf_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        """
        drawing objects
        Отрисовываем спрайт-группу облаков при движении камеры.
        :param surface: Картинка, которую функция отображает.
        :param shift: Скорость движения камеры.
        """
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
