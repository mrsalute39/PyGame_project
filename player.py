import sys
from math import *
import pygame
from DataBaseEditor import *
from moviepy.editor import *
import settings
from time import sleep


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = settings.player_coords
        self.angle = settings.player_angle
        self.shot = False
        self.rel = 0
        self.health = settings.player_max_health
        self.health_recovery_delay = 1000
        self.time_prev = pygame.time.get_ticks()

        self.kill_counter = 0
        self.shots_counter = 0
        self.damage_counter = 0
        self.death_counter = 0
        self.game_completed_counter = 0

        self.player_counters = [self.kill_counter, self.death_counter,
                                self.shots_counter, self.damage_counter, self.game_completed_counter]

    def single_fire_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                self.game.sound.shotgun.play()
                self.shot = True
                self.shots_counter += 1  # --- > счет выстрелов игрока
                self.game.weapon.reloading = True

    def get_damage(self, damage):
        self.health -= damage
        self.game.object_renderer.player_damage()
        self.game.sound.player_pain.play()
        self.game_over()

    def check_health_recovery_delay(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.time_prev > self.health_recovery_delay:
            self.time_prev = time_now
            return True

    def start_recover_health(self):
        if self.check_health_recovery_delay() and self.health < settings.player_max_health:
            self.health += 1

    def movement(self, flag):
        sin_a = sin(self.angle)
        cos_a = cos(self.angle)
        dx, dy = 0, 0
        speed = settings.player_speed * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pygame.key.get_pressed()
        if flag:
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
            self.angle %= tau

    def draw(self):
        pygame.draw.line(self.game.screen, "red", (self.x * 100, self.y * 100),
                         (self.x * 100 + settings.width * cos(self.angle),  # убрать коменты для 2д вида
                          self.y * 100 + settings.width * sin(self.angle)), 2)
        pygame.draw.circle(self.game.screen, "blue", (self.x * 100, self.y * 100), 15)

    def check_wall(self, x, y):
        if (x, y) not in self.game.map.wmap:
            return True
        else:
            return False

    def game_over(self):
        if self.health < 1:
            self.game.theme.stop()

            self.game.object_renderer.game_over()
            self.game.player_movement_flag = False
            self.death_counter += 1

            self.db_editor = DataBaseEditor([self.kill_counter,
                                             self.death_counter, self.shots_counter, self.damage_counter,
                                             self.game_completed_counter])
            self.db_editor.update_db()
            pygame.display.flip()
            pygame.time.wait(1500)
            self.game.start_new_game()

    def win_screen_hooray(self):
        if self.map_pos() == (31, 4):
            self.game_completed_counter += 1

            self.db_editor = DataBaseEditor([self.kill_counter,
                                             self.death_counter, self.shots_counter, self.damage_counter,
                                             self.game_completed_counter])
            self.db_editor.update_db()
            self.game.theme.stop()

            path = "data/videos/ending.mp4"

            pygame.display.set_icon(self.game.icon)
            pygame.display.set_caption("КОНЦОВКА")

            pygame.display.set_mode((settings.width, settings.height))
            outro = VideoFileClip(path)
            outro.preview()

            pygame.quit()
            sys.exit()

    def check_collision(self, dx, dy):
        scale = settings.player_size_scale / self.game.delta_time  # фикс ---> шакаливание картинки при
        # приближении и просмотра сковзь стены добавляя размер игроку
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def mouse_control(self):
        mx, my = pygame.mouse.get_pos()
        if mx < settings.mouse_border_left or mx > settings.mouse_border_right:
            pygame.mouse.set_pos([settings.half_width, settings.half_heigth])
        self.rel = pygame.mouse.get_rel()[0]
        self.rel = max(-settings.mouse_max_rel, min(settings.mouse_max_rel, self.rel))
        self.angle += self.rel * settings.mouse_sens * self.game.delta_time

    def update(self, player_movement_flag):
        self.mouse_control()
        self.movement(player_movement_flag)
        self.start_recover_health()
        self.win_screen_hooray()

    def position(self):
        return self.x, self.y

    def map_pos(self):
        return int(self.x), int(self.y)
