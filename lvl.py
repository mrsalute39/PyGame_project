import pygame

layout = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 1, 1, 0, 0, 1, 1, 1],
          [1, 0, 0, 1, 0, 0, 0, 1, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
          [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
          [1, 0, 0, 0, 1, 1, 0, 0, 0, 1], # 0 --> пустое пространство
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]] # 1 --> стена


class Map:
    def __init__(self, game):
        self.game = game
        self.layout = layout
        self.wmap = {}
        self.get_map()

    def get_map(self):
        for i, row in enumerate(self.layout):
            for j, val in enumerate(row):
                if val:
                    self.wmap[(j, i)] = val

    def draw(self):
        [pygame.draw.rect(self.game.screen, "white", (pos[0] * 100, pos[1] * 100, 100, 100), 2) for pos in self.wmap]


