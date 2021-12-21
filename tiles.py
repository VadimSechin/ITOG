import pygame
from support import import_folder


class Tile(pygame.sprite.Sprite):
    """
    block class (general)

    :parameters:
    ------------
    image : surface
        Квадрат с величиной size
    rect : (int,int)
        Координаты верхней левой вершины.

    """

    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, shift):
        """
        updating parametres
        :param shift: Скорость движения камеры.
        """
        self.rect.x += shift #Связано с движением камеры.


class StaticTile(Tile):
    """
    fixed block class

    :parameter:
    -----------
    image : image
        Картинка неподвижного игрового блока.
    """

    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface


class Crate(StaticTile):
    """
    Box class

    rect : (int,int)
        Координаты левой нижней вершины коробки.
    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('./graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size #Обновлённая координата с учётом разности нижней границы картинки и соотв.прямоугольником (tile)
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):
    """
    class of moving elements of the level

    :parameters:
    ------------
    frames : list
        Набор картинок движущихся (колеблющихся) объектов
    frame index : int
        Номер картинки
    image : image
        Изображение соответсвующего номера
    """

    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        """
        elements animation
        Перелистываем картинки
        """
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames): #Зацикливание перелистывания картинок.
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        """
        updating parameters
        :param shift: Скорость движения камеры.
        """
        self.rect.x += shift
        self.animate() #Связано с движением камеры.


class Coin(AnimatedTile):
    """
    coins class

    :parameters:
    -------------
    rect : (int,int)
        Координаты центра изображения монетки.
    value : int
        Номинал монетки.
    """

    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))
        self.value = value


class Palm(AnimatedTile):
    """
    palm class

    :parameters :
    -------------
    rect : (int,int)
        Координаты левой верхней вершины.
    """

    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset  # Разность нижней границы прямоугольника (tile) и картинки (image)
        self.rect.topleft = (x, offset_y)
