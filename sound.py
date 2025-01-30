import pygame
# все звуки игры


class Sound:
    def __init__(self, game):
        self.game = game
        pygame.mixer.init()
        self.path = "data/sfx/"
        self.music_volume = round(self.game.settings_dict["music_volume"], 2)
        self.effect_volume = round(self.game.settings_dict["effect_volume"], 2)

        self.shotgun = pygame.mixer.Sound(self.path + "shotgun.wav")
        self.enemy_pain = pygame.mixer.Sound(self.path + "enemy_pain.wav")
        self.enemy_death = pygame.mixer.Sound(self.path + "enemy_death.wav")
        self.enemy_attack = pygame.mixer.Sound(self.path + "enemy_attack.wav")
        self.player_pain = pygame.mixer.Sound(self.path + "player_pain.wav")
        self.doom_lvl_theme = pygame.mixer.Sound(self.path + "theme.mp3")

        self.effect_list = [self.shotgun, self.enemy_pain, self.enemy_death, self.enemy_attack, self.player_pain]

        for sound_effect in self.effect_list:
            sound_effect.set_volume(self.effect_volume)
        self.doom_lvl_theme.set_volume(self.music_volume)
