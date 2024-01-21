import pygame
# все звуки игры


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = "data/sfx/"
        self.shotgun = pygame.mixer.Sound(self.path + "shotgun.wav")
        self.enemy_pain = pygame.mixer.Sound(self.path + "enemy_pain.wav")
        self.enemy_death = pygame.mixer.Sound(self.path + "enemy_death.wav")
        self.enemy_attack = pygame.mixer.Sound(self.path + "enemy_attack.wav")
        self.player_pain = pygame.mixer.Sound(self.path + "player_pain.wav")
        self.doom_lvl_theme = pygame.mixer.Sound(self.path + "ebat' chertei.mp3")
