import pygame
import math
import settings


class RayCasting:
    def __init__(self, game):
        self.game = game

    def ray_cast(self):
        ox, oy = self.game.player.position()  # --> нач корды игрока
        x_map, y_map = self.game.player.map_pos() # --> корды клетки игрока

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
                    break
                else:
                    x_vert += dx
                    y_vert += dy
                    depth_vert += delta_depth

            if depth_vert < depth_hor:
                depth = depth_vert
            else:
                depth = depth_hor

            #расчет проекции высоты стен
            proj_height = settings.screen_dist / (depth + 0.00001)
            # рисование самих стен
            pygame.draw.rect(self.game.screen, "white",
                             (ray * settings.scale, settings.half_heigth - proj_height // 2,
                              settings.scale, proj_height))
            ray_angle += settings.d_angle

    def update(self):
        self.ray_cast()
