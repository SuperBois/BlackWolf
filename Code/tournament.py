import pygame, sys
from pygame.locals import *
import math
import random

pygame.init()
font = pygame.font.Font(None, 23)
font_2 = pygame.font.Font(None, 34)

back_x = 100
back_y = -400
back_rect = pygame.Rect(back_x, back_y, 1400, 900)

car = pygame.image.load("Images\\lamborghini2.png")

ground = pygame.image.load("Images\\new_groundpatch.png")
ground_rect = ground.get_rect()
ground_rect.center = back_rect.center
image = car
pos_x, pos_y = back_x + (-110), back_y + (850)


def new_position(object_x, object_y, angle, up, down):
    '''Calculates ang returns the new position of the object relative to the player'''
    if up:
        object_x -= round(speed * math.cos(math.radians(angle)))
        object_y += round(speed * math.sin(math.radians(angle)))

    if down:
        object_x += round(speed * math.cos(math.radians(angle)))
        object_y -= round(speed * math.sin(math.radians(angle)))
    return object_x, object_y


def second_element(list):
    '''returns the second element of the list'''
    return list[1]


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def set_angles(angle, car_dict):
    '''Sets the angles of the given car_dict for proper movement of the car'''
    if angle >= 360:
        angle = 0
    if angle == 0:
        car_dict['prev_angle'] = 0
        car_dict['next_angle'] = 90
    elif angle == 90:
        car_dict['prev_angle'] = 90
        car_dict['next_angle'] = 180
    elif angle == 180:
        car_dict['prev_angle'] = 180
        car_dict['next_angle'] = 270
    elif angle == 270:
        car_dict['prev_angle'] = 270
        car_dict['next_angle'] = 360
    return angle, car_dict


def traffic_cars(screen, car_list, scrolling_angle, up, down):
    """Controls the behaviour of all the cars in the car_list"""
    for car_dict in car_list:
        rect = car_dict['rect']
        angle = car_dict['angle']
        image = car_dict['image']
        min_angle = car_dict['prev_angle']
        max_angle = car_dict['next_angle']
        static_image = car_dict['static_image']

        rotate = False
        can_move = True
        # Checks for collisions with the rotation triggers
        for item in other_list:
            if rect.colliderect(item) and item != car_dict['collided_rect']:
                car_dict['collided_rect'] = item
                rotate = True
        # keeps rotating the car while angle is between min_angle and max_angle
        if min_angle < angle < max_angle:
            rotate = True
        if angle == max_angle:
            rotate = False

        if rotate:
            angle += 5
            image, rect = rot_center(static_image, rect, angle)

        # On collision with lap_counter rect increment the laps_completed in the respective car_Dict
        if rect.colliderect(lap_counter) and lap_counter != car_dict['collided_rect'] and car_dict[
            'laps_completed'] < max_laps:
            if [car_dict['name'], car_dict['laps_completed']] in leaders:
                leaders.remove([car_dict['name'], car_dict['laps_completed']])

            car_dict['laps_completed'] += 1
            leaders.append([car_dict['name'], car_dict['laps_completed']])
            car_dict['collided_rect'] = lap_counter
            leaders.sort(key=second_element, reverse=True)
        # If car can_move then controls its movement
        if can_move:
            rect.x += round(car_dict['speed'] * math.cos(math.radians(angle)))
            rect.y -= round(car_dict['speed'] * math.sin(math.radians(angle)))

        # Sets the previous and next angles for the given dict
        angle, car_dict = set_angles(angle, car_dict)

        # Updates the values within the dictionaries
        car_dict['image'], car_dict['rect'], car_dict['angle'] = image, rect, angle
        # Displays the car on the screen
        screen.blit(car_dict['image'], car_dict['rect'])
        # updates the position of the car_rect
        rect.x, rect.y = new_position(rect.x, rect.y, scrolling_angle, up, down)
        # Creating and displaying tags
        tag_surface = font.render(car_dict['name'], True, (255, 255, 255))
        screen.blit(tag_surface, rect)

    return car_list


#### Initializing all the variables that will be used in the game
car_list = []
names = ['Danish', 'Haris', 'Taha', 'Mustafa', 'Manahil']
car_images = ['red', 'green', 'cyan', 'blue', 'pink', 'orange']

for new_car in range(5):
    pos_x += 200
    image_surface = pygame.image.load(f'Images\\game_cars\\rotated\\car_{car_images[new_car]}.png')
    car_dict = {'name': names[new_car], 'image': image_surface, 'static_image': image_surface,
                'rect': car.get_rect(center=(pos_x, pos_y)), 'prev_angle': 0, 'angle': 0,
                'next_angle': 90, 'speed': random.randint(8, 9), 'collided_rect': None, 'laps_completed': -1}
    car_list.append(car_dict)

other_list = [pygame.Rect(back_x + 1200, back_y + 90, 150, 10),
              pygame.Rect(back_x + 1230, back_y + 760, 10, 150),
              pygame.Rect(back_x + 150, back_y + 40, 10, 150),
              pygame.Rect(back_x + 60, back_y + 750, 150, 10)]
player_name = 'User'
leaders = []

# Player dictionary which contains stores all the properties related to the player
player_dict = {'name': player_name, 'image': car, 'rect': car.get_rect(center=(400, 350)),
               'speed': 9, 'collided_rect': None, 'laps_completed': -1}

# Lap counter rect
lap_counter = pygame.Rect(1310, 300, 200, 10)
angle = 0
speed = 2
rotate = False
heading1 = 'Leader Board'
heading2 = 'Name      Laps'

