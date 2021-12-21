import pygame


class UI:
    """
    health and coins bars

    :parameters:
    -------------
    display_surface : surface
        Поверхность, на которой отображаются шкалы.
    health_bar : image
        Картинка школы здоровья.
    health_bar_topleft : (int,int)
        Координаты левой верхней вершины картинки шкалы здоровья.
    bar_max_width : int
        Ширина шкалы здоровья. (Максимальная длина красной полоски жизней)
    bar_height : int
        Высота шкалы здоровья.
    coin : image
        Картинка монетки.
    coin_rect : (int,int)
        Координаты верхней левой вершины картинки монетки.
    font : font
        Шрифт счётчика монеток.
    """

    def __init__(self, surface):
        # setup
        self.display_surface = surface

        # health
        self.health_bar = pygame.image.load('./graphics/ui/health_bar.png').convert_alpha()
        self.health_bar_topleft = (54, 39)
        self.bar_max_width = 152
        self.bar_height = 4

        # coins
        self.coin = pygame.image.load('./graphics/ui/coin.png').convert_alpha()
        self.coin_rect = self.coin.get_rect(topleft=(50, 61))
        self.font = pygame.font.Font('./graphics/ui/ARCADEPI.TTF', 30)

    def show_health(self, current, full):
        """
        drawing health bar
        :param current: Текущее длина полоски жизней
        :param full: Полная длина полоски жизней
        """
        self.display_surface.blit(self.health_bar, (20, 10))
        current_health_ratio = current / full
        current_bar_width = self.bar_max_width * current_health_ratio #Текущая длина полоски жизни равна отношению чисел макс.длины к текущей.
        health_bar_rect = pygame.Rect(self.health_bar_topleft, (current_bar_width, self.bar_height)) #Задаём положение шкалы здоровья
        pygame.draw.rect(self.display_surface, '#dc4949', health_bar_rect) #Отрисовываем поверхность

    def show_coins(self, amount):
        """
        drawing coins bar
        :param amount: Значение счётчика монеток. (1 золотая = 5 серебряным)
        """
        self.display_surface.blit(self.coin, self.coin_rect)
        coin_amount_surf = self.font.render(str(amount), False, '#33323d') #Задаём количество, отменяем выравнивание, задаём цвет.
        coin_amount_rect = coin_amount_surf.get_rect(midleft=(self.coin_rect.right + 4, self.coin_rect.centery)) #Задаём положение счётчика монеток
        self.display_surface.blit(coin_amount_surf, coin_amount_rect) #Отрисовываем поверхность
