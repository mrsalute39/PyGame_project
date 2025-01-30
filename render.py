import pygame
import settings
from random import randint


class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_texture()
        self.sky_image = self.get_texture("data/textures/night_sky.png", settings.width, settings.half_heigth)
        self.sky_offset = 0
        self.damage_screen = self.get_texture("data/textures/damage.png", settings.width, settings.height)
        self.digit_size = 90
        self.digit_images = [self.get_texture(f"data/textures/digits/{i}.png",
                                              self.digit_size, self.digit_size) for i in range(11)]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture(f"data/textures/game_overs/game_over{randint(0, 21)}.png",
                                                settings.width, settings.height)
        self.crosshair_image = self.get_texture("data/textures/crosshair.png", 35, 35)
        self.win_screen_image = self.get_texture("data/textures/ending.png", settings.width, settings.height)
        self.black_screen = self.get_texture("data/textures/black_screen.png", settings.width, settings.height)

    def draw(self):
        self.draw_sky_and_floor()
        self.render_game_objects()
        self.draw_player_health()
        self.draw_crosshair()

    def draw_player_health(self):
        health = str(self.game.player.health)
        for i, char in enumerate(health):
            self.screen.blit(self.digits[char], ((i + 2.20) * self.digit_size, 70))
        self.screen.blit(self.digits["10"], ((i + 3.20) * self.digit_size, 70))

    def draw_sky_and_floor(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % settings.width
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + settings.width, 0))

        pygame.draw.rect(self.screen, settings.floor_color, (0, settings.half_heigth, settings.width, settings.height))

    def draw_crosshair(self):
        self.screen.blit(self.crosshair_image, (settings.half_width, settings.half_heigth))

    def player_damage(self):
        self.screen.blit(self.damage_screen, (0, 0))

    def render_game_objects(self):
        list_of_objects = sorted(self.game.raycasting.objects_to_render, key=lambda x: x[0], reverse=True)
        for depth, img, pos in list_of_objects:
            self.screen.blit(img, pos)

    def get_texture(self, path, t_width, t_height):
        res = t_width, t_height
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def game_over(self):
        self.screen.blit(self.black_screen, (0, 0))
        self.screen.blit(self.game_over_image, (0, 0))

    def win_screen(self):
        self.screen.blit(self.win_screen_image, (0, 0))

    def load_wall_texture(self):
        textures_dict = {
            1: self.get_texture("data/textures/531.jpg", settings.texture_size, settings.texture_size),
            2: self.get_texture("data/textures/crate.png", settings.texture_size, settings.texture_size),
            # --- > текстурки равны номеру на карте в матрице уровня
            3: self.get_texture("data/textures/533.jpg", settings.texture_size, settings.texture_size),
            4: self.get_texture("data/textures/532.png", settings.texture_size, settings.texture_size),
            5: self.get_texture("data/textures/container_blue.png", settings.texture_size, settings.texture_size),
            6: self.get_texture("data/textures/container_green.jpg", settings.texture_size, settings.texture_size),
            7: self.get_texture("data/textures/container_violet.jpg", settings.texture_size, settings.texture_size),
            8: self.get_texture("data/textures/534.png", settings.texture_size, settings.texture_size),
            9: self.get_texture("data/textures/shrine.jpg", settings.texture_size, settings.texture_size),
            10: self.get_texture("data/textures/tro.png", settings.texture_size, settings.texture_size)
        }
        return textures_dict
