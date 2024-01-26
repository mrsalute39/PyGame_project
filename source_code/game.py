import pygame
import settings
import lvl
import player
import raycasting
import render
import object_creator
import shotgun
import sound
import enemy_behaviour
from DataBaseEditor import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()

        self.game_status = True
        self.start_new_game()
        self.delta_time = 1

        self.global_trigger = False
        self.global_event = pygame.USEREVENT + 0
        pygame.time.set_timer(self.global_event, 70)

    def start_new_game(self):
        self.map = lvl.Map(self)
        self.player = player.Player(self)
        self.object_renderer = render.Renderer(self)
        self.raycasting = raycasting.RayCasting(self)
        self.creator = object_creator.ObjectHandler(self)
        self.weapon = shotgun.Shotgun(self)
        self.sound = sound.Sound(self)
        self.pathfinding = enemy_behaviour.PathFinding(self)
        self.theme = self.sound.doom_lvl_theme.play(-1)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.creator.update()
        self.weapon.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(settings.fps)
        pygame.display.set_caption(f"{int(self.clock.get_fps())}")

    def draw(self):
        # self.screen.fill("black") # 2д задник
        self.object_renderer.draw()  # --> 3д вид
        self.weapon.draw()
        # self.map.draw() # 2д вид
        # self.player.draw() #2д карта

    def check_events(self):
        self.global_trigger = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:

                self.db_editor = DataBaseEditor([self.player.kill_counter,
                                                 self.player.death_counter, self.player.shots_counter,
                                                 self.player.damage_counter,
                                                 self.player.game_completed_counter])
                self.db_editor.update_db()

                self.game_status = False
                pygame.quit()
            elif event.type == self.global_event:
                self.global_trigger = True
            self.player.single_fire_event(event)

    def run(self):
        while self.game_status:
            self.check_events()
            self.update()
            self.draw()
