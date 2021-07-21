import pygame #hotkeys: p - pause, e - toggle drawing/erasing, n - new empty canvas
import random
import copy
screensize = (1000,600)
sc = pygame.display.set_mode(screensize)
pygame.display.set_caption('Game of life')
clock = pygame.time.Clock()                                    
running = True
canvas_size_x = 200
canvas_size_y = 120
FPS = 60
scale = 5

def fill_2d(xsize,ysize,num):
    arr = []
    for i in range(xsize):
        arr.append([])
        for o in range(ysize):
            if num == 1:
                if i > 0 and i < xsize - 1 and o > 0 and o < ysize - 1:
                    arr[i].append(random.randint(0, 1))
                else:
                    arr[i].append(0)
            else:
                arr[i].append(0)
    return arr

def frame_fill(pixels):
    for i in range(len(pixels)):
        for o in range(len(pixels[0])):
            pygame.draw.rect(sc, (pixels[i][o] * 255, pixels[i][o] * 255, pixels[i][o] * 255), (i * scale, o * scale, scale, scale))
            
def gol(arr):
    rules = ['34','3']
    fin = copy.deepcopy(empty)
    for i in range(1,len(arr) - 1):
        for o in range(1,len(arr[0]) - 1):
            summ = 0
            for x in range(-1, 2):
                for y in range(-1, 2):
                    summ += arr[i + x][o + y]
            if str(summ) in rules[0] and arr[i][o] == 1:
                fin[i][o] = 1
            elif str(summ) in rules[1] and arr[i][o] == 0:
                fin[i][o] = 1
            else:
                fin[i][o] = 0
    return fin

def toggle(boolean):
    if boolean:
        return False
    else:
        return True

mousedown = False
filling_or_erasing = False
paused = False
GOL = fill_2d(canvas_size_x,canvas_size_y, 1)
empty = fill_2d(canvas_size_x,canvas_size_y, 0)
while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = toggle(paused)
                frame_fill(GOL)
            elif event.key == pygame.K_e:
                filling_or_erasing = toggle(filling_or_erasing)
            elif event.key == pygame.K_n:
                GOL = fill_2d(canvas_size_x,canvas_size_y,0)
        elif event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mousedown = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mousedown = False
        if event.type == pygame.MOUSEMOTION:
            position = event.pos
        if mousedown:
            if filling_or_erasing:
                GOL[int(position[0]/scale)][int(position[1]/scale)] = 1
            else:
                for i in range(-1,2):
                    for o in range(-1,2):
                        if int(position[0]/scale) + i > -1 and int(position[0]/scale) + i < screensize[0]/scale and int(position[1]/scale) + o > -1 and int(position[1]/scale) + o < screensize[1]/scale:
                            GOL[int(position[0]/scale) + i][int(position[1]/scale) + o] = 0
    if not paused:
        GOL = gol(GOL)
    frame_fill(GOL)
    pygame.display.update()
    clock.tick(FPS)
    pygame.display.set_caption(f'Game of life - Paused:{paused}')