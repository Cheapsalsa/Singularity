import math
import pygame


def KeyGetPressedList():
    """Returns a list of the pressed keys as a sequence of strings."""
    pygame.event.pump()
    pressed = pygame.key.get_pressed()
    result = []
    for i in range(0,len(pressed)):
        if pressed[i] != 0:
            result.append(pygame.key.name(i))
    return result


def KeyIsPressed(KeySymbol):
    """Return a 1 if the specified key is pressed 0 if it isn't"""
    if KeySymbol in KeyGetPressedList():
        return 1
    else:
        return 0


def KeyIsNotPressed(KeySymbol):
    """Return a 1 if the specified key is not pressed 0 if it is"""
    if KeySymbol not in KeyGetPressedList():
        return 1
    else:
        return 0


def collidingCircles(c1x, c1y, c1r, c2x, c2y, c2r):
    """
    :param c1x: x of the first circle region
    :param c1y: y of the first circle region
    :param c1r: radius of the first circle region
    :param c2x: x of the second circle region
    :param c2y: y of the second circle region
    :param c2r: radius of the first circle region
    :return: This returns True if we the two circle regions are colliding and False if they are not.
    """
    if (int(c1x) - int(c2x)) ** 2 + (int(c1y) - int(c2y)) ** 2 <= (int(c1r) + int(c2r)) ** 2:
        return True
    return False