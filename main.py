import pygame
import sys
import settings
import lvl
import player
import raycasting
import render
import sprite_object
import object_creator
import shotgun
import sound


class Game:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        self.clock = pygame.time.Clock()
        self.game_status = True
        self.start_new_game()
        self.delta_time = 1

    def start_new_game(self):
        self.map = lvl.Map(self)
        self.player = player.Player(self)
        self.object_renderer = render.Renderer(self)
        self.raycasting = raycasting.RayCasting(self)
        self.creator = object_creator.ObjectHandler(self)
        self.shotgun = shotgun.Shotgun(self)
        self.sound = sound.Sound(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.creator.update()
        self.shotgun.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(settings.fps)
        pygame.display.set_caption(f"{int(self.clock.get_fps())}")

    def draw(self):
        # self.screen.fill("black") # 2д задник
        self.object_renderer.draw()  # --> 3д вид
        self.shotgun.draw()
        # self.map.draw() # 2д вид
        # self.player.draw() #2д карта

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_status = False
                # pygame.quit()
            self.player.single_fire_event(event)

    def run(self):
        while self.game_status:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
