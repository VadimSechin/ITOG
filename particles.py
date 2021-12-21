import pygame
from support import import_folder


class ParticleEffect(pygame.sprite.Sprite):
    """
    running and jumping effects

    :parameters :
    ------------

    frame_index : int
        Номер картинки

    animation_speed : int
        Скорость перелистывания кадров.

    frames : list
        Список картинок.

    image : image
        Картинка с каким-то номером.

    rect : (int,int)
        Центральные координаты картинки.
    """

    def __init__(self, pos, type):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'jump':
            self.frames = import_folder('./graphics/character/dust_particles/jump')
        if type == 'land':
            self.frames = import_folder('./graphics/character/dust_particles/land')
        if type == 'explosion':
            self.frames = import_folder('./graphics/enemy/explosion')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        """
        effect animation
        """
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, x_shift):
        """
        updating parameters
        :param x_shift: Скорость движения камеры.
        """
        self.animate()
        self.rect.x += x_shift
