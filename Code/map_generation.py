
from game_functions import *

#############################  LOADING iMAGES AND GETTING THEIR DIMENSIONS #####################################

# LANE DISTRIBUTOR
footpath = pygame.image.load('Images\\footpath.png')
footpath_width, footpath_height = footpath.get_size()

footpath2 = pygame.image.load('Images\\footpath2.png')
footpath2_width, footpath2_height = footpath2.get_size()

# OTHER CARS
ver_car = pygame.image.load('Images\\lamborghini.png')
ver_car_width, ver_car_height = ver_car.get_size()

#PAINT SHOP
car_paint = pygame.image.load('Images\\car_paint.png')
car_paint_width,car_paint_height = car_paint.get_size()

#CAR RACE TOURNAMENT
car_race = pygame.image.load('Images\\car_race.png')
car_race_width,car_race_height = car_race.get_size()

#F1 RACER
f1_racer = pygame.image.load('Images\\f1_racer.png')
f1_racer_width,f1_racer_height = f1_racer.get_size()

#SPACE SHOOTER
space_shooter = pygame.image.load('Images\\space_shooter.png')
space_shooter_width , space_shooter_height = space_shooter.get_size()

# HOUSE IMAGE
house = pygame.image.load('Images\\house5.png')
house_width, house_height = house.get_size()

house_rot = pygame.image.load('Images\\house5_rotated.png')
house_rot_width, house_rot_height = house.get_size()

# GROUND IMAGE
ground_image = pygame.image.load('Images\\road_ke_saath.png')
ground_width, ground_height = ground_image.get_size()


def colliders_list():
    '''Creates patches of grounds and small rects (colliders) to trigger rotation of traffic'''
    # CREATING GROUND PATCHES AND TRAFFIC COLLIDERS (rects to trigger rotation)

    # Defining position of ground patches
    ground_pos_x = 200
    ground_pos_y = 200
    patch_spacing = 1400
    num_patches = 16
    grounds = []
    colliders = []

    for create in range(num_patches):
        ground_rect = pygame.Rect(ground_pos_x, ground_pos_y, ground_width, ground_height)

        # rect at corners of ground patch to trigger rotation of traffic
        top_l = pygame.Rect(ground_rect.x + 150, ground_rect.y, 5, 190)
        top_r = pygame.Rect(ground_rect.topright[0] - 200, ground_rect.topright[1] + 150, 190, 5)
        bottom_r = pygame.Rect(ground_rect.bottomright[0] - 150, ground_rect.bottomright[1] - 200, 5, 190)
        bottom_l = pygame.Rect(ground_rect.bottomleft[0], ground_rect.bottomleft[1] - 150, 190, 5)

        # rect at corners of footpath to trigger rotation of random characters
        foot_top_l = pygame.Rect(ground_rect.x + 270, ground_rect.y + 200, 5, 70)
        foot_top_r = pygame.Rect(ground_rect.topright[0] - 290, ground_rect.topright[1] + 270, 70, 5)
        foot_bottom_r = pygame.Rect(ground_rect.bottomright[0] - 280, ground_rect.bottomright[1] - 290, 5, 70)
        foot_bottom_l = pygame.Rect(ground_rect.bottomleft[0] + 200, ground_rect.bottomleft[1] - 280, 90, 5)

        # merging all the lists into collider list to store as one list.
        colliders.extend([top_l, foot_top_l, top_r, foot_top_r, bottom_r, foot_bottom_r, bottom_l, foot_bottom_l])

        # appending in grounds list
        grounds.append(ground_rect)

        # changing positions of ground patches
        if ground_pos_x >= 4000:

            ground_pos_x = 200
            ground_pos_y += 900
            continue
        ground_pos_x += patch_spacing
    return grounds, colliders


def create_map(screen):
    '''creates dictionary of objects in map and its images'''

    car_paint_rect = pygame.Rect(6000, 600, car_paint_width,car_paint_height)
    car_race_rect = pygame.Rect(6000,1200,car_race_width,car_race_height)
    f1_racer_rect = pygame.Rect(6000,1800,f1_racer_width,f1_racer_height)
    spaceshooter_rect = pygame.Rect(6000,2400,space_shooter_width , space_shooter_height)

    ################################ INITIALIZING VARIABLES AND CREATING THE MAP ######################################
    grounds, colliders = colliders_list()

    # Dictionary with reference to all lists and their elements (The rects of all objects on map)

    obj_dict = {'grounds': grounds,
                'car': create_cars(grounds, ground_width - 160, 230, ver_car_width, ver_car_height),
                'houses_1': create_objects(grounds, 1, house_width, house_height, 400, 345),
                'houses_2': create_objects(grounds, 1, house_rot_width, house_rot_height, 800, 345),
                'lane_vertical': create_cars(grounds, ground_width - 25, 200, footpath_width, footpath_height),
                'lane_horizontal': create_cars(grounds, 200, ground_height - 25, footpath2_width, footpath2_height),
                'colliders': colliders,
                'paint_shop':[car_paint_rect],
                'tournament':[car_race_rect],
                'mini_game':[f1_racer_rect],
                'space_shooter':[spaceshooter_rect]
                }
    shops = {'paint_shop':[car_paint_rect],
                'tournament':[car_race_rect],
                'mini_game':[f1_racer_rect],
                'space_shooter':[spaceshooter_rect]}
    obj_img_dict = {
                'grounds': ground_image,
                'car': ver_car,
                'houses_1': house,
                'houses_2':house_rot,
                'lane_vertical': footpath,
                'lane_horizontal': footpath2,
                'colliders': None,
                'paint_shop':car_paint,
                'tournament':car_race,
                'mini_game':f1_racer,
                'space_shooter':space_shooter
                }
    return obj_dict, obj_img_dict,shops


def display(screen, all_objects, objects_img):
    '''blits every object of dictionaries on screen forming a map'''

    for key in all_objects.keys():
        if key == 'car':
            continue
        values = all_objects[key]
        for value in values:
            if objects_img[key] is not None:
                screen.blit(objects_img[key], value)
