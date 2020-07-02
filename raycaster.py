import array
import pygame
import math
from tkinter import *

# tutorial from https://lodev.org/cgtutor/raycasting.html

# constants
mapWidth = 24
mapHeight = 24
screenWidth = 900 #640
screenHeight = 600  #480

# world map
worldMap = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 3, 0, 0, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 0, 0, 3, 0, 3, 0, 3, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 5, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# initialize pygame
pygame.init()

# initialize font
pygame.font.init()

# create the screen
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Python Raycaster")

# create game clock
clock = pygame.time.Clock()

def switch(number: int):
    """acts like a switch statement. switches the ints of the map with a color value to display.

    Args:

        number: the number to switch on
    """
    switcher = {
        1: (255, 0, 0),  # red
        2: (0, 255, 0),  # green
        3: (0, 0, 255),  # blue
        4: (255, 255, 255)  # white
    }
    return switcher.get(number, pygame.Color("#ffff00"))  # default is yellow

def stop():
    pygame.quit()
    quit()


        
def display_text(text: str, position: tuple, color: tuple):
    """displays text to the screen at the given position.

    Args:

        text: the text to display.
        position: the position to display the text.
        color: the color of the text.

    """
    fpsFont = pygame.font.SysFont('Consolas',15)
    screen.blit(fpsFont.render(text, False, color), position)

