import pygame, sys, random

particles = []

def explode(screen, location, colour,size, ended):
    global particles
    x_pos, y_pos = location
    if not ended:
        for i in range(50):
            # Location, ,size
            particles.append([[x_pos, y_pos], [random.randint(0, 42) / 6 - 3.5, random.randint(0, 42) / 6 - 3.5], random.randint(size -2, size + 5)])
            #Adjust radius of circle in last element of list.

    for particle in particles:
        particle[0][0] += particle[1][0]
        # Adding velocity about x-axis on location of x-axis to move it horizontally
        particle[0][1] += particle[1][1]
        # Adding velocity about y-axis on y-axis location to move it.
        particle[2] -= 0.2
        # Particles get smaller over time, the circles get smaller so this will also be the radius of the circle
        # which gets reduced over time.
        pygame.draw.circle(screen, colour, [(int(particle[0][0])), (int(particle[0][1]))], int(particle[2]))
        if particle[2] <= 0:
            particles.remove(particle)
    if particles == []:
        return True
    else:
        return False


