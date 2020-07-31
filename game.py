import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.font.init()
WIDTH = 1280
HEIGHT = 720
clock = pygame.time.Clock()

# fonts
LABEL = pygame.font.Font('resources/fonts/purista.otf', 18)
HEADER = pygame.font.Font('resources/fonts/purista.otf', 24)
TITLE = pygame.font.Font('resources/fonts/purista.otf', 64)
PARAGRAPH = pygame.font.Font('resources/fonts/purista.otf', 12)

# colours
BLUE = (0, 51, 103)
DARKBLUE = (0, 38, 76)
GREY = (175, 175, 175)
WHITE = (242, 242, 242)


def main_menu():
    running = True

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(pygame.Color("#003367"))
    
    pygame.display.set_caption("Battleship 2020")

    label = pygame.font.Font('resources/fonts/purista.otf', 32)
    
    title = pygame.font.Font('resources/fonts/purista.otf', 64)
    text = title.render("Battleship", True, pygame.Color("#FFFFFF"))
    screen.blit(text, (16, 16))

    btn_play = pygame.draw.rect(screen, pygame.Color("#00264e"), (54, 196, 256, 48))
    text = label.render("Play", True, pygame.Color("#FFFFFF"))
    screen.blit(text, (62, 196))
    
    btn_options = pygame.draw.rect(screen, pygame.Color("#00264e"), (54, 268, 256, 48))
    text = label.render("Options", True, pygame.Color("#FFFFFF"))
    screen.blit(text, (62, 268))
    
    btn_exit = pygame.draw.rect(screen, pygame.Color("#00264e"), (54, 340, 256, 48))
    text = label.render("Exit", True, pygame.Color("#FFFFFF"))
    screen.blit(text, (62, 340))

    pygame.display.update()
    while running:
        mx, my = pygame.mouse.get_pos()
        if btn_play.collidepoint((mx, my)):
            pygame.draw.polygon(screen, pygame.Color("#00264e"), [(16, 204), (16, 236), (48, 220)])
        else:
            pygame.draw.rect(screen, pygame.Color("#003367"), (16, 204, 36, 36))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        pygame.display.update()


def options():
    running = True
    while running:
        pass


def _add_button(screen, text, position, dimensions):
    x, y = position
    w, h = dimensions
    rectangle = (x, y, w, h)
    button = pygame.draw.rect(screen, BLUE, rectangle)
    label = LABEL.render(text, True, WHITE)
    screen.blit(label, label.get_rect(center=button.center))
    border = pygame.draw.rect(screen, GREY, rectangle, 1)


def add_big_button(screen, text, position):
    _add_button(screen, text, position, (214, 48))


def add_button(screen, text, position):
    _add_button(screen, text, position, (120, 32))


def draw_text(screen, text, font, position):
    textbox = font.render(text, True, WHITE)
    screen.blit(textbox, position)


def draw_ship_silhoutte(screen, image, rectangle):
    x, y, w, h = rectangle
    sil = pygame.image.load(image)
    sil = pygame.transform.scale(sil, (w, h))
    screen.blit(sil, (x, y))


def draw_sidebar(screen):
    rectangle = (WIDTH // 2, 0, WIDTH // 2, HEIGHT)
    sidebar = pygame.draw.rect(screen, DARKBLUE, rectangle)
    pygame.draw.line(screen, GREY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)

    draw_text(screen, "Deployment", TITLE, (678, 0))

    # composition
    draw_text(screen, "Fleet Composition", HEADER, (678, 100))
    draw_text(screen, "Select a ship to place it on the grid to the left", PARAGRAPH, (678, 133))
    draw_text(screen, "Right-click to undo placement", PARAGRAPH, (678, 148))
    draw_ship_silhoutte(screen, "resources/images/SIL_CARRIER_W.png", (678, 192, 251, 50))
    draw_text(screen, "Aircraft Carrier", PARAGRAPH, (678, 246))
    draw_ship_silhoutte(screen, "resources/images/SIL_CRUISER_W.png", (980, 178, 180, 64))
    draw_text(screen, "Missile Cruiser", PARAGRAPH, (980, 246))
    draw_ship_silhoutte(screen, "resources/images/SIL_SUBMARINE_W.png", (678, 310, 181, 50))
    draw_text(screen, "Submarine", PARAGRAPH, (678, 364))
    draw_ship_silhoutte(screen, "resources/images/SIL_DESTROYER_W.png", (878, 300, 181, 60))
    draw_text(screen, "Destroyer", PARAGRAPH, (878, 364))
    draw_ship_silhoutte(screen, "resources/images/SIL_BOAT_W.png", (1079, 310, 161, 50))
    draw_text(screen, "Patrol Boat", PARAGRAPH, (1079, 364))

    # orientation
    draw_text(screen, "Ship Orientation", HEADER, (678, 404))
    draw_text(screen, "Placement orientation of the current selected ship", PARAGRAPH, (678, 436))
    add_button(screen, "Horizontal", (678, 460))
    add_button(screen, "Vertical", (832, 460))

    # difficulty
    draw_text(screen, "Enemy Difficulty", HEADER, (678, 517))
    draw_text(screen, "Difficulty of the opposing player", PARAGRAPH, (678, 549))
    add_button(screen, "Easy", (678, 573))
    add_button(screen, "Medium", (832, 573))
    add_button(screen, "Hard", (986, 573))

    # bottom buttons
    add_big_button(screen, "Begin Operation", (678, 648))
    add_big_button(screen, "Reset Deployment", (922, 648))
    
    pygame.display.update()


def game():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(BLUE)
    draw_sidebar(screen)
    pygame.display.set_caption("Battleship 2020")
    pygame.display.update()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()


if __name__ == "__main__":
    game()