def display_text_centered(text: str, position: tuple, color: tuple, size: int, font: str): 
    """displays text to the screen with the given parameters

    Args:

        text: the text to display
        position: the position to display the text.
        color: the color of the text.
        size: the font size
        font: the system font to use
    """
    font_obj = pygame.font.SysFont(font, size)
    rendered = font_obj.render(text, False, color)
    rect = rendered.get_rect().width
    screen.blit(rendered, (position[0] - rect // 2,position[1]))
    return rendered
        
def get_text_object(text: str, color: tuple, fontSize: int, font: str):
    font_obj = pygame.font.SysFont(font, fontSize)
    return font_obj.render(text, False, color)

def game_intro():
    intro = True
    while intro:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting...")
                intro = False
                stop()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:

                    intro = False
                    
        display_text_centered(text="Python raycaster", position=(screenWidth // 2, 100), color=(200, 200, 200), size=30, font='Consolas')
        display_text_centered(text="Press 'SPACE' to start", position=(screenWidth // 2, 200), color=(200, 40, 40), size=20, font='Consolas')
        display_text_centered(text="WASD to move, left and right arrow keys to look", position=(screenWidth//2, 250), color=(50, 100, 100), size=16, font='Consolas')

        copy_right_text = get_text_object(text="made by Sem van der Hoeven", color=(100, 100, 100), fontSize=12, font='Consolas')
        rect = copy_right_text.get_rect()
        screen.blit(copy_right_text, (0, screenHeight - rect.height))
        
        
        pygame.display.update()
        clock.tick(30)

def game_loop(clock, screen):
    """main game loop that runs the game.

    Args:

        clock: The pygame clock object.
        screen: the pygame screen object.
    """

    posX = 22.0  # x start position
    posY = 12.0  # y start position
    dirX = -1.0  # initial x of direction vector
    dirY = 0.0  # initial y of direction vector

    planeX = 0.0  # 2d raycaster version of camera plane x
    planeY = 0.66  # 2d raycaster version of camera plane y

    running = True
    rotateLeft = False
    rotateRight = False
    moveForward = False
    moveBackward = False
    moveLeft = False
    moveRight = False
    debugMode = False
    
    # main game loop
    print("starting game...")
    while running:

        # update the next frame at 30 fps
        ms = clock.tick(60) / 1000.0

        moveSpeed = ms * 3.0
        rotSpeed = ms * 3.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("exiting...")
                del screen
                del clock
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('a'):
                    moveLeft = True
                if event.key == ord('d'):
                    moveRight = True
                if event.key == ord('w'):
                    moveForward = True
                if event.key == ord('s'):
                    moveBackward = True
                if event.key == pygame.K_LEFT:
                    rotateLeft = True
                if event.key == pygame.K_RIGHT:
                    rotateRight = True
                if event.key == pygame.K_TAB:
                    debugMode = not debugMode
                    print("setting debug mode to" ,debugMode)
            if event.type == pygame.KEYUP:
                if event.key == ord('a'):
                    moveLeft = False
                if event.key == ord('d'):
                    moveRight = False
                if event.key == ord('w'):
                    moveForward = False
                if event.key == ord('s'):
                    moveBackward = False
                if event.key == pygame.K_LEFT:
                    rotateLeft = False
                if event.key == pygame.K_RIGHT:
                    rotateRight = False
        if running == False:
            continue  # if the user has pressed the quit key, stop the loop

        # loop that goes over every x (vertical line)
        screen.fill((0, 0, 0))
        for x in range(screenWidth):

            # calculate camera x, the x coordinate on the camera plane that the current
            # x-coordinate represents.
            # This way, the right side of the screen will get coordinate 1, center will get coordinate 0,
            # and left will get coordinate -1
            cameraX = 2 * x / float(screenWidth) - 1
            rayDirX = dirX + planeX * cameraX
            rayDirY = dirY + planeY * cameraX

            # which box of the map we're in
            mapX = int(posX)
            mapY = int(posY)

            # length of the ray from current position to next x or y side
            sideDistX = 0.0  # (double)
            sideDistY = 0.0  # (double)

            # length of ray from one x or y-side to next x or y-side

            # rayDirX and rayDirY can be 0, so then division by 0 would occur if
            # we did only abs(1/rayDirX), so we need to check if it is 0
            deltaDistX = 0 if rayDirY == 0 else (
                1 if rayDirX == 0 else abs(1/rayDirX))
            deltaDistY = 0 if rayDirX == 0 else (
                1 if rayDirY == 0 else abs(1/rayDirY))

            perpWallDist = 0.0  # used to calculate the length of the ray (double)

            # what direction to step in x or y-direction (either +1 or -1 for positive or negative direction)
            # if the ray direction has a negative x-component, stepX will be -1. If it has a positive x-component,
            # it will be +1. If the x-component is 0 the value of stepX won't matter because it won't be used.
            # same for stepY
            stepX = 0  # (int)
            stepY = 0  # (int)

            hit = 0  # was there a wall hit?
            side = 0  # (int) was a vertical or horizontal wall hit?

            # calculate step and initial sideDist
            # is the x-component of the ray is negative, sideDistX is the distance to the first vertical line to the left.
            if rayDirX < 0:
                # if the x-component of the ray is positive, sideDistX is the distance to the first vertical line to the richt.
                # same for the y-component, but then to the first horizontal line to the top or bottom
                stepX = -1
                sideDistX = (posX - mapX) * deltaDistX
            else:
                stepX = 1
                sideDistX = (mapX + 1.0 - posX) * deltaDistX

            if rayDirY < 0:
                stepY = -1
                sideDistY = (posY - mapY) * deltaDistY
            else:
                stepY = 1
                sideDistY = (mapY + 1.0 - posY) * deltaDistY

            # actual DDA algorithm

            while hit == 0:  # while the ray has not hit a wall
                # jump to the next map square, OR in x direction OR in y direction
                if (sideDistX < sideDistY):  # the ray is going morea horizontal than vertical
                    sideDistX += deltaDistX
                    mapX += stepX
                    side = 0
                else:
                    sideDistY += deltaDistY
                    mapY += stepY
                    side = 1
                # check if the ray has hit a wall
                # if it is not 0, so the square does not contain a walkable square, so a wall
                if worldMap[mapX][mapY] > 0:
                    hit = 1

            # calculate the distance projected on camera direction (Euclidean distance will give fisheye effect!)
            if side == 0:  # vertical wall hit
                perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
            else:  # horizontal wall hit
                perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

            # calculate the height of the line to draw on the screen
            if (perpWallDist != 0):
                lineHeight = int(screenHeight / perpWallDist)

            # calculate the lowest and highest pixel to fill in current vertical stripe
            drawStart = -lineHeight / 2 + screenHeight / 2
            if drawStart < 0:
                drawStart = 0
            drawEnd = lineHeight / 2 + screenHeight / 2
            if drawEnd >= screenHeight:
                drawEnd = screenHeight - 1

            color = switch(worldMap[mapX][mapY])

            if side == 1:
                color = (color[0] / 2, color[1] / 2, color[2] / 2)

            pygame.draw.line(screen, color, (x, int(drawStart)),
                            (x, int(drawEnd)), 1)

        if moveForward:
            movePosX = int(posX + dirX * moveSpeed)  # x position to move to next
            movePosY = int(posY + dirY * moveSpeed)  # y position to move to next

            if worldMap[movePosX][movePosY] == 0:
                posX += dirX * moveSpeed
                posY += dirY * moveSpeed

        if moveBackward:
            movePosX = int(posX - dirX * moveSpeed)
            movePosY = int(posY - dirY * moveSpeed)

            if worldMap[movePosX][movePosY] == 0:
                posX -= dirX * moveSpeed
                posY -= dirY * moveSpeed

        if moveLeft:
            oldDirX = dirX
            oldDirY = dirY
            dirX = dirX * math.cos(math.pi/2) - dirY * math.sin(math.pi/2)
            dirY = oldDirX * math.sin(math.pi/2) + dirY * math.cos(math.pi/2)

            movePosX = int(posX + dirX * moveSpeed)  # x position to move to next
            movePosY = int(posY + dirY * moveSpeed)  # y position to move to next
            if worldMap[movePosX][movePosY] == 0:
                posX += dirX * moveSpeed
                posY += dirY * moveSpeed
            dirX = oldDirX
            dirY = oldDirY

        if moveRight:
            oldDirX = dirX
            oldDirY = dirY
            dirX = dirX * math.cos(-math.pi/2) - dirY * math.sin(-math.pi/2) # rotate 90 degrees to the right
            dirY = oldDirX * math.sin(-math.pi/2) + dirY * math.cos(-math.pi/2) # so change the direction to 90 degrees

            # apply the move, so move to the right
            movePosX = int(posX + dirX * moveSpeed)  # x position to move to next
            movePosY = int(posY + dirY * moveSpeed)  # y position to move to next
            if worldMap[movePosX][movePosY] == 0:
                posX += dirX * moveSpeed
                posY += dirY * moveSpeed
            # reset the direction vector because we still want to look forward
            dirX = oldDirX
            dirY = oldDirY

        if rotateRight:
            oldDirX = dirX
            dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
            dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
            planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)

        if rotateLeft:
            oldDirX = dirX
            dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
            dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
            oldPlaneX = planeX
            planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
            planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)


        textToRender = "FPS: " + str(int(1 // ms))
        if debugMode: textToRender = textToRender + " posX: " + str(int(
            posX)) + " posY: " + str(int(
            posY)) + " dirX: " + str(dirX) + " dirY: " + str(dirY)

        display_text(textToRender, (0, 0), (0, 255, 255))
        copy_right_text = get_text_object(text="press TAB for debug info", color=(100, 100, 100), fontSize=12, font='Consolas')
        rect = copy_right_text.get_rect()
        screen.blit(copy_right_text, (0, screenHeight - rect.height))

        # uodate the display
        pygame.display.update()

game_intro()
game_loop(clock,screen)
stop()
