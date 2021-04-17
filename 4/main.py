import sys

import pygame
import requests

coord = '27.780603,53.858644'
coords = [27.780603, 53.858644]
z = 10

params_for_map = {
    'l': 'map',
}
map_files = []

pygame.init()
screen = pygame.display.set_mode((600, 400))
status = [0, 1, 1]

keys = {0: 'map', 1: 'sat', 2: 'skl'}


def draw_interface():
    global status
    x = 5
    for i in range(3):
        pygame.draw.rect(screen, 'red', (x, 5, 45, 45), status[i])
        x += 50


def change_status(pos):
    global status, params_for_map, keys
    x, y = pos
    if x <= 150 and y <= 50:
        n = x // 51
        status = [1, 1, 1]
        status[n] = 0
        params_for_map['l'] = keys[n]
        update()


def mouse_update(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        change_status(event.pos)


def update():
    map_request = f"http://static-maps.yandex.ru/1.x"
    params_for_map['z'] = z
    params_for_map['ll'] = ','.join([str(i) for i in coords])
    response = requests.get(map_request, params_for_map)

    if not response:
        print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.fill((0, 0, 0))
    screen.blit(pygame.image.load(map_file), (0, 0))
    draw_interface()
    pygame.display.flip()


def change_coords(arr):
    global coords
    coords[0] += arr[0]
    coords[1] += arr[1]
    if coords[0] > 180:
        coords[0] = 180
    elif coords[0] < -180:
        coords[0] = -180
    elif coords[1] > 90:
        coords[1] = 90
    elif coords[1] < -90:
        coords[1] = -90

    print(coords)


def update_zoom(key):
    global z
    if key == pygame.K_PAGEUP:
        if z < 22:
            z += 1
            update()
    elif key == pygame.K_PAGEDOWN:
        if z > 1:
            z -= 1
            update()


def update_coords(key):
    global z
    t = 5 / z
    if key in [119, 1073741906]:
        change_coords([0, t])
        update()
    elif key in [115, 1073741905]:
        change_coords([0, -t])
        update()
    elif key in [1073741904, 97]:
        change_coords([-t, 0])
        update()
    elif key in [1073741903, 100]:
        change_coords([t, 0])
        update()


def check_key(key):
    print(key)
    update_zoom(key)
    update_coords(key)


update()
run = True
while run:

    for event in pygame.event.get():
        mouse_update(event)
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            check_key(event.key)

pygame.quit()
