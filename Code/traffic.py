import math,pygame
from game_functions import *

def update_angle(car_dict):
    angle = car_dict['theeta']
    if angle == 360 or angle == -360:
        car_dict['theeta'] = 0

    if angle == 0:
        car_dict['prev_theeta'] = 0
        car_dict['next_theeta'] = 90

    elif angle == 90:
        car_dict['prev_theeta'] = 90
        car_dict['next_theeta'] = 180

    elif angle == 180:
        car_dict['prev_theeta'] = 180
        car_dict['next_theeta'] = 270

    elif angle == 270:
        car_dict['prev_theeta'] = 270
        car_dict['next_theeta'] = 360

    elif angle == 360:
        car_dict['prev_theeta'] = 0
        car_dict['next_theeta'] = 90
        car_dict['theeta'] = 0
        return car_dict



def traffic_cars(screen,car_list, player_dict, obj_dict):
    other_list = obj_dict['colliders']
    player = player_dict['rect']

    for car_dict in car_list:
        rect = car_dict['rect']
        angle = car_dict['theeta']
        speed = car_dict['speed']
        image = car_dict['image']
        min_theeta = car_dict['prev_theeta']
        max_theeta = car_dict['next_theeta']
        static_image = car_dict['static_image']

        rotate = False

        for item in other_list:
            if rect.colliderect(item) and item != car_dict['collided_rect']:
                car_dict['collided_rect'] = item
                rotate = True
        if min_theeta < angle < max_theeta:
            rotate = True
        if angle == max_theeta:
            rotate = False
        if rotate:
            angle += 10
            image, rect = rot_center(static_image, rect, angle)

        if not rect.colliderect(player):
            rect.x += round(speed * math.cos(math.radians(angle+90)))
            rect.y -= round(speed * math.sin(math.radians(angle+90)))


        car_dict['image'], car_dict['rect'], car_dict['theeta'] = image, rect, angle

        screen.blit(image,rect)
        update_angle(car_dict)
        rect.x, rect.y = new_position(rect.x, rect.y, player_dict)




    return car_list
