import pygame

class Tile(pygame.sprite.Sprite):
    """отвечает за плитку, по которой передвигается персонаж"""
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))#квадратные блоки
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, x_shift):
        """графически выводит"""
        self.rect.x += x_shift
        
    
