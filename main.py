import pygame
import sys
import settings
import lvl
import player
import raycasting

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.width, settings.height))
        self.clock = pygame.time.Clock()
        self.game_status = True
        self.start_new_game()
        self.delta_time = 1

    def start_new_game(self):
        self.map = lvl.Map(self)
        self.player = player.Player(self)
        self.raycasting = raycasting.RayCasting(self)


    def update(self):
        self.player.update()
        self.raycasting.update()
        pygame.display.flip()
        self.delta_time = self.clock.tick(settings.fps)
        pygame.display.set_caption(f"{int(self.clock.get_fps())}")

    def draw(self):
        self.screen.fill("black")
        #self.map.draw()
        #self.player.draw()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_status = False
                #pygame.quit()

    def run(self):
        while self.game_status:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
