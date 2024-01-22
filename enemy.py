from sprite_object import *
from random import randint, random, choice


class Enemy(AnimatedSprite):
    def __init__(self, game, path="data/sprites/enemy/soldier/0.png", pos=(10.5, 5.5), scale=0.6,
                 shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_images = self.get_images(self.path + "/attack")
        self.death_images = self.get_images(self.path + "/death")
        self.idle_images = self.get_images(self.path + "/idle")
        self.pain_images = self.get_images(self.path + "/pain")
        self.walk_images = self.get_images(self.path + "/walk")

        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False

        # хар-ки врага
        self.attack_dist = randint(3, 6)
        self.speed = 0.028
        self.size = 10
        self.health = 100
        self.attack_damage = randint(10, 16)
        self.accuracy = 0.2

        # состояние врага
        self.alive = True
        self.pain = False

    def update(self):
        self.check_animation_time()
        self.get_sprite()
        self.run_logic()
        # self.draw_ray_cast() # --> для 2д дебага убрать коммент

    def check_enemy_got_hit(self):  # --> проверка попадания игрока по врагу
        if self.ray_cast_value and self.game.player.shot:
            if settings.half_width - self.sprite_half_width \
                    < self.screen_x < settings.half_width + self.sprite_half_width:
                self.game.player.shot = False
                self.game.sound.enemy_pain.play()
                self.pain = True
                self.health -= self.game.weapon.damage
                self.check_health()

    def run_logic(self):  # --- > запускает мозг противника
        if self.alive:
            self.ray_cast_value = self.ray_cast_check()
            self.check_enemy_got_hit()
            if self.pain:
                self.animate_pain()

            elif self.ray_cast_value:
                self.player_search_trigger = True

                if self.dist < self.attack_dist:
                    self.animate(self.attack_images)
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()

            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()

            else:
                self.animate(self.idle_images)
        else:
            self.animate_death()

    def check_wall(self, x, y):
        if (x, y) not in self.game.map.wmap:
            return True
        else:
            return False

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * self.size)):
            self.y += dy

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos(), self.game.player.map_pos())
        next_x, next_y = next_pos

        # pygame.draw.rect(self.game.screen, "green", (100 * next_x, 100 * next_y, 100, 100))
        # -- > рисует клетки куда пойдет враг(2д режим)
        if next_pos not in self.game.creator.enemy_positions:
            angle = math.atan2(next_y + 0.5 - self.y, next_x + 0.5 - self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_collision(dx, dy)

    def attack(self):
        if self.animation_trigger:
            self.game.sound.enemy_attack.play()
            if random() < self.accuracy:
                self.game.player.get_damage(self.attack_damage)

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.sound.enemy_death.play()

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def animate_death(self):
        if not self.alive:
            if self.game.global_trigger and self.frame_counter < len(self.death_images) - 1:
                self.death_images.rotate(-1)
                self.image = self.death_images[0]
                self.frame_counter += 1

    def map_pos(self):
        return int(self.x), int(self.y)

    def ray_cast_check(self):  # -- > запуск рейкаста для проверки коллизии стен(чтобы игрок не стрелял сковзь них)
        if self.game.player.map_pos() == self.map_pos():
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.position()
        x_map, y_map = self.game.player.map_pos()

        ray_angle = self.theta
        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        if sin_a > 0:
            y_hor, dy = y_map + 1, 1
        else:
            y_hor, dy = y_map - 1e-6, -1

        depth_hor = (y_hor - oy) / sin_a
        x_hor = ox + depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(settings.max_depth):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos():
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.wmap:
                wall_dist_h = depth_hor
                break
            else:
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

        if cos_a > 0:
            x_vert, dx = x_map + 1, 1
        else:
            x_vert, dx = x_map - 1e-6, -1

        depth_vert = (x_vert - ox) / cos_a
        y_vert = oy + depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(settings.max_depth):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos():
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.wmap:
                wall_dist_v = depth_vert
                break
            else:
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)  # -- > результаты рейкаста и послед проверка
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            return True
        else:
            return False

    def draw_ray_cast(self):  # --- > рисует линию от игрока до врага (для демонстрации)
        pygame.draw.circle(self.game.screen, "red", (100 * self.x, 100 * self.y), 15)
        if self.ray_cast_check():
            pygame.draw.line(self.game.screen, "orange", (100 * self.game.player.x, 100 * self.game.player.y),
                             (100 * self.x, 100 * self.y), 2)


# --- > все враги

class SoldierDoom(Enemy):
    def __init__(self, game, path="data/sprites/enemy/soldier/0.png", pos=(10.5, 5.5), scale=0.6,
                 shift=0.38, animation_time=180):
        super().__init__(game, path, pos, scale, shift, animation_time)


class CacoDemonDoom(Enemy):
    def __init__(self, game, path="data/sprites/enemy/cacodemon/0.png", pos=(10.5, 5.5), scale=1.0,
                 shift=0.25, animation_time=150):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.attack_dist = 1.0
        self.health = 150
        self.attack_damage = randint(20, 26)
        self.speed = 0.04
        self.accuracy = 0.5
