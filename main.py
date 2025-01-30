import pygame
import pygame_menu as pm
import sys
import json
from button import Button
from game import Game
from moviepy.editor import *
import settings
from DataBaseEditor import *
from math import tan

settings_window_font = pm.font.get_font("data/font/bender.otf", 65)
mytheme = pm.Theme(background_color=(0, 0, 0, 0),
                   title_background_color=(0, 0, 0), widget_font=settings_window_font, selection_color="#85004B")

pygame.init()
pygame.mixer.init()

icon = pygame.image.load("data/icon/icon.ico")
pygame.display.set_icon(icon)

with open("data/configs/settings.json", "r") as f:
    settings_from_json = json.load(f)

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Меню")
background = pygame.image.load("data/textures/bg.png")

db = DataBaseEditor()

settings_manager = pm.Menu(title="", width=1280, height=600, theme=mytheme)
settings_manager._theme.widget_font_size = 65
settings_manager._theme.widget_font_color = "white"

possible_resolution = [
    ("1280x720", (1280, 720), 0.68),
    ("1920x1080", (1920, 1080), 0.88),
    ("2560x1440", (2560, 1440), 1.08),
    ("3840x2160", (3840, 2160), 1.28)
]

settings_manager.add.dropselect(title="Разрешение экрана", items=possible_resolution,
                                dropselect_id="resolution", default=settings_from_json["resolution"][1], max_selected=1)

settings_manager.add.range_slider(title="Громкость музыки", default=round(settings_from_json["music_volume"], 2),
                                  range_values=(
                                      0.0, 1.0), increment=1, value_format=lambda x: str(round(float(x), 2)),
                                  rangeslider_id="music_volume")
settings_manager.add.range_slider(title="Громкость эффектов", default=round(settings_from_json["effect_volume"], 2),
                                  range_values=(
                                      0.0, 1.0), increment=1, value_format=lambda x: str(round(float(x), 2)),
                                  rangeslider_id="effect_volume")

main_menu_theme = pygame.mixer.Sound("data/sfx/menu_theme.mp3")
main_menu_theme.set_volume(round(settings_from_json["music_volume"], 2))
main_menu_theme.play(-1)

save_settings_effect = pygame.mixer.Sound("data/sfx/save_settings.wav")
save_settings_effect.set_volume(round(settings_from_json["effect_volume"], 2))


def get_font(size):
    return pygame.font.Font("data/font/bender.otf", size)


def play():
    pygame.mixer.stop()
    path = "data/videos/intro.mp4"
    pygame.display.set_caption("""ИНТРО""")
    pygame.display.set_mode((settings.width, settings.height))

    intro = VideoFileClip(path)
    intro.preview()

    pygame.quit()

    game = Game(settings_from_json)
    game.run()


