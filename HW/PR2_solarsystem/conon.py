# -*- coding: utf-8 -*- 

import pygame
import numpy as np 

poly = np.array([[0,0], [100, 0], [100, 20], [0, 20]])
cor = np.array([100, 200])

def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    return np.array([[c,-s, 0], [s, c, 0], [0, 0, 1]])

def Tmat(x, y):
    H = np.eye(3)
    return np.array([[x, 0, 0], [0, y, 0], [0, 0, 1]])


# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PINK = (255, 200, 180)

def main():
    # Pygame 초기화
    pygame.init()
    info = pygame.display.Info()
    SIZE = WIDTH, HEIGHT = info.current_w, info.current_h
    print(WIDTH, HEIGHT)

    # 윈도우 제목
    pygame.display.set_caption("Drawing")

    # 윈도우 생성
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # 게임 화면 업데이트 속도
    clock = pygame.time.Clock()

    # 게임 종료 전까지 반복
    done = False
    # 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
    font = pygame.font.SysFont('FixedSys', 40, True, False)

    degree = 10

    # 게임 반복 구간
    while not done:
        # 이벤트 반복 구간
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # 게임 로직 구간

        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)


        # 다각형 그리기
        degree +=1
        pygame.draw.polygon(screen, GREEN, poly, 4)
        


        # 안티얼리어스를 적용하고 검은색 문자열 렌더링
        text = font.render("Hello Pygame", True, BLACK)
        screen.blit(text, [200, 600])

        # 화면 업데이트
        pygame.display.flip()

        clock.tick(20)

    # 게임 종료

if __name__ == "__main__":
    main()
    pygame.quit()

