import pygame
from tiles import AnimatedTile
from random import randint

class Enemy(AnimatedTile):
    """
    class of NPS enemy
    """
    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2, 4)

    def move(self):
        """
        enemy movement (general)
        :return:
        """
        self.rect.x += self.speed

    def reverse_image(self):
        """
        reversing enemy (image)
        :return:
        """
        if self.speed > 0 :
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """
        reversing enemy (movement)
        :return:
        """
        self.speed *= -1

    def update(self, shift):
        """
        updating parameters
        :param shift:
        :return:
        """
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
        
        
    
