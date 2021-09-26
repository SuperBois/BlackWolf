import pygame, sys
from pygame.locals import *

mainClock = pygame.time.Clock()
pygame.init()
font1 = pygame.font.SysFont("Comic Sans MS", 30)
font2 = pygame.font.SysFont("Comic Sans MS", 20)

def show_text(text ,font ,color,surface , x, y):
    textobj = font.render(text , 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def load_preview(screen, car_image):
    screen.blit(car_image, (600, 180))

def purchase(coins, purchased,image, image_surface):
    image_colors = ['red', 'green', 'blue', 'pink', 'orange', 'yellow']
    if coins > 0:
        for color in image_colors:
            if image == f"Images\\cars_preview\\car_{color}.png" and purchased != color:
                coins -= 100
                image_surface = pygame.image.load(f"Images\\game_cars\\car_{color}.png")
                purchased = color

    return coins, purchased, image_surface


def main_menu(coins, purchased, screen, font1, font2, image, image_surface, username,state):
    click = False
    while state == 'paint_shop':
        screen.fill((0, 0, 0))

        mx, my = pygame.mouse.get_pos()
        # First two coordinates = pos. on screen, Last two coordinates = Size of rect
        button_red = pygame.Rect(20, 140, 50,50)
        button_green = pygame.Rect(100, 140, 50, 50)
        button_yellow = pygame.Rect(180, 140, 50, 50)
        button_blue = pygame.Rect(20, 220, 50, 50)
        button_pink = pygame.Rect(100, 220, 50, 50)
        button_orange = pygame.Rect(180, 220, 50, 50)
        button_purchase = pygame.Rect(30, 350, 150, 50)
        button_go_back = pygame.Rect(340, 500, 100, 50)

        if button_red.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_red.png"
        if button_green.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_green.png"
        if button_yellow.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_yellow.png"
        if button_blue.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_blue.png"
        if button_pink.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_pink.png"
        if button_orange.collidepoint((mx, my)):
            if click:
                image = "Images\\cars_preview\\car_orange.png"

        if button_purchase.collidepoint((mx, my)):
            if click:
                coins, purchased, image_surface = purchase(coins, purchased, image, image_surface)

        if button_go_back.collidepoint((mx,my)):
            # Resetting image for the case if user selects a color without purchasing and leaves the menu.
            if click:  # In that case, when user pops menu again , the last selected color pallette preview is shown rather than the color of car
                image = f"Images\\cars_preview\\car_{purchased}.png"  # This if statements handle that condition by resetting image value when you leave the paint shop menu to the color of car
                state = 'main_game'
                with open(f"profiles\\profile_{username}.txt", "w") as file:
                    user_profile = {'username': username, 'coins': coins}
                    file.writelines(f'{user_profile}')

        click = False

        pygame.draw.rect(screen, (255, 0, 0), button_red)
        pygame.draw.rect(screen, (15, 252, 3), button_green)
        pygame.draw.rect(screen, (252, 244, 3), button_yellow)
        pygame.draw.rect(screen, (20, 3, 252), button_blue)
        pygame.draw.rect(screen, (252, 3, 252), button_pink)
        pygame.draw.rect(screen, (252, 161, 3), button_orange)
        pygame.draw.rect(screen, (252, 255, 255), button_purchase)
        pygame.draw.rect(screen, (252, 255, 255), button_go_back)

        show_text("Paint Shop", font1, (255, 255, 255), screen, 20, 20)
        show_text("Choose a color", font2, (255, 255, 255), screen, 30, 70)
        show_text("Go back", font2, (0, 0, 0), screen, 350, 510)
        show_text("Purchase", font2, (0, 0, 0), screen, 57, 357)
        show_text("Coins: ", font1, (255, 255, 255), screen, 600, 20)
        show_text(str(coins), font2, (255, 255, 255), screen, 700, 28)
        show_text(f"{purchased.capitalize()} color equipped", font2, (255, 255, 255), screen, 300, 400)

        if coins == 0:
            show_text("No Coins Left", font2, (255, 255, 255), screen, 330, 450)

        car_image = pygame.image.load(image)
        load_preview(screen, car_image)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        mainClock.tick(45)
    return coins, purchased, image, image_surface,state
