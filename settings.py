from math import *
width, height = 1600, 900  # --> разрешение
half_width = width // 2
half_heigth = height // 2
fps = 0

player_coords = 1.5, 5 # --> стартовая позиция
player_angle = 0
player_speed = 0.004 # --> скорость перемещения игрока
player_rot_speed = 0.002 # --> скорость разворота игрока

fov = pi / 3
half_fov = pi / 6
num_rays = width // 2
half_num_rays = width // 6
d_angle = fov / num_rays
max_depth = 20

screen_dist = half_width / tan(half_fov)
scale = width // num_rays