import pygame
from support import import_csv, import_graphics
from settings import tile_size
from tiles import Tile, StaticTile, CrateTile, CoinTile, PalmTile
from enemy import Enemy


class Level:
    def __init__(self, level_data, surface):
        # Gereral setup
        self.display_surface = surface
        self.world_shift = 0

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
                        if value == '0': sprite = CoinTile(tile_size, x, y, 'graphics/coins/gold')
                        if value == '1': sprite = CoinTile(tile_size, x, y, 'graphics/coins/silver')

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

    def run(self):
        # Palms background
        self.palms_bg_sprites.update(self.world_shift)
        self.palms_bg_sprites.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraints_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

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
