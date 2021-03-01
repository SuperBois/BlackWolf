import pygame
import math
import random

particles = []
def create_objects(grounds, num_objects, object_width, object_height, padx, pady):
    objects = []

    for ground_rect in grounds:
        pos_x = ground_rect.x + padx
        pos_y = ground_rect.y + pady

        for create in range(num_objects):

            if pos_x + object_width > ground_rect.topright[0]:
                pos_x = ground_rect.x + padx
                pos_y += object_height + pady

            if pos_y + object_height > ground_rect.bottom:
                break

            object_rect = pygame.Rect(pos_x, pos_y, object_width, object_height)
            objects.append(object_rect)
            pos_x += object_width + padx
    return objects

def create_cars(grounds, pad_x, pad_y, object_width, object_height):
    object_cars = []

    for ground_rect in grounds:
        pos_x = ground_rect.topleft[0] + pad_x
        pos_y = ground_rect.topleft[1] + pad_y
        object_rect = pygame.Rect(pos_x, pos_y, object_width, object_height)
        object_cars.append(object_rect)

    return object_cars

def car_dicts(vertical_cars,ver_car):
    id = 1
    cars_list = []
    for gari in vertical_cars:
        car_dict = {'id': id, 'image': ver_car,'static_image':ver_car, 'rect': gari, 'prev_theeta': 0, 'theeta': 0, 'next_theeta': 90,
                    'speed':4, 'collided_rect': None}
        cars_list.append(car_dict)
        id += 1
    return cars_list

def new_position(object_x,object_y,player_dict):

    up , down ,left,right = player_dict['movement']
    is_driving = player_dict['is_driving']
    angle = player_dict['angle']

    if is_driving:
        speed = player_dict['car_speed']
        if up:
            object_x -= round(speed * math.cos(math.radians(angle + 90)))
            object_y += round(speed * math.sin(math.radians(angle + 90)))

        if down:
            object_x += round(speed * math.cos(math.radians(angle + 90)))
            object_y -= round(speed * math.sin(math.radians(angle + 90)))
    else:
        speed = player_dict['char_speed']
        if player_dict['is_scrolling']:
            up,down,left,right = player_dict['is_scrolling']
        else:
            up,down,left,right = player_dict['movement']
        if up:
            object_y += round(speed * math.sin(math.radians(angle )))

        if down:
            object_y += round(speed * math.sin(math.radians(angle)))

        if right:
            object_x -= round(speed * math.cos(math.radians(angle)))

        if left:
            object_x -= round(speed * math.cos(math.radians(angle)))


    return object_x,object_y


def display_particles(location, screen):
    # [Location , velocity/direction , radius of circle]

    particles.append([location, [random.randint(0, 30) / 10 - 1, -5], random.randint(2, 10)])
    for particle in particles:
        particle[0][0] -= random.randint(1, 3) * particle[1][0]
        # Adding velocity about x-axis on location of x-axis to move it horizontally

        particle[0][1] += random.randint(1, 4)* 0.01 * particle[1][1]
        # Adding velocity about y-axis on y-axis location to move it.

        particle[2] -= 0.2
        # Particles get smaller over time, the circles get smaller so this will also be the radius of the circle
        # which gets reduced over time.

        pygame.draw.circle(screen, (60, 63, 65), [(int(particle[0][0])), (int(particle[0][1]))], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)

def collision_side(screen,player_dict, obj_dict):
    col_eff = 10
    rect = player_dict['rect']
    is_driving = player_dict['is_driving']
    collider = [obj_dict['houses_1'],obj_dict['houses_2'],obj_dict['lane_vertical'],obj_dict['lane_horizontal']]
    up,down ,left,right = player_dict['movement']
    for objects in collider:
        for obj in objects:
            if not is_driving:
                if rect.colliderect(obj):
                    if abs(rect.top - obj.bottom) < col_eff:  # or abs(rect.top - tile.top) < col_eff:
                        up =  False

                    elif abs(rect.bottom - obj.top) < col_eff:  # or abs(rect.bottom - tile.bottom) < col_eff:
                        down =  False

                    elif abs(rect.left - obj.right) < col_eff:
                        left =  False
                    elif abs(rect.right - obj.left) < col_eff:
                        right = False
                player_dict['movement'] = up,down ,left,right
            else:
                if rect.colliderect(obj):
                    if abs(obj.top - rect.bottom) < 20:
                        rect.bottom = obj.top + 1
                    elif abs(obj.bottom - rect.top) < 20:
                        rect.top = obj.bottom - 1
                    elif abs(obj.right - rect.left) < 20:
                        rect.left = obj.right
                    elif abs(obj.left - rect.right) < 20:
                        rect.right = obj.left

def scroll_objects(screen,player_dict, objects_list):
    up,down,left,right = player_dict['movement']


    angle = player_dict['angle']
    is_driving = player_dict['is_driving']
    char_sprite = player_dict['animation']
    player_rect = player_dict['rect']
    is_scrolling = player_dict['is_scrolling']




    for object_list in objects_list.values():
        for object in object_list:
            if is_scrolling:
                keys = pygame.key.get_pressed()
                up = keys[pygame.K_w]
                down = keys[pygame.K_s]
                left = keys[pygame.K_a]
                right = keys[pygame.K_d]
                player_dict['is_scrolling'] = [up ,down,left,right]


            elif not is_driving and not is_scrolling:
                if player_dict['walk'] + 1 >= player_dict['walk_limit']:
                    player_dict['walk'] = 0
                if up:
                    player_dict['angle'] = 90
                    player_dict['walk'] += 1
                    player_dict['image'], player_dict['rect']= rot_center(char_sprite[player_dict['walk']],player_rect, angle)
                elif down:
                    player_dict['angle'] = 270
                    player_dict['walk'] += 1
                    player_dict['image'], player_dict['rect'] = rot_center(char_sprite[player_dict['walk']], player_rect,angle)
                elif right:
                    player_dict['angle'] = 0
                    player_dict['walk'] += 1
                    player_dict['image'], player_dict['rect'] = rot_center(char_sprite[player_dict['walk']], player_rect,angle)
                elif left:
                    player_dict['angle'] = 180
                    player_dict['walk'] +=1
                    player_dict['image'], player_dict['rect']= rot_center(char_sprite[player_dict['walk']], player_rect,angle)
                else:
                    player_dict['angle']=angle
                    player_dict['walk'] = 0
                    player_dict['image'],player_dict['rect']=rot_center(char_sprite[player_dict['walk']],player_rect,angle)
            else:
                player_dict['image'],player_dict['rect'] = rot_center(player_dict['static_car'], player_dict['rect'], angle)

                if left and (up or down):
                    angle += 0.01
                if right and (up or down):
                    angle -= 0.01
                player_dict['angle'] = angle
            object.x , object.y = new_position(object.x, object.y, player_dict)

def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""

    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)

    return rot_image, rot_rect


def collided_obj(player_dict, obj_dict_list, req_key):
    for obj_dict in obj_dict_list:
        if player_dict['rect'].colliderect(obj_dict[req_key]):
            player_dict['angle'] = obj_dict['theeta']
            obj_dict_list.remove(obj_dict)
            return True
    return False
