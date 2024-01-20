from sprite_object import *
# ---------СОЗДАТЕЛЬ ОБЪЕКТОВ-------------------------------------------------------------------------------------------
# упрощает создание пропов, спрайтов, врагов, прочего


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = list()
        self.static_sprite_path = "data/sprites/props/"
        self.animated_sprites_path = "data/sprites/animated_props/"

        # сюда добавлять спрайты:
        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprite(game))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update(self):
        [sprite.update() for sprite in self.sprite_list]