def stats():
    player_stats = db.get_stats()
    while True:
        stats_mouse_pos = pygame.mouse.get_pos()

        screen.fill("black")

        stats_text = get_font(100).render("Ваша статистика:", True, "#85004B")
        stats_rect = stats_text.get_rect(center=(650, 100))
        screen.blit(stats_text, stats_rect)

        kills_text = get_font(50).render(f"Убийств:----------------------------> {player_stats[0]}", True, "#85004B")
        kills_rect = kills_text.get_rect(center=(630, 235))
        screen.blit(kills_text, kills_rect)

        deaths_text = get_font(50).render(f"Смертей:----------------------------> {player_stats[1]}", True, "#85004B")
        deaths_rect = deaths_text.get_rect(center=(630, 310))
        screen.blit(deaths_text, deaths_rect)

        shots_text = get_font(50).render(f"Выстрелов:----------------------------> {player_stats[2]}", True, "#85004B")
        shots_rect = shots_text.get_rect(center=(630, 385))
        screen.blit(shots_text, shots_rect)

        damage_text = get_font(50).render(f"Нанесено урона:----------------------------> {player_stats[3]}",
                                          True, "#85004B")
        damage_rect = damage_text.get_rect(center=(600, 460))
        screen.blit(damage_text, damage_rect)

        completions_text = get_font(50).render(f"Прохождения игры:----------------------------> {player_stats[4]}",
                                               True, "#85004B")
        completions_rect = completions_text.get_rect(center=(630, 535))
        screen.blit(completions_text, completions_rect)

        stats_back_button = Button(image=pygame.image.load("data/textures/collision_rect.png"),
                                   pos=(650, 650), text_input="Назад", font=get_font(75),
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

        menu_text = get_font(170).render("Главное меню", True, "#85004B")
        menu_rect = menu_text.get_rect(center=(650, 100))

        play_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(650, 240),
                             text_input="Играть", font=get_font(75), base_color="white", hovering_color="#85004B")
        stats_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(650, 375),
                              text_input="Статистика", font=get_font(75), base_color="white", hovering_color="#85004B")
        settings_window_button = Button(image=pygame.image.load("data/textures/collision_rect.png"),
                                        pos=(650, 520), text_input="Настройки", font=get_font(75), base_color="white",
                                        hovering_color="#85004B")
        quit_button = Button(image=pygame.image.load("data/textures/collision_rect.png"), pos=(650, 655),
                             text_input="Выйти", font=get_font(75), base_color="white", hovering_color="#85004B")

        screen.blit(menu_text, menu_rect)
        buttons = [play_button, stats_button, quit_button, settings_window_button]

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
                if settings_window_button.check_for_input(menu_mouse_pos):
                    settings_window()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


def settings_window():
    text_color = "black"
    while True:

        stats_mouse_pos = pygame.mouse.get_pos()
        screen.fill("black")
        settings_back_button = Button(image=pygame.image.load("data/textures/collision_rect.png"),
                                      pos=(300, 650), text_input="Назад", font=get_font(75),
                                      base_color="white", hovering_color="#85004B")
        settings_save_button = Button(image=pygame.image.load("data/textures/collision_rect.png"),
                                      pos=(950, 650), text_input="Сохранить", font=get_font(75),
                                      base_color="white", hovering_color="#85004B")
        settings_back_button.change_color(stats_mouse_pos)
        settings_back_button.update(screen)
        settings_save_button.change_color(stats_mouse_pos)
        settings_save_button.update(screen)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if settings_back_button.check_for_input(stats_mouse_pos):
                    main_menu()
                if settings_save_button.check_for_input(stats_mouse_pos):
                    save_settings()
                    text_color = "#85004B"
        if settings_manager.is_enabled():
            settings_manager.update(events)
            settings_manager.draw(screen)

        settings_text = get_font(50).render("Настройки вступят в силу после перезапуска :)", True, text_color)
        settings_rect = settings_text.get_rect(center=(650, 150))

        screen.blit(settings_text, settings_rect)
        pygame.display.update()


def save_settings():
    save_settings_effect.play()
    settings_data = settings_manager.get_input_data()  # cловарь с ключами 'resolution', 'music_volume, 'effect_volume'
    with open("data/configs/settings.json", "w") as f:
        json.dump(settings_data, f)


def apply_existing_settings():
    if os.path.exists("data/configs/settings.json"):
        with open("data/configs/settings.json", "r") as f:
            local_settings = json.load(f)
        re_init_settings_file(local_settings)


def re_init_settings_file(settings_dict):  # --> переинициализирует файл с настройками, не лучшее решение но мне лень
    settings.width, settings.height = settings_dict['resolution'][0][1]
    settings.half_width = settings.width // 2
    settings.half_heigth = settings.height // 2
    settings.num_rays = settings.width // 2
    settings.half_num_rays = settings.num_rays // 2
    settings.d_angle = settings.fov / settings.num_rays
    settings.screen_dist = settings.half_width / tan(settings.half_fov)
    settings.scale = settings.width // settings.num_rays


if __name__ == '__main__':
    apply_existing_settings()
    main_menu()
