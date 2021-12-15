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
        """ Движение экрана  """
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
        if self.player.sprite.rect.top >= screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)
        if collided_coins:
            self.coin_sound.play()
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
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
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

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


        

        


        
        
