import pygame
from support import import_csv_layout, import_cut_graphics
from settings import *
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels


class Level:
    """ Класс Level используется для создания игрового уровня

    Основное применение - создание игровых спрайтов, их перемещение, коллизии

    Atributes

    ---------
    display_surface : surface
        поверхность игрового уровня
    world_shift : int
        скорость перемещения камеры
    current_x : int
        положение игрового персонажа по оси х
    stomp_sound : mp3_file
        музыка нанесения урона
    coin_sound : mp3_file
        музыка собрания монеток
    create_overworld : function
        функция создающая карту уровней
    current_level : int
        номер текущего уровня, начиная с 0
    new_max_level : library
        номер максимального доступного уровня, начиная с 0
    player : GroupSingle
        спрайт игрового персонажа
    player_setup : function
        создание спрайта игрового персонажа и точки завершения уровня
    change_coins : function
        функция обновляющая число собранных монет
    dust_sprite : GroupSingle
        спрайт эффектов движения персонажа
    player_on_ground : bull
        утверждение, является ли персонаж на поверхности игровых спрайтов
    explosion_sprites : Group
        спрайты эффектов убийства врага
    terrain_sprites : Group
        спрайты ландшафта
    grass_sprites : Group
        спрайты травы
    crate_sprites : Group
        спрайты ящиков
    coin_sprites : Group
        спрайты монеток
    fg_palm_sprites : Group
        спрайты пальм переднего плана
    bg_palm_sprites : Group
        спрайты пальм заднего плана
    enemy_sprites : Group
        спрайты врагов
    constraint_sprites : Group
        спрайты точек поворота врагов
    sky : class Sky instance
        объект класа Sky, отображает небо
    water : class Water instance
        объект класа  Water, отображает воду
    clouds : class Clouds instance
        объект класа Clouds, отображает облака

    """
    
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # audio
        self.stomp_sound = pygame.mixer.Sound('./audio/effects/stomp.wav')
        self.coin_sound = pygame.mixer.Sound('./audio/effects/coin.wav')

        # overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']
        
        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)

        # user interface
        self.change_coins = change_coins
        
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # explosion particles
        self.explosion_sprites = pygame.sprite.Group()
        
        # terrain setup
        terrain_layout = import_csv_layout(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # grass setup
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # crates setup
        crate_layout = import_csv_layout(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # coins setup
        coin_layout = import_csv_layout(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # foreground palms
        fg_palms_layout = import_csv_layout(level_data['fg palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palms_layout, 'fg palms')

        # background palms
        bg_palm_layout = import_csv_layout(level_data['bg palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'bg palms')

        # enemies
        enemy_layout = import_csv_layout(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # constraint
        constraint_layout = import_csv_layout(level_data['constraints'])
        self.constraint_sprites = self.create_tile_group(constraint_layout, 'constraints')

        # decorations
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 20, level_width)
        self.clouds = Clouds(400, level_width, 50)
        

    def create_tile_group(self, layout, type):
        """ Метод, который из обработанного csv файла получает координаты спрайтов,
            согласно координатам создает игровые спрайты,
            вся информация о спрайтах хранится в группе

            return :
            Группа игровых спрайтов"""
        
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != '-1':
                    x = column_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile_list = import_cut_graphics('./graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface) 
                        
                    if type == 'grass':
                        grass_tile_list = import_cut_graphics('./graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        sprite = Crate(tile_size, x, y)
                        sprite_group.add(sprite)

                    if type == 'coins':
                        if value == '0':
                            sprite = Coin(tile_size, x, y, './graphics/coins/gold', 5)
                        if value == '1':
                            sprite = Coin(tile_size, x, y, './graphics/coins/silver', 1)
                            
                    if type == 'fg palms':
                        if value == '4' or value == '5' or value == '6' or value == '7' :
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_small', 38)
                        if value == '0' or value == '1' or value == '2' or value == '3' :
                            sprite = Palm(tile_size, x, y, './graphics/terrain/palm_large', 64)
                        
                    if type == 'bg palms':
                        sprite = Palm(tile_size, x, y, './graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y)

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    if type == 'player':
                        if value == '0':
                            sprite = Tile(tile_size, x, y)
                       
                    sprite_group.add(sprite)   
            
        return sprite_group

    def enemy_constraint_collision(self):
        """ Метод, который изменяет направление движения врагов при столкновении врагов с точками поворота """

        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
                
    def create_jump_particles(self, pos):
        """ Метод, который создает спрайт эффект прыжка персонажа """

        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 18)
        else:
            pos += pygame.math.Vector2(10, -18)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horisontal_movement_collision(self):
        """ Метод, описывающий все горизонтальное движение игрового персонажа"""

        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self. crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites :
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.collision_rect.right
                    
        if player.on_left and (player.collision_rect.left < self.current_x or player.direction.x >=0):
            player.on_left = False
        elif player.on_right and (player.collision_rect.right > self.current_x or player.direction.x <=0):
            player.on_right = False

    def get_player_on_ground(self):
        """ Метод, проверяющий является ли игровой персонаж на поверхности игровых спрайтов """

        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        """ Метод, создающий спрайт эффекта приземления """
        
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 20)
            else:
                offset = pygame.math.Vector2(-10, 20)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
                
    def vertical_movement_collision(self):
        """ Метод, описывающий все вертикальное движение персонажа """
        
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self. crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        
    def player_setup(self, layout, change_health):
        """ Метод, создающий спрайт игрового персонажа и точку завершения уровня

        Parametrs
        ---------

        layout : list
            лист листов значений id объектов 
        change_health : function
            проверяет количество собранных монет
        """
        
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite) 
                if value == '1':
                    hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
                    
    def scroll_x(self):
        """ Метод, изменяющий скорость движение камеры,
            в засисимости от положения и скорости игрового персонажа """
        
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x  = player.direction.x

        if player_x < 3*screen_width//7  and direction_x < 0:
            self.world_shift = 7
            player.speed = 0
        
        elif player_x > 4*screen_width//7 and direction_x > 0:
            self.world_shift = -7
            player.speed = 0

        else:
            self.world_shift = 0
            player.speed = 7

    def check_death(self):
        """ Метод, обновляющий уровень при падении в воду """

        if self.player.sprite.rect.top >= screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        """ Метод, создающий карту уровней и открывающий следующий
            уровнень при попадании персонажа в точку заверщения уровня """
        
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        """ Метод, который считает количество собранных монет """
        
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def enemy_ai_behaviour(self):
        """ Метод, который заставляет врагов следовать за персонажем если он находится неподалеку """
        
        for enemy in self.enemy_sprites:
            enemy_x = enemy.rect.centerx
            enemy_top = enemy.rect.centery - 32
            enemy_bottom = enemy.rect.centery + 32
            player_center_y = self.player.sprite.rect.centery
            player_center_x = self.player.sprite.rect.centerx
            if enemy_top < player_center_y < enemy_bottom and enemy_x-200 < player_center_x < enemy_x+200:
                if self.player.sprite.rect.centerx - enemy.rect.centerx != 0:
                    enemy.speed = abs(enemy.speed)*((self.player.sprite.rect.centerx - enemy.rect.centerx) / (abs(self.player.sprite.rect.centerx - enemy.rect.centerx)))
                

    def check_enemy_collisions(self):
        """ Метод, обрабатывающий все столкновения персонажа и врагов """
        
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y > 1:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    self.stomp_sound.play()
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()
    def run(self):
        """ Метод, который запускает уровень """

        # небо
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        
        # пальмы заднего вида
        self.bg_palm_sprites.draw(self.display_surface)
        self.bg_palm_sprites.update(self.world_shift)

        # ландшафт
        self.terrain_sprites.draw(self.display_surface)
        self.terrain_sprites.update(self.world_shift)

        # ящик
        self.crate_sprites.draw(self.display_surface)
        self.crate_sprites.update(self.world_shift)
        
        # NPC - пассивые противники
        self.enemy_sprites.draw(self.display_surface)
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift) # ограничения для NPC
        self.enemy_constraint_collision() # поворачивает противников на границе
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        self.enemy_ai_behaviour()

        # трава
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        # монетки
        self.coin_sprites.draw(self.display_surface)
        self.coin_sprites.update(self.world_shift)

        # пальмы переднего вида
        self.fg_palm_sprites.draw(self.display_surface)
        self.fg_palm_sprites.update(self.world_shift)

        # пыль
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # спрайты игрока
        self.player.update()
        self.horisontal_movement_collision()
        
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.draw(self.display_surface)
        self.goal.update(self.world_shift)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # океан
        self.water.draw(self.display_surface, self.world_shift)


        

        


        
        
