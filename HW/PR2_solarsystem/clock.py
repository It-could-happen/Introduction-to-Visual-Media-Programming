import numpy as np
import pygame
import time
from time import localtime
from time import time
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CENTER_X = WINDOW_WIDTH/2
CENTER_Y = WINDOW_HEIGHT/2

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (20, 20, 20)
Biba_magenta = (187, 38, 73)

#시침, 분침, 초침의 길이와 두께 
HOURHAND_LENGTH = 100
HOURHAND_THICKNESS = 20
MINUTEHAND_LENGTH = 150
MINUTEHAND_THICKNESS = 18
SECONDHAND_LENGTH = 200
SECONDHAND_THICKNESS = 10

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

def makeRect(width, height):
    newbox = np.array( [[0, 0, 1], [width, 0, 1], [width, height, 1], [0, height, 1]])
    return newbox


def main():
    # Pygame 초기화
    pygame.init()

    # 윈도우 제목 
    pygame.display.set_caption("Clock by 20171166")

    # 윈도우 생성
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # 게임 화면 업데이트 속도
    clock = pygame.time.Clock()

    #이미지 경로 설정
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets') 

    # 게임 종료 전까지 반복
    done = False    # 게임이 진행중인지 확인하는 변수

    # done이 True라면 게임이 계속 진행중이라는 의미

    #시계 바늘 파츠 값 정의

    hourHandBox = makeRect(HOURHAND_LENGTH, HOURHAND_THICKNESS)
    minuteHandBox = makeRect(MINUTEHAND_LENGTH, MINUTEHAND_THICKNESS)
    secondHandBox = makeRect(SECONDHAND_LENGTH, SECONDHAND_THICKNESS)

    #이미지 로드
    clockimage = pygame.image.load(os.path.join(assets_path, 'clock.png'))

    # 게임 반복 구간
    while not done: # 게임이 진행되는 동안 계속 반복 작업을 하는 while 루프
        # 이벤트 반복 구간
        for event in pygame.event.get():
            # 어떤 이벤트가 발생했는지 확인
            if event.type == pygame.QUIT:
                done = True # 반복을 중단시켜 게임 종료
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    done = True
            
        # 게임 로직 구간
        timestamp = time()
        mytime = localtime(timestamp)
        curHour = mytime.tm_hour
        curMinute = mytime.tm_min
        curSecond = mytime.tm_sec

        minDegree = curMinute * 6 - 90
        secDegree = curSecond * 6 - 90
        hourDegree = (curHour%12) * 30 + minDegree/12 - 90


        hourH = Tmat(CENTER_X, CENTER_Y) @ Rmat(hourDegree) @ Tmat(-HOURHAND_THICKNESS/2, -HOURHAND_THICKNESS/2)
        minuteH = Tmat(CENTER_X, CENTER_Y) @ Rmat(minDegree) @ Tmat(-HOURHAND_THICKNESS/2, -MINUTEHAND_THICKNESS/2)
        secondH = Tmat(CENTER_X, CENTER_Y) @ Rmat(secDegree) @ Tmat(-HOURHAND_THICKNESS/2, -SECONDHAND_THICKNESS/2)

        hourHand = remove3thDim(hourH @ hourHandBox.T)
        minuteHand = remove3thDim(minuteH @ minuteHandBox.T)
        secondHand = remove3thDim(secondH @ secondHandBox.T)
        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)

        # 화면 그리기 구간
        screen.blit(clockimage, (CENTER_X-(clockimage.get_width()/2),CENTER_Y-(clockimage.get_height()/2)))
        pygame.draw.polygon(screen, GREEN, secondHand)        
        pygame.draw.polygon(screen, BLUE, minuteHand)
        pygame.draw.polygon(screen, RED, hourHand)


        pygame.draw.circle(screen, BLACK, (CENTER_X, CENTER_Y), 10)


        # 화면 업데이트
        pygame.display.flip()

        # 초당 60 프레임으로 업데이트
        clock.tick(60) 

    # 게임 종료


if __name__ == "__main__":
    main()
    pygame.quit()
