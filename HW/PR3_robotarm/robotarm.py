import numpy as np
import pygame
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (20, 20, 20)
Biba_magenta = (187, 38, 73)

# 사용 함수 정의

#이동 행렬 생성함수
def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H

#회전 행렬 생성 함수
def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array([[c,-s, 0], [s, c, 0], [0, 0, 1]])
    return R

#3차원 요소 제거 함수
def remove3thDim(pp):
    q = pp[0:2, :].T
    return q

class robotArm:
    pass

# poly: 4 x 3 matrix
poly = np.array( [[0, 0, 1], [100, 0, 1], [100, 20, 1], [0, 20, 1]])
poly = poly.T # 3x4 matrix 


def makeRect(width, height):
    newbox = np.array( [[0, 0, 1], [width, 0, 1], [width, height, 1], [0, height, 1]])
    return newbox

cor = np.array([10, 10, 1])


def main():
    # Pygame 초기화
    pygame.init()

    # 윈도우 제목 
    pygame.display.set_caption("robot arm by 20171166")

    # 윈도우 생성
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # 게임 화면 업데이트 속도
    clock = pygame.time.Clock()

    #이미지 경로 설정
    current_path = os.path.dirname(__file__)

    # 게임 종료 전까지 반복
    done = False    # 게임이 진행중인지 확인하는 변수
    font = pygame.font.SysFont('FixedSys', 24, True, False)

    # done이 True라면 게임이 계속 진행중이라는 의미
    degree1 = -90
    degree2 = 30
    degree3 = 40
    degree4 = degree3

    #로봇팔 파츠 값 정의
    base = makeRect(100, 100)
    baseH = Tmat(WINDOW_WIDTH/2-100, WINDOW_HEIGHT-200)
    basePart = remove3thDim(baseH @ base.T)

    firstArmLength = 120
    secondArmLength = 100
    thirdArmLength = 100

    firstArmbox = makeRect(firstArmLength, 20)
    secondArmbox = makeRect(secondArmLength, 20)
    thirdArmbox = makeRect(thirdArmLength, 20)

    #robotHand = np.array([[0,0,1], [0,25,1 ], [40,10,1], [35,8,1], [20,5,1], [0,5,1]])

    robotHandImage = pygame.image.load(os.path.join(current_path, 'robotHand.png'))
    robotHandImage = pygame.transform.scale(robotHandImage, (80, 40))
    robotHand = np.array([0,0,1])

    text1 = font.render("Press the direction key to rotate the first and second joints.", True, BLACK)
    text2 = font.render("Press 'z','x' key is third joint rotate", True, BLACK)
    text3 = font.render("Press 'a','s' key is extand hand", True, BLACK)
    text4 = font.render("Press 'q','w' key is rotate hand", True, BLACK)
    
    # 게임 반복 구간
    while not done: # 게임이 진행되는 동안 계속 반복 작업을 하는 while 루프
        # 이벤트 반복 구간
        for event in pygame.event.get():
            # 어떤 이벤트가 발생했는지 확인
            if event.type == pygame.QUIT:
                done = True # 반복을 중단시켜 게임 종료
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            degree1 += -1
        if keys[pygame.K_RIGHT]:
            degree1 += +1
        if keys[pygame.K_UP]:
            degree2 += -1
        if keys[pygame.K_DOWN]:
            degree2 += +1
        if keys[pygame.K_z]:
            degree3 += 1
        if keys[pygame.K_x]:
            degree3 += -1
        if keys[pygame.K_a]:
            thirdArmLength += 1
        if keys[pygame.K_s]:
            thirdArmLength += -1
        if keys[pygame.K_q]:
            degree4 += -1
        if keys[pygame.K_w]:
            degree4 += 1
            
        if degree1 > -10:
            degree1 = -10
        elif degree1 < -170:
            degree1 = -170
        # 게임 로직 구간

        firstH = baseH @ Tmat(50, 0) @ Rmat(degree1) @ Tmat(-10, -10) 
        secondH = firstH @ Tmat(firstArmLength, 0) @ Tmat(-10, 10) @ Rmat(degree2) @ Tmat(-10, -10)
        thirdH = secondH @ Tmat(secondArmLength, 0) @ Tmat(-10, 10) @ Rmat(degree3) @ Tmat(-10, -10)
        robotHandH = thirdH @ Tmat(thirdArmLength+10, 0 ) 

        firstPart = remove3thDim(firstH @ firstArmbox.T)
        secondPart = remove3thDim(secondH @ secondArmbox.T)
        thirdPart = remove3thDim(thirdH @ thirdArmbox.T)
        rotatedImage = pygame.transform.rotate(robotHandImage, degree4)
        robotHandPart =  (robotHandH @ robotHand.T)[0:2 :].T 

        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)

        # 화면 그리기 구간
        pygame.draw.polygon(screen, GRAY, basePart,  5)
        pygame.draw.polygon(screen, GRAY, firstPart,  5)
        pygame.draw.polygon(screen, GRAY, secondPart,  5)
        pygame.draw.polygon(screen, GRAY, thirdPart,  5)
        screen.blit(rotatedImage, (robotHandPart[0] + robotHandImage.get_width() / 2 - rotatedImage.get_width() / 2, robotHandPart[1] + robotHandImage.get_height() / 2 - rotatedImage.get_height() / 2)      )


        screen.blit(text1, (50,50))
        screen.blit(text2, (50,70))
        screen.blit(text3, (50,90))
        screen.blit(text4, (50,110))


        # 화면 업데이트
        pygame.display.flip()

        # 초당 60 프레임으로 업데이트
        clock.tick(60) 

    # 게임 종료


if __name__ == "__main__":
    main()
    pygame.quit()
