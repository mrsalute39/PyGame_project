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

        self.add_sprite(SpriteObject(game, path="data/sprites/props/table.png", pos=(3.5, 2.5), scale=0.75, shift=0.5))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/christmas_tree.png", pos=(3.5, 1.5), scale=1.0,
                                     shift=0.001))
        self.add_sprite(
            AnimatedSprite(game, path="data/sprites/animated_props/red_torch/red_torch_0.png", pos=(2.5, 5.5)))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/fridge.png", pos=(3.5, 3.5), scale=0.8, shift=0.15))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/tv.png", pos=(2.5, 3.5), scale=0.8, shift=0.2))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/main_hero_car.png", pos=(6.0, 1.5), scale=1.0,
                                     shift=0.3))
        self.add_sprite(SpriteObject(game, path="data/sprites/props/dead_body.png", pos=(11.5, 2.5), scale=0.75, shift=0.25))

        # врагов добавлять сюда:

        self.add_enemy(Trooper(game, pos=(13.5, 2.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(12.5, 6.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(6.75, 17.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(13.5, 19.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(5.5, 15.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(8.5, 15.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(1.5, 23.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(21.5, 19.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(19.5, 16.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(18.5, 3.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(19.5, 3.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(21.5, 3.5), scale=0.75, shift=0.25))
        self.add_enemy(Trooper(game, pos=(18.5, 3.5), scale=0.75, shift=0.25))

        self.add_enemy(FastAsFuckBoi(game, pos=(22.5, 22.5)))
        self.add_enemy(FastAsFuckBoi(game, pos=(22.5, 25.5)))
        self.add_enemy(FastAsFuckBoi(game, pos=(17.5, 15.5)))
        self.add_enemy(FastAsFuckBoi(game, pos=(16.5, 7.5)))
        self.add_enemy(FastAsFuckBoi(game, pos=(25.5, 7.5)))
        self.add_enemy(FastAsFuckBoi(game, pos=(22.5, 5.5)))


    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update(self):
        self.enemy_positions = {enemy.map_pos() for enemy in self.enemy_list if enemy.alive}
        [sprite.update() for sprite in self.sprite_list]
        [enemy.update() for enemy in self.enemy_list]

    def add_enemy(self, some_enemy):
        self.enemy_list.append(some_enemy)

