#Wormy.py

import pygame,sys,random,os
from pygame.locals import *

path=r"d:\python书籍文档\makinggames"
os.chdir(path)

FPS=15
FPS1=30
WINDOWWIDTH=640
WINDOWHEIGHT=480
CELLSIZE=20
assert WINDOWWIDTH%2==0,'Window width must be a multiple of cell size.'
assert WINDOWHEIGHT%2==0,'Window height must be a multiple of cell size.'
CELLWIDTH=int(WINDOWWIDTH/CELLSIZE)#表示x轴能够容纳的CELL的数量
CELLHEIGHT=int(WINDOWHEIGHT/CELLSIZE)#表示y轴能够容纳的CELL的数量
#              R   G   B
WHITE       =(255,255,255)
BLACK       =(  0,  0,  0)
RED         =(255,  0,  0)
GREEN       =(  0,255,  0)
BLUE        =(  0,  0,255)
YELLOW      =(255,255,  0)
DARKGREEN   =(  0,155,  0)
DARKGRAY    =( 40, 40, 40)
BGCOLOR=BLACK

UP='up'
DOWN='down'
LEFT='left'
RIGHT='right'

HEAD=0

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Wormy')
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    showStartScreen()#
    while True:
        musicList = ['beyond不在犹豫.mp3', '求佛.mp3', 'beyond光辉岁月.mp3', 'beyond海阔天空.mp3', '张学友好久不见.mp3']
        pygame.mixer.music.load(musicList[random.randint(0, 4)])
        pygame.mixer.music.play(-1,0.0)
        runGame()#
        pygame.mixer.music.stop()
        showGameOverScreen()#

def runGame():
    startx=random.randint(5,CELLWIDTH-6)
    starty=random.randint(5,CELLHEIGHT-6)
    wormCoords=[{'x':startx,'y':starty},{'x':startx-1,'y':starty},{'x':startx-2,'y':starty}] #设置初始化时的worm数据结构
    direction=RIGHT #设置初始化时worm的移动方向

    apple=getRandomLocation()

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                terminate()
            elif event.type==KEYDOWN:
                if (event.key==K_LEFT or event.key==K_a) and direction!=RIGHT:#当worm向右移动时，发出向左的按键无效
                    direction=LEFT
                elif (event.key==K_RIGHT or event.key==K_d) and direction!=LEFT:
                    direction=RIGHT
                elif (event.key==K_UP or event.key==K_w) and direction!=DOWN:
                    direction=UP
                elif (event.key==K_DOWN or event.key==K_s) and direction!=UP:
                    direction=DOWN
                elif event.key==K_ESCAPE:
                    terminate()
        for i in range(len(wormCoords)): #永远不出界
            if wormCoords[i]['x'] <0:
                wormCoords[i]['x'] += CELLWIDTH
            elif wormCoords[i]['x'] > CELLWIDTH-1:
                wormCoords[i]['x'] -= CELLWIDTH
            elif wormCoords[i]['y'] > CELLHEIGHT-1:
                wormCoords[i]['y'] -= CELLHEIGHT
            elif wormCoords[i]['y'] <0:
                wormCoords[i]['y'] += CELLHEIGHT

        for wormBody in wormCoords[1:]:
            if wormBody['x']==wormCoords[HEAD]['x'] and wormBody['y']==wormCoords[HEAD]['y']: #头和身体其他部委相撞
                return
        if wormCoords[HEAD]['x']==apple['x'] and wormCoords[HEAD]['y']==apple['y']: #如果worm的头和apple相遇
            apple=getRandomLocation()
        else:#如果没有相遇则先删除末尾的worm
            del wormCoords[-1]
        if direction==UP:
            newHead={'x':wormCoords[HEAD]['x'],'y':wormCoords[HEAD]['y']-1}
        if direction==DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        if direction==LEFT:
            newHead = {'x': wormCoords[HEAD]['x']-1, 'y': wormCoords[HEAD]['y']}
        if direction==RIGHT:
            newHead = {'x': wormCoords[HEAD]['x']+1, 'y': wormCoords[HEAD]['y']}
        wormCoords.insert(0,newHead)
        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        drawApple(apple)
        drawScore(len(wormCoords)-3)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def showStartScreen():
    titleFont=pygame.font.Font('freesansbold.ttf',100)
    titleSurf1=titleFont.render('Wormy!',True,WHITE,DARKGREEN)
    titleSurf2 = titleFont.render('Wormy!', True, GREEN)

    degrees1=0
    degrees2=0

    while True:
        DISPLAYSURF.fill(BGCOLOR)

        rotatedSurf1=pygame.transform.rotate(titleSurf1,degrees1)  #做出开始画面，让‘Wormy!’进行旋转
        rotatedRect1=rotatedSurf1.get_rect()
        rotatedRect1.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf1,rotatedRect1)

        rotatedSurf2=pygame.transform.rotate(titleSurf2,degrees2)  #做出开始画面，让‘Wormy!’进行旋转
        rotatedRect2=rotatedSurf2.get_rect()
        rotatedRect2.center=(WINDOWWIDTH/2,WINDOWHEIGHT/2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress(): #用于退出初始屏幕的画面‘Wormy!’的旋转
            pygame.event.get()
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS1)
        degrees1+=3
        degrees2+=7
