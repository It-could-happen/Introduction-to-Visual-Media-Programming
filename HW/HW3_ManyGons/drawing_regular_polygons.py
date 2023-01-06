# -*- coding: utf-8 -*- 

import pygame
import numpy as np 

def regularNGon(ngon):
    #nd을 넣으면 n각형의 좌표를 가진 배열을 반환하는 함수
    gons5 = []
    radius = 1
    for i in range(ngon):
        deg = i * 360. / ngon
        radian = deg * np.pi / 180
        c = np.cos(radian)
        s = np.sin(radian)
        x = radius * c 
        y = radius * s
        gons5.append([x,y])
    gons5 = np.array(gons5)
    return gons5 
#
def rotate(poly1, degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    Rr = np.array( [[ c, -s], [s, c] ] )
    #R, R.shape
    ppT1 = Rr @ poly1.T 
    pp1 = ppT1.T
    return pp1 
        #
def rotateByPoint(poly, degree, x, y):
    pass

def tranlate(g, tvec):
    tvec = np.array(tvec)
    for i in range(g.shape[0]): # translation by transl vector
        g[i] = g[i] + tvec
    return g 

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

class polygonEntity:
    def __init__(self, ngon = -1):
        self.color = (255, 0, 0)
        self.n = np.random.randint(3, 13)
        self.radius = np.random.randint(5,30)
        self.vertices = self.radius * regularNGon(self.n)

        #self.pos = np.array([self.radius, self.radius])+ [200, 100]
        self.p= self.vertices.copy()
        self.tr = np.array([300.0,300.0]) #initial position
        self.degree = 0 #rotation
        self.vdeg = 10

        self.vxy = np.array([10,7])

        self.destroyed = False

    def update(self, ):
        self.degree += self.vdeg
        self.tr += self.vxy
        self.p = rotate(self.vertices.copy(), self.degree)
        self.p= tranlate(self.p, self.tr)

        if self.tr[0] + self.radius > WINDOW_WIDTH:
            self.tr[0] = WINDOW_WIDTH - self.radius
            self.vxy[0] *= -1
        if self.tr[0] - self.radius < 0:
            self.tr[0] = self.radius
            self.vxy[0] *= -1
        if self.tr[1] + self.radius > WINDOW_HEIGHT:
            self.tr[1] = WINDOW_HEIGHT - self.radius
            self.vxy[1] *= -1
        if self.tr[1] - self.radius < 0:
            self.tr[1] = self.radius
            self.vxy[1] *= -1
        pass

    def draw(self, scr):
        pygame.draw.polygon(scr, self.color, self.p )

def collision(elist, i, j):
    flag = False
    e1 = elist[i]
    e2 = elist[j]
    diff = e1.tr - e2.tr
    dist = np.sqrt(np.power(diff[1],2.) + np.power(diff[0], 2.))
    if dist < e1.radius + e2.radius:
        flag = True

    return flag


def makeSound(i, j):
    print("sound", i, j)


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
    polyList = []
    polygonEnt = polygonEntity()
    for i in range(200):
        pe = polygonEntity(np.random.randint(3,20))
        pe.vxy= np.random.uniform(-6, 7, size=2)
        pe.vdeg = np.random.uniform(-6, 7)
        pe.color = (np.random.randint(0,256), np.random.randint(0,256), np.random.randint(0,256))
        polyList.append(pe)

    removeList = []
    time = 0

    # 게임 반복 구간
    while not done:
        time +=1
        # 이벤트 반복 구간
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # 게임 로직 구간

        # 화면 삭제 구간

        # 윈도우 화면 채우기
        screen.fill(WHITE)


        # 다각형 그리기
        for i in range(len(polyList)):
            polyList[i].draw(screen)
        #polygonEnt.draw(screen)

        for i in range(len(polyList)):
            polyList[i].update()

        #collision
        if time > 50:
            removeList.clear()
            for i in range(len(polyList)):
                for j in range(i+1, len(polyList)):
                    if collision(polyList, i, j):
                        makeSound(i, j)
                        removeList.append(i)
                        removeList.append(j)
                        polyList[i].destroyed = True
                        polyList[j].destroyed = True

            removeListCopy = list(set(removeList))
            for i in range(len(removeListCopy)):
                j = len(removeListCopy) - i -1
                if polyList[j].destroyed == True:
                    del polyList[j]


        # 안티얼리어스를 적용하고 검은색 문자열 렌더링
        text = font.render("Hello Pygame", True, BLACK)
        screen.blit(text, [200, 600])

        # 화면 업데이트
        pygame.display.flip()
        polygonEnt.update()
        clock.tick(20)

    # 게임 종료

if __name__ == "__main__":
    main()
    pygame.quit()

