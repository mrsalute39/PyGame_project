import pygame


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = "data/sfx/"
        self.shotgun = pygame.mixer.Sound(self.path + "shotgun.wav")