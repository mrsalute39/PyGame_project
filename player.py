import settings
from math import *
import pygame


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = settings.player_coords
        self.angle = settings.player_angle

    def movement(self):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        dx, dy = 0, 0
        speed = settings.player_speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pygame.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pygame.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pygame.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_collision(dx, dy)

        if keys[pygame.K_LEFT]:
            self.angle -= settings.player_rot_speed * self.game.delta_time
        if keys[pygame.K_RIGHT]:
            self.angle += settings.player_rot_speed * self.game.delta_time
        self.angle %= tau

    def draw(self):
        #pygame.draw.line(self.game.screen, "red", (self.x * 100, self.y * 100),
        #                 (self.x * 100 + settings.width * cos(self.angle),
        #                  self.y * 100 + settings.width * sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, "blue", (self.x * 100, self.y * 100), 15)

    def check_wall(self, x, y):
        if (x, y) not in self.game.map.wmap:
            return True
        else:
            return False

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def update(self):
        self.movement()

    def position(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x), int(self.y)
