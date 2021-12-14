import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Palm
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        # general setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        # player setup
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)
        
        # dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        
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
        self.clouds = Clouds(400, level_width, 30)
        

    def create_tile_group(self, layout, type):
        """ Из обработанного csv файла получаем координаты спрайтов,
            согласно координатам сохраняем картинки,
            вся информация о спрайтах хранится в группе"""
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
                            sprite = Coin(tile_size, x, y, './graphics/coins/gold')
                        if value == '1':
                            sprite = Coin(tile_size, x, y, './graphics/coins/silver')
                            
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
        """ при столкновении NPC с преградой он поворачивает """
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()
    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 18)
        else:
            pos += pygame.math.Vector2(10, -18)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def horisontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self. crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites :
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >=0):
            player.on_left = False
        elif player.on_right and (player.rect.right > self.current_x or player.direction.x <=0):
            player.on_right = False

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        # вручную устанавливается уровень картинок
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 20)
            else:
                offset = pygame.math.Vector2(-10, 20)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)
                
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self. crate_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False
        
    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if value == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite) 
                if value == '1':
                    hat_surface = pygame.image.load('./graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)
                    
    def scroll_x(self):
        """ Движение экрана  """
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x  = player.direction.x

        if player_x < screen_width//6  and direction_x < 0:
            self.world_shift = 7
            player.speed = 0
        
        elif player_x > 5*screen_width//6 and direction_x > 0:
            self.world_shift = -7
            player.speed = 0

        else:
            self.world_shift = 0
            player.speed = 7

    def run(self):
        """ запускает всю игру / уровень """

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

        # океан
        self.water.draw(self.display_surface, self.world_shift)


        

        


        
        
