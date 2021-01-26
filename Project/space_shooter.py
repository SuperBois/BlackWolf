from explosions import *
import time

# background image
bg = pygame.image.load('Images\\bg.jpg')

# initializing the player
player = pygame.image.load('Images\\spaceship.png')
player_rect = player.get_rect()
player_rect.center = (400, 500)

# loading asteriods
asteriod = pygame.image.load('Images\\asteroid.png')
asteriod_rect = asteriod.get_rect()
asteriod_rect.x = random.randint(310,460)
asteriod_rect.y = 50

# loading bullets
bullet = pygame.image.load('Images\\bullet.png')
bullet_rect = bullet.get_rect()
fire = False
ended = False

# font
font = pygame.font.SysFont("Comic Sans MS", 30)
coins_text = font.render('Coins: ', True, (250,250,250))

def space_shooter(screen, coins,state, username):
    global player_rect, fire, ended
    screen.blit(bg, (0, 0))
    keys = pygame.key.get_pressed()
    if not ended:
        state = 'space_shooter'
        # gets all pressed keys

        if keys[pygame.K_LEFT] and 300 < player_rect.x:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT] and player_rect.x < 500:
            player_rect.x += 5
        if keys[pygame.K_SPACE] and not fire:
            fire = True
            bullet_rect.x = player_rect.x
            bullet_rect.y = player_rect.y

        # if asteriod gets out of the screen
        if asteriod_rect.y > 600:
            asteriod_rect.x = random.randint(300, 500)
            asteriod_rect.y = -50

        if fire:
            if bullet_rect.y > 0:
                bullet_rect.y -= 10
                screen.blit(bullet, bullet_rect)
            else:
                bullet_rect.y = player_rect.y + 50
                fire = False

        # starting position of asteriod
        asteriod_rect.y += 10

        screen.blit(asteriod, asteriod_rect)
        screen.blit(player, player_rect)

        if player_rect.colliderect(asteriod_rect):
            explode(screen, [player_rect.centerx, player_rect.centery], (255, 201, 14), 10,ended)
            ended = True

        if asteriod_rect.colliderect(bullet_rect):
            asteriod_rect.y = -50
            asteriod_rect.x = random.randint(300, 500)
            fire = False
            bullet_rect.y = player_rect.y + 50
            coins += 10
        # Displaying the coins on screen
        coins_surface = font.render(str(coins), True, (200, 200, 200))
        screen.blit(coins_text, (20, 20))
        screen.blit(coins_surface, (100, 20))
        return coins, state
    else:
        # explosive effect
        end_screen = explode(screen, [player_rect.centerx, player_rect.centery], (255, 201, 14), 10, ended)
        state = 'space_shooter'
        if end_screen:
            state = game_over(screen, username, coins)
            
        return coins, state

def game_over(screen,username, coins):
    game_over = pygame.image.load('Images\\gameover.png')
    screen.blit(game_over, game_over.get_rect())
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        with open(f"profiles\\profile_{username}.txt", "w") as file:
            user_profile = {'username': username, 'coins': coins}
            file.writelines(f'{user_profile}')
        return 'main_game'
    else:
        return 'space_shooter'
