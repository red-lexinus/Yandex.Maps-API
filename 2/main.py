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


def update():
    map_request = f"http://static-maps.yandex.ru/1.x"
    params_for_map['z'] = z
    params_for_map['ll'] = coord
    response = requests.get(map_request, params_for_map)

    if not response:
        print("Ошибка выполнения запроса:")
    print(response.url)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()


update()
run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            # print(event.key)
            # if event.key in [119, 1073741906]:
            #     print(z)
            #     if z != 22:
            #         z += 1
            #         update()
            # elif event.key in [115, 1073741905]:
            #     print(z)
            #     if z != 1:
            #         z -= 1
            #         update()
            if event.key == pygame.K_PAGEUP:
                if z < 22:
                    z += 1
                    update()
            elif event.key == pygame.K_PAGEDOWN:
                if z > 1:
                    z -= 1
                    update()

pygame.quit()
