import pygame
from decoration import Sky
import pygame._sprite as sprite
import pygame.image as image
import pygame.font as font


class Potion(sprite.Sprite):
    """
    class of the health potion
    """

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = image.load('./graphics/coins/health_potion/01.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Back_gr_for_item(sprite.Sprite):
    """
    class of the health potion background in the shop
    """

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = image.load('./graphics/coins/background/1.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class BB(sprite.Sprite):
    """
    class of the back button in the shop
    """

    def __init__(self, pos):
        super().__init__()
        self.pos = pos
        self.image = image.load('./graphics/coins/door.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)


class Shop:
    """
    class of the shop itself
    """

    def __init__(self, surface, create_overworld):
        # setup
        self.display_surface = surface
        self.create_overworld = create_overworld

        # sprites
        self.sky = Sky(8, 'overworld')
        self.setup_back_btn()
        self.setup_potion()
        self.setup_bg()

    def setup_bg(self):
        """
        setups background in the shop
        """
        self.bg = sprite.GroupSingle()
        shop_sprite = Back_gr_for_item((250, 255))
        self.bg.add(shop_sprite)

    def setup_back_btn(self):
        """
        setups button in the shop
        """
        self.back_btn = sprite.GroupSingle()
        shop_sprite = BB((1120, 50))
        self.back_btn.add(shop_sprite)

    def setup_potion(self):
        """
        setups button in the shop
        """
        self.potion = sprite.GroupSingle()
        shop_sprite = Potion((250, 250))
        self.potion.add(shop_sprite)

    def run(self):
        """
        runs shop
        """
        self.sky.draw(self.display_surface)
        self.back_btn.draw(self.display_surface)
        self.bg.draw(self.display_surface)
        self.potion.draw(self.display_surface)

        # text under potion item
        myfont = font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render('Health potion (10)', False, (0, 0, 0))
        self.display_surface.blit(textsurface, (170, 300))