def showGameOverScreen():
    gameOverFont=pygame.font.Font('freesansbold.ttf',150)
    gameSurf=gameOverFont.render('Game',True,WHITE)
    gameRect=gameSurf.get_rect()
    gameRect.midtop=(WINDOWWIDTH/2,10)
    overSurf=gameOverFont.render('Over',True,WHITE)
    overRect=overSurf.get_rect()
    overRect.midtop=(WINDOWWIDTH/2,gameRect.height+10+25)

    DISPLAYSURF.blit(gameSurf,gameRect)
    DISPLAYSURF.blit(overSurf,overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress()

    while True:
        if checkForKeyPress():
            pygame.event.get()
            return

def checkForKeyPress():
    if len(pygame.event.get(QUIT))>0:
        terminate()
    keyUpEvents=pygame.event.get(KEYUP)
    if len(keyUpEvents)==0:
        return None
    if keyUpEvents[0].key==K_ESCAPE:
        terminate()
    return keyUpEvents[0].key
def drawPressKeyMsg(): #显示右下角的按键提示
    pressKeySurf=BASICFONT.render('Press a key to play.',True,DARKGREEN)
    pressKeyRect=pressKeySurf.get_rect()
    pressKeyRect.topleft=(WINDOWWIDTH-200,WINDOWHEIGHT-30)
    DISPLAYSURF.blit(pressKeySurf,pressKeyRect)
def getRandomLocation():
    return {'x':random.randint(0,CELLWIDTH-1),'y':random.randint(0,CELLHEIGHT-1)}

def terminate():
    pygame.quit()
    sys.exit()

def drawGrid():
    for x in range(0,WINDOWWIDTH,CELLSIZE):
        pygame.draw.line(DISPLAYSURF,DARKGREEN,(x,0),(x,WINDOWHEIGHT))
    for y in range(0,WINDOWHEIGHT,CELLSIZE):
        pygame.draw.line(DISPLAYSURF, DARKGREEN, (0, y), (WINDOWWIDTH,y))
def drawApple(coord):
    x=coord['x']*CELLSIZE
    y=coord['y']*CELLSIZE
    appleRect=pygame.Rect(x,y,CELLSIZE,CELLSIZE)
    pygame.draw.rect(DISPLAYSURF,RED,appleRect)
def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, YELLOW, wormSegmentRect)
        wormInnerSegmentRect=pygame.Rect(x+4,y+4,CELLSIZE-8,CELLSIZE-8)
        pygame.draw.rect(DISPLAYSURF, GREEN, wormInnerSegmentRect)
def drawScore(score):
    scoreSurf=BASICFONT.render('Score: %s'%(score),True,WHITE)
    scoreRect=scoreSurf.get_rect()
    scoreRect.topleft=(WINDOWWIDTH-120,10)
    DISPLAYSURF.blit(scoreSurf,scoreRect)


if __name__=='__main__':
    main()