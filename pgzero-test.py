import pgzrun
import pygame

TITLE = "The Hate Circuit"
WIDTH = 800
HEIGHT = 600

def draw():
    screen.clear()
    screen.surface = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    screen.draw.circle((400, 300), 30, "white")


pgzrun.go()
