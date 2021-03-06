import pygame
from support import import_csv, import_graphics
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, CrateTile, CoinTile, PalmTile
from enemy import Enemy
from sky import Sky
from water import Water
from clouds import Clouds
from player import Player
from particles import Particles
from game_data import levels


class Level:
    def __init__(self, current_level, surface, create_overworld, update_coins, update_health):
        # Gereral setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = 0

        # Audio
        self.coin_sound = pygame.mixer.Sound('audio/effects/coin.wav')
        self.coin_sound.set_volume(0.25)
        self.stomp_sound = pygame.mixer.Sound('audio/effects/stomp.wav')
        self.stomp_sound.set_volume(0.25)

        # Overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data['unlock']

        # Player setup
        player_layout = import_csv(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, update_health)

        # User interface
        self.update_coins = update_coins

        # Dust
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_floor = False

        # Explosion
        self.explosion_sprites = pygame.sprite.Group()

        # Terrain setup
        terrain_layout = import_csv(level_data['terrain'])
        self.terrain_sprites = self.create_tile_group(terrain_layout, 'terrain')

        # Grass setup
        grass_layout = import_csv(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # Crates setup
        crate_layout = import_csv(level_data['crates'])
        self.crate_sprites = self.create_tile_group(crate_layout, 'crates')

        # Coins
        coin_layout = import_csv(level_data['coins'])
        self.coin_sprites = self.create_tile_group(coin_layout, 'coins')

        # Palms foreground
        palms_fg_layout = import_csv(level_data['palms fg'])
        self.palms_fg_sprites = self.create_tile_group(palms_fg_layout, 'palms fg')

        # Palms background
        palms_bg_layout = import_csv(level_data['palms bg'])
        self.palms_bg_sprites = self.create_tile_group(palms_bg_layout, 'palms bg')

        # Enemy
        enemy_layout = import_csv(level_data['enemies'])
        self.enemy_sprites = self.create_tile_group(enemy_layout, 'enemies')

        # Contstraints
        constraints_layout = import_csv(level_data['constraints'])
        self.constraints_sprites = self.create_tile_group(constraints_layout, 'constraints')

        # Decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 24, level_width)
        self.clouds = Clouds(400, level_width, 20)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        jump_dust_particles_sprite = Particles(pos, 'jump')
        self.dust_sprite.add(jump_dust_particles_sprite)

    def player_setup(self, layout, update_health):
        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size

                if value == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, update_health)
                    self.player.add(sprite)
                if value == '1':
                    hat_surface = pygame.image.load('graphics/character/hat.png').convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, value in enumerate(row):
                if value != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == 'terrain':
                        terrain_tile = import_graphics('graphics/terrain/terrain_tiles.png')
                        tile_surface = terrain_tile[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'grass':
                        grass_tile = import_graphics('graphics/decoration/grass/grass.png')
                        tile_surface = grass_tile[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == 'crates':
                        crate_surface = pygame.image.load('graphics/terrain/crate.png')
                        sprite = CrateTile(tile_size, x, y, crate_surface)

                    if type == 'coins':
                        if value == '0': sprite = CoinTile(tile_size, x, y, 'graphics/coins/gold', 5)
                        if value == '1': sprite = CoinTile(tile_size, x, y, 'graphics/coins/silver', 1)

                    if type == 'palms fg':
                        if value == '0': sprite = PalmTile(tile_size, x, y, 'graphics/terrain/palm_small', 38)
                        if value == '1': sprite = PalmTile(tile_size, x, y, 'graphics/terrain/palm_large', 72)

                    if type == 'palms bg':
                        sprite = PalmTile(tile_size, x, y, 'graphics/terrain/palm_bg', 64)

                    if type == 'enemies':
                        sprite = Enemy(tile_size, x, y, 'graphics/enemy/run')

                    if type == 'constraints':
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraints_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)

        jump_dust_particles_sprite = Particles(pos, 'jump')
        self.dust_sprite.add(jump_dust_particles_sprite)

    def create_land_particles(self):
        if not self.player_on_floor and self.player.sprite.on_floor and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)

            land_dust_particles_sprite = Particles(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(land_dust_particles_sprite)

    def get_player_on_floor(self):
        if self.player.sprite.on_floor:
            self.player_on_floor = True
        else:
            self.player_on_floor = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        screen_quarter = screen_width / 4

        if player_x < screen_quarter and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - screen_quarter and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def horizontal_movement(self):
        player = self.player.sprite
        player.collision_rect.x += player.direction.x * player.speed
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites(
        ) + self.palms_fg_sprites.sprites()

        # Detect collision
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

    def vertical_movement(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.terrain_sprites.sprites() + self.crate_sprites.sprites(
        ) + self.palms_fg_sprites.sprites()

        # Detect collision
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_floor = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_floor and player.direction.y < 0 or player.direction.y > player.gravity:
            player.on_floor = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collisions(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coin_sprites, True)

        if collided_coins:
            self.coin_sound.play()

            for coin in collided_coins:
                self.update_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemy_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom

                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.stomp_sound.play()
                    self.player.sprite.direction.y = -15
                    explostion_sprite = Particles((enemy.rect.center), 'explosion')
                    self.explosion_sprites.add(explostion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def run(self):
        # Sky
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # Palms background
        self.palms_bg_sprites.update(self.world_shift)
        self.palms_bg_sprites.draw(self.display_surface)

        # Dust particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # Explosion particles
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # Crates
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Palms foreground
        self.palms_fg_sprites.update(self.world_shift)
        self.palms_fg_sprites.draw(self.display_surface)

        # Coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_movement()
        self.get_player_on_floor()
        self.vertical_movement()
        self.create_land_particles()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()

        self.check_coin_collisions()
        self.check_enemy_collisions()

        # Water
        self.water.draw(self.display_surface, self.world_shift)
