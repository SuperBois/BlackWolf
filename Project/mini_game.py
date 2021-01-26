import pygame, sys, random
import paint_shop
from pygame.locals import *


mainClock = pygame.time.Clock()
pygame.init()

#LOADING IMAGES
background_image = pygame.image.load("Images\\bg.jpg")
mini_game_area = pygame.image.load("Images\\mini_game_region.png")
car_colors = ['green', 'red', 'pink', 'blue', 'orange']
player_car_surface = pygame.image.load("Images\\game_cars\\car_yellow.png")

#GETTING RECT
player = player_car_surface.get_rect()
player.center = (390, 500)



def random_cars(car_image_surface):
    '''spawns random cars on screen'''

    obstacle = car_image_surface.get_rect()
    obstacle.center = (380, 0)
    return obstacle, car_image_surface


def mini_game(state, coins, screen, username):
    ''''''
    right = False
    left = False
    speed = 10
    count = 0

    difficulty = 0
    collision_counter = 0
    random_cars_surface = pygame.image.load(f"Images//game_cars//inverted//car_{'red'}.png")
    obstacle, random_cars_surface = random_cars(random_cars_surface)
    possible_x_positions = [290, 300 ,380,390, 450,460]
    coin_surface = pygame.image.load(f"Images//game_cars//inverted//coin_image2.jpg")
    coin = coin_surface.get_rect()
    coin.center = (380, -50)
    while state == "mini_game":
        screen.fill((0,0,0))
        random_color = random.choice(car_colors)



        movement_x = 0
        movement_y = 0

        if right == True:
            movement_x += 5
        if left == True:
            movement_x -= 5
        if player.x < 290:
            left = False

        if player.x > 470:
            right = False

        player.x += movement_x
        player.y += movement_y

        obstacle.y += speed

        if count > 5:
            coin.y += 5
            if coin.y > 600:
                coin.y = -100
                coin.x = random.choice(possible_x_positions)
                count = 0


        if obstacle.y > 600:
            obstacle.y = -100
            obstacle.x = random.choice(possible_x_positions)
            random_cars_surface = pygame.image.load(f"Images//game_cars//inverted//car_{random_color}.png")
            count += 1
            difficulty += 1
        screen.fill((0, 0, 0))
        screen.blit(background_image, [0, 0])
        screen.blit(mini_game_area, [280, -1])
        screen.blit(player_car_surface, player)
        screen.blit(random_cars_surface, obstacle)
        screen.blit(coin_surface, coin)


        paint_shop.show_text("Mini-game", paint_shop.font1, (255, 255,255), screen, 20, 20)
        paint_shop.show_text(f"Collision Counter: {collision_counter}", paint_shop.font2, (255, 0,0), screen, 20, 90)
        paint_shop.show_text(f"Coins: {coins}", paint_shop.font1, (255, 255, 255),screen, 620, 20)






        if player.colliderect(coin):
            coins += 50
            coin.y = -400
            coin.x = random.choice(possible_x_positions)
            count = 0

        if player.colliderect(obstacle):
            collision_counter += 1
            obstacle.y = -400
            obstacle.x = random.choice(possible_x_positions)
            difficulty = 0


        if difficulty > 5:
            speed += 2
            difficulty = 0

        if collision_counter == 3:
            state = 'main_game'
            with open(f"profiles//profile_{username}.txt", "w") as file:
                user_profile = {'username': username, 'coins': coins}
                file.writelines(f'{user_profile}')

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_RIGHT and player.x < 470:
                    right = True
                if event.key == K_LEFT and player.x > 290:
                    left = True

            if event.type == KEYUP:
                if event.key == K_RIGHT:
                    right = False
                if event.key == K_LEFT:
                    left = False

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        mainClock.tick(60)
    return state,coins