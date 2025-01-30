import pygame
import math
import settings


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < settings.height:
                wall_column = self.textures[texture].subsurface(
                    offset * (settings.texture_size - settings.scale), 0, settings.scale, settings.texture_size
                )
                wall_column = pygame.transform.scale(wall_column, (settings.scale, proj_height))
                wall_pos = (ray * settings.scale, settings.half_heigth - proj_height // 2)
            else:
                texture_height = settings.texture_size * settings.height / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (settings.texture_size - settings.scale), settings.half_texture_size - texture_height // 2,
                    settings.scale, texture_height
                )
                wall_column = pygame.transform.scale(wall_column, (settings.scale, settings.height))
                wall_pos = (ray * settings.scale, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        texture_vert, texture_hor = 1, 1
        ox, oy = self.game.player.position()  # --> нач корды игрока
        x_map, y_map = self.game.player.map_pos()  # --> корды клетки игрока

        ray_angle = self.game.player.angle - settings.half_fov + 0.000001
        for ray in range(settings.num_rays):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            if sin_a > 0:
                y_hor, dy = y_map + 1, 1
            else:  # ------> горизонтали
                y_hor, dy = y_map - 1e-6, -1

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(settings.max_depth):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.wmap:
                    texture_hor = self.game.map.wmap[tile_hor]
                    break
                else:
                    x_hor += dx
                    y_hor += dy
                    depth_hor += delta_depth
            # --------------------------------------ох зря я не учил тригонометрию--------------------------------------
            if cos_a > 0:
                x_vert, dx = x_map + 1, 1
            else:  # ---------------> вертикали
                x_vert, dx = x_map - 1e-6, -1

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(settings.max_depth):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.wmap:
                    texture_vert = self.game.map.wmap[tile_vert]
                    break
                else:
                    x_vert += dx
                    y_vert += dy
                    depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            depth *= math.cos(self.game.player.angle - ray_angle)  # --> убирает эффект рыбего глаза
            # расчет проекции высоты стен
            proj_height = settings.screen_dist / (depth + 0.00001)
            # рисование самих стен
            # pygame.draw.rect(self.game.screen, "white",
            #                 (ray * settings.scale, settings.half_heigth - proj_height // 2,
            #                  settings.scale, proj_height))
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            ray_angle += settings.d_angle

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

    def get_texture(self, path, res=(settings.texture_size, settings.texture_size)):
        texture = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(texture, res)
