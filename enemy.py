import pygame
from tiles import AnimatedTile
from random import randint


class Enemy(AnimatedTile):
    """
    class of NPC enemy

    :parameters :
    ------------
    rect.y : int
        Положение врага по вертикали.
    rect.x : int
        Положение врага по горизотали.
    speed : int
        Скорость врага.
    """

    def __init__(self, size, x, y):
        super().__init__(size, x, y, './graphics/enemy/run')
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2, 4)

    def move(self):
        """
        Перемещение врага.
        """
        self.rect.x += self.speed

    def reverse_image(self):
        """
        reversing enemy (image)
        """
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        """
        reversing enemy (movement)
        """
        self.speed *= -1

    def update(self, shift):
        """
        updating parameters
        Описываем движение врага при движении камеры.
        :param shift: Скорость движения камеры.
        """

        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()
