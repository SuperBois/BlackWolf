import pygame
def initialize_player():
    player_dict = {}
    # SPRITE SHEET OF CHARACTER 1
    walk_limit = 0
    char_movement = []

    # lOADING THE IMAGES OF ANIMATION IN RESPECTIVE LISTS
    for run in range(1, 7):
        char_movement.append(pygame.image.load(f'Images\\right\\right{run}.png'))
        walk_limit += 1
    static = pygame.image.load('Images\\right\\right1.png')

    player_rect = static.get_rect()
    player_rect.center = 400, 300

    up, down, left, right = False, False, False, False
    player_dict = {
        'image': static,
        'rect': player_rect,
        'angle': 0,
        'animation': char_movement,
        'is_scrolling':False,
        'is_driving': False,
        'image_path': 'Images\\lamborghini.png',
        'car': pygame.image.load('Images\\lamborghini.png'),
        'scrolling':[up,down,left,right],
        'movement': [up, down, left, right],
        'static_car': pygame.image.load('Images\\lamborghini.png'),
        'char_speed': 6,
        'car_speed':13,
        'walk': 0,
        'walk_limit': walk_limit,
        'purchased': 'yellow'
    }
    return player_dict


def display_player(screen, player_dict):
    screen.blit(player_dict['image'], player_dict['rect'])
