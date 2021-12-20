import pygame
from game_data import levels
from support import import_folder
from decoration import Sky


class Node(pygame.sprite.Sprite):
    """
    class of the level node
    """

    def __init__(self, pos, status, icon_speed, path):
        super().__init__()
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        if status == 'available':
            self.status = 'available'
        elif status == 'locked':
            self.status = 'locked'
        self.rect = self.image.get_rect(center=pos)
        self.detection_zone = pygame.Rect(self.rect.centerx - (4 * icon_speed // 7),
                                          self.rect.centery - (4 * icon_speed // 7), icon_speed, icon_speed)

    def animate(self):
        """
        animates node
        """
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self):
        """
        updates node
        """
        if self.status == 'available':
            self.animate()
        else:
            tinted_surf = self.image.copy()
            tinted_surf.fill('black', None, pygame.BLEND_RGBA_MULT)
            self.image.blit(tinted_surf, (0, 0))


class Shop(pygame.sprite.Sprite):
    """
    class of the shop door
    """

    def __init__(self, pos):
        """
        :param pos: position of the door to the shop
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graphics/coins/door.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Icon(pygame.sprite.Sprite):
    """
    class of the character's hat
    """

    def __init__(self, pos):
        """
        :param pos: position of the character's hat
        """
        super().__init__()
        self.pos = pos
        self.image = pygame.image.load('./graphics/character/hat.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)

    def update(self):
        """
        updates character's hat position
        """
        self.rect.center = self.pos


class Overworld:
    """
    class of the owerworld itself
    """

    def __init__(self, start_level, max_level, surface, create_level, create_shop):
        """
        :param start_level: start level
        :param max_level: max level
        :param surface:
        :param create_level: def which creates level
        :param create_shop: def which opens shop
        """
        # setup
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level
        self.create_shop = create_shop
        self.create_level = create_level

        # movement logic
        self.moving = False
        self.move_direction = pygame.math.Vector2(0, 0)
        self.speed = 7

        # sprites
        self.setup_nodes()
        self.setup_icon()
        self.setup_shop()
        self.sky = Sky(8, 'overworld')

        # time
        self.start_time = pygame.time.get_ticks()
        self.allow_input = False
        self.timer_length = 300  # Bucks

    def setup_nodes(self):
        """
        setups nodes of levels
        """
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate(levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'available', self.speed, node_data['node_graphics'])

            elif index >= self.max_level:
                node_sprite = Node(node_data['node_pos'], 'locked', self.speed, node_data['node_graphics'])

            self.nodes.add(node_sprite)

    def setup_icon(self):
        """
        setups the item of the character's hat
        """
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def setup_shop(self):
        """
        setups shops door button
        """
        self.shop = pygame.sprite.GroupSingle()
        shop_sprite = Shop((50, 50))
        self.shop.add(shop_sprite)

    def draw_paths(self):
        """
        draws path between levels
        """
        if self.max_level > 0:
            points = [node['node_pos'] for index, node in enumerate(levels.values()) if index <= self.max_level]
            pygame.draw.lines(self.display_surface, '#a04f45', False, points, 6)

    def input(self):
        """
        reacts to the player's button taps
        """
        keys = pygame.key.get_pressed()
        if not self.moving and self.allow_input:
            if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
                self.move_direction = self.get_movement_data('next')
                self.current_level += 1
                self.moving = True
            elif keys[pygame.K_LEFT] and self.current_level > 0:
                self.move_direction = self.get_movement_data('previous')
                self.current_level -= 1
                self.moving = True

            elif keys[pygame.K_SPACE]:
                self.create_level(self.current_level)

    def get_movement_data(self, target):
        """ Возвращает единичный вектор в направлении к следующему уровню
        """
        start = pygame.math.Vector2(self.nodes.sprites()[self.current_level].rect.center)
        if target == 'next':
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level + 1].rect.center)
        else:
            end = pygame.math.Vector2(self.nodes.sprites()[self.current_level - 1].rect.center)

        return (end - start).normalize()

    def update_icon_pos(self):
        """
        updates position of the character's hat
        """
        if self.moving and self.move_direction:
            self.icon.sprite.pos += self.speed * self.move_direction
            target_node = self.nodes.sprites()[self.current_level]
            if target_node.detection_zone.collidepoint(self.icon.sprite.pos):
                self.moving = False
                self.move_direction = pygame.math.Vector2(0, 0)

    def input_timer(self):
        """
        just timer
        """
        if not self.allow_input:
            current_time = pygame.time.get_ticks()
            if current_time - self.start_time >= self.timer_length:
                self.allow_input = True

    def run(self):
        """
        runs overworld
        """
        self.input_timer()
        self.input()
        self.update_icon_pos()
        self.nodes.update()
        self.icon.update()

        self.sky.draw(self.display_surface)
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        self.shop.draw(self.display_surface)
