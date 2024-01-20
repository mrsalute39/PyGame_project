import pygame
import settings


class Renderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_texture()
        self.sky_image = self.get_texture("data/textures/why.png", settings.width, settings.half_heigth)
        self.sky_offset = 0

    def draw(self):
        self.draw_sky_and_floor()
        self.render_game_objects()

    def draw_sky_and_floor(self):
        self.sky_offset = (self.sky_offset + 4.5 * self.game.player.rel) % settings.width
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + settings.width, 0))

        pygame.draw.rect(self.screen, settings.floor_color, (0, settings.half_heigth, settings.width, settings.height))

    def render_game_objects(self):
        list_of_objects = sorted(self.game.raycasting.objects_to_render, key=lambda x: x[0], reverse=True)
        for depth, img, pos in list_of_objects:
            self.screen.blit(img, pos)

    def get_texture(self, path, t_width, t_height):
        res = t_width, t_height
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)

    def load_wall_texture(self):
        textures_dict = {
            1: self.get_texture("data/textures/1.png", settings.texture_size, settings.texture_size),
            2: self.get_texture("data/textures/2.png", settings.texture_size, settings.texture_size),  # --- > текстурки равны номеру на карте в матрице уровня
            3: self.get_texture("data/textures/3.png", settings.texture_size, settings.texture_size)
        }
        return textures_dict
