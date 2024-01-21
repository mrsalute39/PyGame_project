from sprite_object import *
from enemy import *
# ---------СОЗДАТЕЛЬ ОБЪЕКТОВ-------------------------------------------------------------------------------------------
# упрощает создание пропов, спрайтов, врагов, прочего


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = list()
        self.enemy_list = list()
        self.static_sprite_path = "data/sprites/props/"
        self.animated_sprites_path = "data/sprites/animated_props/"
        self.enemy_sprite_path = "data/sprites/enemy/"

        self.enemy_positions = {}

        # сюда добавлять спрайты:
        self.add_sprite(SpriteObject(game, path="data/sprites/props/dead_body.png", pos=(3.5, 3.5), scale=0.8, shift=0.1))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/dead_body.png", pos=(3.5, 1.5), scale=0.8, shift=0.1))
        self.add_sprite(
            AnimatedSprite(game, path="data/sprites/animated_props/red_torch/red_torch_0.png", pos=(2.5, 4.5)))
        # врагов добавлять сюда:
        self.add_enemy(SoldierDoom(game))
        self.add_enemy(SoldierDoom(game, pos=(13.5, 4.5)))
        self.add_enemy(CacoDemonDoom(game, pos=(6.5, 3.5)))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update(self):
        self.enemy_positions = {enemy.map_pos() for enemy in self.enemy_list if enemy.alive}
        [sprite.update() for sprite in self.sprite_list]
        [enemy.update() for enemy in self.enemy_list]

    def add_enemy(self, some_enemy):
        self.enemy_list.append(some_enemy)

