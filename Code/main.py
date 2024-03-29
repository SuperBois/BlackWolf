import pygame, sys, random, math
from map_generation import *
from game_functions import *
from player import *
from paint_shop import *
import tournament
from traffic import *
from mini_game import *
from space_shooter import *



def read_coins(username):
    with open(f"profiles//profile_{username}.txt") as file:           #This function will read the user's profile from profile folder
        profile_info = file.readlines()
        profile_dict = eval(profile_info[0])
        coins = profile_dict['coins']
    return coins

def game(username, state):
    # initializes the pygame window
    pygame.init()
    clock = pygame.time.Clock()
    # CAPTION
    pygame.display.set_caption('BlackWolf')
    # SCREEN DIMENSIONS
    screen_width = 800
    screen_height = 600

    # Creates a window of size screen_width and screen_height
    screen = pygame.display.set_mode((screen_width, screen_height), 0, 32)

    # Stores all the objects on screen and their images in the form of a dictionary
    obj_dict, obj_img_dict, shops = create_map(screen)

    # initializes the state of the game

    player_dict = initialize_player()
    angle = 0

    # list of dictionaries of all cars
    car_dict_list = car_dicts(obj_dict['car'], obj_img_dict['car'])
    coins = read_coins(username)

    ended = False

    while state != 'end':
        # FOR ENDING GAME

        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if events.type == pygame.KEYDOWN:
                # checks if 'f' key is pressed and player colliding with any car

                if events.key == pygame.K_f and not player_dict['is_driving'] and collided_obj(player_dict, car_dict_list,'rect'):
                    player_dict['is_driving'] = True

                elif events.key == pygame.K_f and player_dict['is_driving']:
                    player_dict['is_driving'] = False

        keys = pygame.key.get_pressed()

        up = keys[pygame.K_UP]
        down = keys[pygame.K_DOWN]
        left = keys[pygame.K_LEFT]
        right = keys[pygame.K_RIGHT]

        player_rect = player_dict['rect']

        for key,values in shops.items():
            if player_rect.colliderect(shops[key][0]):
                state = key
                if state == 'space_shooter':
                    ended = False
                diff = player_rect.x - (obj_dict[key][0].x) + shops[key][0].width
                player_rect.x = shops[key][0].x + 20
                print(player_rect.x, player_rect.y)
                for keys, values in obj_dict.items():
                    for rect in obj_dict[keys]:
                        rect.x += diff

        if state == 'main_game':
            # clears the screen (by filling it with colour)
            screen.fill((77, 77, 77))
            # updating the movement of the player
            player_dict['movement'] = [up, down, left, right]
            # displays all objects on screen
            collision_side(screen,player_dict,obj_dict)
            #traffic
            scroll_objects(screen,player_dict, obj_dict)
            display(screen, obj_dict, obj_img_dict)

            traffic_cars(screen, car_dict_list, player_dict, obj_dict)
            display_player(screen, player_dict)

        elif state == 'paint_shop':
            coins, player_dict['purchased'], player_dict['image_path'], player_dict['car'], state = main_menu(coins,
                                                                                                          player_dict['purchased'],
                                                                                                          screen,
                                                                                                          font1,
                                                                                                          font2,
                                                                                                          player_dict['image_path'],
                                                                                                          player_dict['car'],
                                                                                                          username,
                                                                                                          state)
            player_dict['static_car'] = player_dict['car']

        elif state == 'tournament':
            state, coins = tournament.game(screen, username, screen_width, coins)

        elif state == 'mini_game':
            state, coins = mini_game(state, coins, screen, username)

        elif state == 'space_shooter':
            state , coins, ended = space_shooter(screen,coins,state,username,ended)

        # Limits the framerate of the game
        clock.tick(60)

        pygame.display.update()
