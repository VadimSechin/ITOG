import pygame
from support import import_folder

class Tile(pygame.sprite.Sprite):
    """
    block class (general)
    """
    def __init__(self, size, x, y):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, shift):
        """
        updating parametres
        :param shift:
        :return:
        """
        self.rect.x += shift
        
class StaticTile(Tile):
    """
    fixed block class
    """
    def __init__(self, size, x, y, surface):
        super().__init__(size, x, y)
        self.image = surface
    
class Crate(StaticTile):
    """
    fixed box class
    """
    def __init__(self, size, x, y):
        super().__init__(size, x, y, pygame.image.load('./graphics/terrain/crate.png').convert_alpha())
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft = (x, offset_y))
        
class AnimatedTile(Tile):
    """
    class of moving elements of the level
    """
    def __init__(self, size, x, y, path):
        super().__init__(size, x, y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        
    def animate(self):
        """
        elements animation
        :return:
        """
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, shift):
        """
        updating parameters
        :param shift:
        :return:
        """
        self.rect.x += shift
        self.animate()

class Coin(AnimatedTile):
    """
    coins class
    """
    def __init__(self, size, x, y, path, value):
        super().__init__(size, x, y, path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x, center_y))
        self.value = value

class Palm(AnimatedTile):
    """
    palm class
    """
    def __init__(self, size, x, y, path, offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)


            
