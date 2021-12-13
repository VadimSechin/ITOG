import pygame
from support import import_folder #импортируем функцию, которая работает с картинками.

class Player(pygame.sprite.Sprite):
    """большой класс игрового персонажа. Присутствуют методы : """

    def __init__(self, pos, surface, create_jump_particles):
        # создаёт кучу атрибутов
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        #dust particles
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        #player movement
        self.speed = 7
        self.direction = pygame.math.Vector2(0,0)
        self.gravity = 0.7
        self.jump_speed = -14

        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False # colliding with the left wall
        self.on_right = False # colliding with the right wall

    def import_character_assets(self):
        """ создаём словарь состояний игрока и соответствующие этому состоянию картинки. """
        character_path = './graphics/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        # создаём список картинок эффектов бега.
        self.dust_run_particles = import_folder('./graphics/character/dust_particles/run')
        

    def animate(self):
        """ Куча проверок (взаимодейтсвия со стенами, полом и потолком). Перелистывание картинок и выбор нужного
        состояния персонажа. """
        animation = self.animations[self.status]

        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        #set the rect
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def run_dust_animation(self):
        """ проверям нужно ли рисовать ту или иную картинку. Реализуем список картинок (см.ф-ию import_dust_run_particles) """
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index += self.dust_animation_speed
            if self.dust_frame_index >= len(self.dust_run_particles):
                self.dust_frame_index = 0
            dust_particle = self.dust_run_particles[int(self.dust_frame_index)]

            if self.facing_right:
                #вручную вставляется высота и ширина пыли
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                flipped_dust_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_dust_particle, pos)

    def get_status(self):
        """ Проверка состояния персонажа (прыгает, падает или ему комфортно) """
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 1:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'           

    def get_input(self):
        """ Обработка событий """
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom )

    def apply_gravity(self):
        """физическое падение"""
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """прыжок"""
        self.direction.y = self.jump_speed

    def update(self):
        """"изменение всего графического интерфейся"""
        self.get_input()
        self.get_status()
        self.animate()
        self.run_dust_animation()
        
