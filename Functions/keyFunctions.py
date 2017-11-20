import pygame


def key_get_pressed_list():
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    result = []
    for i in range(0,len(pressed)):
        if pressed[i] != 0:
            result.append(pygame.key.name(i))
    return result


def key_is_pressed(keySymbol):
    if keySymbol in key_get_pressed_list():
        return 1
    else:
        return 0


def key_is_not_pressed(keySymbol):
    if keySymbol not in key_get_pressed_list():
        return 1
    else:
        return 0



