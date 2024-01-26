import pygame
import settings
import math
import os
from collections import deque


class SpriteObject:
    def __init__(self, game, path="data/sprites/props/apel.png", pos=(10.5, 3.5), scale=0.4, shift=1.0):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pygame.image.load(path).convert_alpha()
        self.image_width = self.image.get_width()
        self.image_half_width = self.image.get_width() // 2
        self.image_ratio = self.image_width / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.sprite_scale = scale
        self.sprite_height_shift = shift

    def get_sprite_projection(self):
        proj = settings.screen_dist / self.norm_dist * self.sprite_scale
        proj_width, proj_height = proj * self.image_ratio, proj

        image = pygame.transform.scale(self.image, (proj_width, proj_height))

        self.sprite_half_width = proj_width // 2
        height_shift = proj_height * self.sprite_height_shift
        pos = self.screen_x - self.sprite_half_width, settings.half_heigth - proj_height // 2 + height_shift

        self.game.raycasting.objects_to_render.append((self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        self.theta = math.atan2(dy, dx)

        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau

        delta_rays = delta/settings.d_angle
        self.screen_x = (settings.half_num_rays + delta_rays) * settings.scale

        self.dist = math.hypot(dx, dy)
        self.norm_dist = self.dist * math.cos(delta)
        if -self.image_half_width < self.screen_x < (settings.width + self.image_half_width) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()


class AnimatedSprite(SpriteObject):
    def __init__(self, game, path="data/sprites/animated_props/burning_barrel/burning_barrel_0.png",
                 pos=(11.5, 3.5), scale=0.8, shift=0.15, animation_time=120):
        super().__init__(game, path, pos, scale, shift)
        self.animation_time = animation_time
        self.path = path.rsplit("/", 1)[0]
        self.images = self.get_images(self.path)
        self.animation_time_prev = pygame.time.get_ticks()
        self.animation_trigger = False

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pygame.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            self.image = images[0]

    def get_images(self, path):
        images = deque()
        for fname in os.listdir(path):
            if os.path.isfile(os.path.join(path, fname)):
                img = pygame.image.load(path + "/" + fname).convert_alpha()
                images.append(img)
        return images

    def update(self):
        super().update()
        self.check_animation_time()
        self.animate(self.images)
