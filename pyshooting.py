import pygame
import sys
import random
from time import sleep

padWidth = 480
padHeight = 600
rockImage = ["rock01.png","rock02.png","rock03.png","rock04.png","rock05.png",
             "rock06.png","rock07.png","rock08.png","rock09.png","rock10.png",
             "rock11.png","rock01.png","rock01.png","rock01.png","rock15.png",
             "rock16.png","rock17.png","rock18.png","rock19.png","rock20.png",
             "rock21.png","rock22.png","rock23.png","rock24.png","rock25.png",
             "rock26.png","rock27.png","rock28.png","rock29.png","rock30.png"]

explosionSound = ['explosion.wav']
             

# 게임에 등장하는 객체를 드로잉

def writeScore(count):
    global gamePad
    font = pygame.font.Font("NanumGothic.ttf",20)
    text = font.render("파괴한 운석 수:" + str(count), True, (255, 255, 255))
    gamePad.blit(text, (10,0))

def writePassed(count):
    global gamePad
    font = pygame.font.Font("NanumGothic.ttf",20)
    text = font.render("놓친  운석 수:" + str(count), True, (255, 0, 0))
    gamePad.blit(text, (350,0))


def writeMessage(text):
    global gamePad, gameOverSound
    textfont = pygame.font.Font("NanumGothic.ttf",60)
    text = textfont.render(text, True, (255, 0, 0))
    textpos = text.get_rect()
    textpos.center = (padWidth/2, padHeight/2)
    gamePad.blit(text, textpos)
    pygame.display.update()
    pygame.mixer.music.stop()
    gameOverSound.paly()
    sleep(2)
    pygame.mixer.music.play(-1)
    runGame()

def crash():
    global gamePad
    writeMessage("전투기  파괴!")

def gameOver():
    global gamePad
    writeMessage("GAME OVER")


def drawObject(obj, x, y):
    global gamePad
    gamePad.blit(obj, (x, y)) 



def initGame():
    global gamePad, clock, backgroud, fighter, missile, explosion, missileSound
    pygame.init()
    gamePad = pygame.display.set_mode((padWidth, padHeight))
    pygame.display.set_caption("pyshooting")            #게임 이름
    backgroud = pygame.image.load("game_screen.png")  #배경 이름
    fighter = pygame.image.load("spaceship.png")
    missile = pygame.image.load("missile3.png")
    explosion = pygame.image.load("warp.png")
    pygame.mixer.music.load("Inner_Sanctum.mp3")
    pygame.mixer.music.play(-1)
    missileSound = pygame.mixer.Sound()
    gameOverSound = pygame.mixer.Sound()
    clock = pygame.time.Clock()

def runGame():
    global gamePad, clock, backgroud,fighter, missile, explosion

    fighterSize = fighter.get_rect().size
    fighterWidth = fighterSize[0]
    fighterHeight = fighterSize[1]

    x = padWidth * 0.45
    y = padHeight * 0.9
    fighterX = 0

    missileXY = []

    #새로운 운석 (랜덤)
    rock = pygame.image.load(random.choice(rockImage))
    rockSize = rock.get_rect().size
    rockWidth = rockSize[0]
    rockHeight = rockSize[1]
    destorySound = pygame.mixer.Sound(random.choice(explosionSound))
    

    rockX = random.randrange(0, padWidth - rockWidth)
    rockY = 0
    rockSpeed = 2

    isShot = False
    shotCount = 0
    rockPassed = 0

    onGame = False
    while not onGame:
        for event in pygame.event.get():
            if event.type in [pygame.QUIT]:    #게임 프로그램 종료
                pygame.quit()
                sys.exit()
                
            if event.type in[pygame.KEYDOWN]:
                if event.key == pygame.K_LEFT: # 전투기 왼쪽으로 이동
                    fighterX -= 5

                elif event.key == pygame.K_RIGHT: #전투기 오른쪽으로 이동
                    fighterX += 5

                elif event.key == pygame.K_SPACE: #미사일 발사
                    missileSound.play()
                    missileX = x + fighterWidth/2
                    missileY = y - fighterHeight
                    missileXY.append([missileX, missileY])
                  
            if event.type in [pygame.KEYUP]:   #방향기를 때면 전투기 멈춤
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    fighterX = 0

        drawObject(backgroud , 0, 0)


        #전투기 위치 재조정
        x += fighterX
        if x < 0:
            x = 0
        elif x > padWidth - fighterWidth:
            x = padWidth - fighterWidth


        #전투기가 운석과 충돌했는지 체크
        if y < rockY + rockHeight:
            if (rockX > x and rockX < x + fighterWidth) or \
                    (rockX + rockWidth > x and rockWidth < x +fighterWidth): 

                 crash()

        drawObject(fighter, x, y) 

        if len(missileXY) != 0:
            for i,bxy in enumerate(missileXY):
                bxy[1] -= 10
                missileXY[i][1] = bxy[1]

                if bxy[1] < rockY:
                    if bxy[0] > rockX and bxy[0] < rockX + rockWidth:
                        missileXY.remove(bxy)
                        isShot = True
                        shotCount += 1


                if bxy[1] <= 0:
                    try:
                        missileXY.remove(bxy)
                    except:
                        pass


        if len(missileXY) != 0:
            for bx, by in missileXY:
                drawObject(missile, bx, by)


        writeScore(shotCount)

        rockY += rockSpeed

        if rockY > padHeight:
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
    
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            rockPassed += 1

        if rockPassed == 3: #운석 3개를 놓치면 게임 오버
            gameOver()

        #놓친 운석 수 표시
        writePassed(rockPassed)

        #운석을 맞춘 경우
        if isShot:
            #운석 폭발
            drawObject(explosion, rockX, rockY) # 운석 폭발
            destorySound.play()

            #새로운 운석 (랜덤)
            rock = pygame.image.load(random.choice(rockImage))
            rockSize = rock.get_rect().size
            rockWidth = rockSize[0]
            rockHeight = rockSize[1]
    
            rockX = random.randrange(0, padWidth - rockWidth)
            rockY = 0
            destorySound = pygame.mixer.Sound(random.choice(explosionSound))
            isShot = False

            rockSpeed += 0.2
            if rockSpeed >= 10:
                rockSpeed = 10

            

        drawObject(rock, rockX, rockY)

        pygame.display.update()

        clock.tick(60)

    pygame.quit()


initGame()
runGame()

    
