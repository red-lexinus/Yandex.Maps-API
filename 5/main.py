import sys
import pygame_gui
import pygame
import requests
import json

x = 38.205085
y = 44.419486
z = 17

params_for_map = {}


def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 20)
    text = font.render(text, True, (255, 255, 255))
    text_x, text_y = x, y
    screen.blit(text, (text_x, text_y))


map_files = []

pygame.init()
screen = pygame.display.set_mode((600, 400))
type_ = 'map'
run = True
sat = pygame.Rect((0, 2), (20, 20))
map = pygame.Rect((40, 2), (20, 20))
gbr = pygame.Rect((80, 2), (20, 20))


def make_req(place):
    global x, y
    try:
        res = requests.get(
            f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={place}&format=json")
        res = res.json()
        res = res["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        c = res["Point"]["pos"]
        c = c.split()
        x = float(c[0])
        y = float(c[1])
        print(c)

    except Exception:
        print("Ошибка")


manager = pygame_gui.UIManager((600, 400))
clock = pygame.time.Clock()

entry = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((105, 0), (120, 25)), manager=manager
)

run = True


def update_display():
    global rects_, rects
    time_delta = clock.tick(60) / 1000.0
    map_request = f"http://static-maps.yandex.ru/1.x"
    params_for_map['z'] = z
    params_for_map['ll'] = f'{x},{y}'
    params_for_map['l'] = type_
    params_for_map['pt'] = f"{x},{y},pm2rdm"
    response = requests.get(map_request, params_for_map)
    rects = [(sat, 'S', 'sat'), (map, 'M', 'map'), (gbr, 'G', 'sat,skl')]
    if not response:
        print("Ошибка выполнения запроса:")
        print(response.url)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    screen.blit(pygame.image.load(map_file), (0, 0))

    for i in range(3):
        rect = rects[i][0]
        text = rects[i][1]
        pygame.draw.rect(screen, (0, 0, 0), rect)
        draw_text(screen, text, rect.x + 2, rect.y + 1)
    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()


while run:
    global rects_, rects
    update_display()
    for event in pygame.event.get():
        manager.process_events(event)

        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_PAGEUP:
                if z != 22:
                    z += 1
            if event.key == pygame.K_UP:
                y += 0.5
            elif event.key == pygame.K_DOWN:
                y -= 0.5
            elif event.key == pygame.K_RIGHT:
                x += 0.5
            elif event.key == pygame.K_LEFT:
                x -= 0.5
            elif event.key == pygame.K_PAGEDOWN:
                if z != 1:
                    z -= 1
        elif event.type == pygame.MOUSEBUTTONUP:
            rects_ = [i[0] for i in rects]
            for list_ in rects:
                rect = list_[0]
                if rect.collidepoint(event.pos):
                    type_ = list_[2]
        elif event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                make_req(event.text)

pygame.quit()