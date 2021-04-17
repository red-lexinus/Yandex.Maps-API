import os
import sys

import pygame
import requests

coord = '27.780603,53.858644'
z = '10'

params_for_map = {
    'l': 'map',
}
map_files = []
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

pygame.init()
screen = pygame.display.set_mode((600, 400))

run = True
while run:
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

pygame.quit()
