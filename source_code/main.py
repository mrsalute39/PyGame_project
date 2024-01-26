import pygame
import sys
from button import Button
from game import Game
from moviepy.editor import *
import settings
from DataBaseEditor import *

pygame.init()
pygame.mixer.init()
main_menu_theme = pygame.mixer.Sound("data/sfx/menu_theme.mp3")
main_menu_theme.play(-1)
screen = pygame.display.set_mode((settings.width, settings.height))
pygame.display.set_caption("Меню")
background = pygame.image.load("data/textures/bg.png")

db = DataBaseEditor()


def get_font(size):
    return pygame.font.Font("data/font/bender.otf", size)


def play():
    pygame.mixer.stop()
    path = "data/videos/intro.mp4"
    pygame.display.set_caption("""ИНТРО""")
    pygame.display.set_mode((settings.width, settings.height), pygame.FULLSCREEN)

    intro = VideoFileClip(path)
    intro.preview()

    pygame.quit()

    game = Game()
    game.run()


def stats():
    player_stats = db.get_stats()
    while True:
        stats_mouse_pos = pygame.mouse.get_pos()

        screen.fill("black")

        stats_text = get_font(100).render("Ваша статистика:", True, "#85004B")
        stats_rect = stats_text.get_rect(center=(950, 160))
        screen.blit(stats_text, stats_rect)

        kills_text = get_font(50).render(f"Убийств:----------------------------> {player_stats[0]}", True, "#85004B")
        kills_rect = kills_text.get_rect(center=(930, 335))
        screen.blit(kills_text, kills_rect)

        deaths_text = get_font(50).render(f"Смертей:----------------------------> {player_stats[1]}", True, "#85004B")
        deaths_rect = deaths_text.get_rect(center=(930, 410))
        screen.blit(deaths_text, deaths_rect)

        shots_text = get_font(50).render(f"Выстрелов:----------------------------> {player_stats[2]}", True, "#85004B")
        shots_rect = shots_text.get_rect(center=(930, 485))
        screen.blit(shots_text, shots_rect)

        damage_text = get_font(50).render(f"Нанесено урона:----------------------------> {player_stats[3]}",
                                          True, "#85004B")
        damage_rect = damage_text.get_rect(center=(930, 560))
        screen.blit(damage_text, damage_rect)

        completions_text = get_font(50).render(f"Прохождения игры:----------------------------> {player_stats[4]}",
                                               True, "#85004B")
        completions_rect = completions_text.get_rect(center=(930, 635))
        screen.blit(completions_text, completions_rect)

        stats_back_button = Button(image=pygame.image.load("data/textures/collision_rect.png"),
                                   pos=(950, 900), text_input="Назад", font=get_font(75),
                                   base_color="white", hovering_color="#85004B")

        stats_back_button.change_color(stats_mouse_pos)
        stats_back_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if stats_back_button.check_for_input(stats_mouse_pos):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        screen.blit(background, (0, 0))
        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(200).render("Главное меню", True, "#85004B")
        menu_rect = menu_text.get_rect(center=(950, 200))

        play_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(950, 450),
                             text_input="Играть", font=get_font(75), base_color="white", hovering_color="#85004B")
        stats_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(950, 600),
                              text_input="Статистика", font=get_font(75), base_color="white", hovering_color="#85004B")
        quit_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(950, 750),
                             text_input="Выйти", font=get_font(75), base_color="white", hovering_color="#85004B")
        screen.blit(menu_text, menu_rect)
        buttons = [play_button, stats_button, quit_button]

        for btn in buttons:
            btn.change_color(menu_mouse_pos)
            btn.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if stats_button.check_for_input(menu_mouse_pos):
                    stats()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()


if __name__ == '__main__':
    main_menu()
