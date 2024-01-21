from math import *
width, height = 1600, 900  # --> разрешение
half_width = width // 2
half_heigth = height // 2
fps = 0

player_coords = 1.5, 1.5 # --> стартовая позиция
player_angle = 0
player_speed = 0.004 # --> скорость перемещения игрока
player_rot_speed = 0.002 # --> скорость разворота игрока
player_size_scale = 60
player_max_health = 100

mouse_sens = 0.00015
mouse_max_rel = 40
mouse_border_left = 100
mouse_border_right = width - mouse_border_left

fov = pi / 3
half_fov = fov / 2
num_rays = width // 2
half_num_rays = num_rays // 2
d_angle = fov / num_rays
max_depth = 20

screen_dist = half_width / tan(half_fov)
scale = width // num_rays # --- > колво прямоугольников на экране (коэф для оптимизации)

texture_size = 256
half_texture_size = texture_size // 2
floor_color = (30, 30, 30)