# Headings surfaces
heading1_surface = font.render(heading1, True, (255, 0, 0))
heading2_surface = font.render(heading2, True, (0, 255, 0))
lap_increase = True

max_laps = 3
max_laps_surface = font.render(f'max laps: {max_laps}', True, (255, 255, 255))


def game_over(screen, username, leaders):
    # Checks if the username is among the top three positions in the leaderboard
    if username == leaders[0][0]:
        position = font_2.render('Congratulations!! You secured first position.', True, (255, 255, 255))
        coins_text = font.render("You have received 1000 coins", True, (255, 255, 255))

    elif username == leaders[1][0]:
        position = font_2.render('Congratulations!! You secured second position.', True, (255, 255, 255))
        coins_text = font.render("You have received 700 coins", True, (255, 255, 255))

    elif username == leaders[2][0]:

        position = font_2.render('Congratulations!! You secured third position.', True, (255, 255, 255))
        coins_text = font.render("You have received 400 coins", True, (255, 255, 255))
    else:
        position = font_2.render('You lost the race :-|', True, (255, 255, 255))
        coins_text = font.render('Try harder next time', True, (255, 255, 255))
    instructions = font.render('Press ESCAPE to get back to main_game', True, (255, 255, 255))
    screen.blit(position, (200, 350))

    screen.blit(coins_text, (200, 400))
    screen.blit(instructions, (200, 500))


def game(screen, username, screen_width, coins):
    global car_list, angle, up, down, speed, lap_increase
    # clear display #
    up = False
    down = False
    player_dict['name'] = username
    screen.fill((77, 77, 77))
    if player_dict['laps_completed'] < max_laps:
        pygame.draw.rect(screen, (63, 63, 63), back_rect)
        screen.blit(ground, (ground_rect))
        screen.blit(heading1_surface, (60, 10))
        screen.blit(heading2_surface, (50, 40))
        screen.blit(max_laps_surface, (screen_width - 200, 40))

        # Displays the names of leaders
        x_pos = 50  # Space from left
        y_pos = 70  # Space from top
        for sub_list in leaders:
            for entry in sub_list:
                text_surface = font.render(str(entry), True, (250, 250, 250))
                screen.blit(text_surface, (x_pos, y_pos))
                x_pos += 100
            x_pos = 50
            y_pos += 30  # Space on y-axis between 2 names

        # Decreasing the speed of car outside the map
        if not player_dict['rect'].colliderect(back_rect) or player_dict['rect'].colliderect(ground_rect):
            speed = 3
        else:
            speed = player_dict['speed']

        if player_dict['rect'].colliderect(other_list[2]):
            lap_increase = True

        pygame.draw.rect(screen, (230, 230, 230), lap_counter)

        # Checking the state (pressed / unpressed) of keys and storing them in variable
        keys = pygame.key.get_pressed()
        # Checking the key pressed and moving the background with respect to arrow keys pressed
        if keys[K_UP]:
            up = True
            back_rect.x -= round(speed * math.cos(math.radians(angle)))
            back_rect.y += round(speed * math.sin(math.radians(angle)))
        if keys[K_DOWN]:
            down = True
            back_rect.x += round(speed * math.cos(math.radians(angle)))
            back_rect.y -= round(speed * math.sin(math.radians(angle)))
        if keys[K_RIGHT]:
            angle -= 1.5
            player_dict['image'], player_dict['rect'] = rot_center(car, player_dict['rect'], angle)
        if keys[K_LEFT]:
            angle += 1.5
            player_dict['image'], player_dict['rect'] = rot_center(car, player_dict['rect'], angle)

        # updating the position of every object on map while car is moving
        for item in other_list:
            item.x, item.y = new_position(item.x, item.y, angle, up, down)

        lap_counter.x, lap_counter.y = new_position(lap_counter.x, lap_counter.y, angle, up, down)
        ground_rect.x, ground_rect.y = new_position(ground_rect.x, ground_rect.y, angle, up, down)

        # checking for collisions with the the loop counter rect
        if player_dict['rect'].colliderect(lap_counter) and lap_increase:
            lap_increase = False
            if [username, player_dict['laps_completed']] in leaders:
                leaders.remove([username, player_dict['laps_completed']])
            player_dict['laps_completed'] += 1
            player_dict['collided_rect'] = lap_counter
            leaders.append([username, player_dict['laps_completed']])
            leaders.sort(key=second_element, reverse=True)

        # adding the collided_rect to a list to increase number of laps only on first collision
        for item in other_list:
            if player_dict['rect'].colliderect(item) and item != player_dict['collided_rect']:
                player_dict['collided_rect'] = item

        # Displaying the car_surface on the screen
        screen.blit(player_dict['image'], player_dict['rect'])
        # Creating and displaying the tag for the user
        tag_surface = font.render(username, True, (255, 255, 255))
        screen.blit(tag_surface, player_dict['rect'])
        # updating the other cars on the map
        car_list = traffic_cars(screen, car_list, angle, up, down)
        state = 'tournament'
    else:
        keys = pygame.key.get_pressed()
        end = keys[pygame.K_ESCAPE]
        game_over(screen, username, leaders)
        if end:
            if username == leaders[0][0]:
                coins += 1000
            if username == leaders[1][0]:
                coins += 700
            if username == leaders[2][0]:
                coins += 200
            print(coins)
            with open(f"profiles\\profile_{username}.txt", "w") as file:
                user_profile = {'username': username, 'coins': coins}
                file.writelines(f'{user_profile}')
            state = 'main_game'

        else:
            state = 'tournament'
    return state, coins
