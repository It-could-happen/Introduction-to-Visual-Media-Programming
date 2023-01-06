import pygame
import numpy as np
#다양한 정다각형을 그리고 축을 통해 회전시킨다. 
#회전하는 각도는 달라져야 한다. 
#

# 게임 윈도우 크기
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
CENTER = [WINDOW_WIDTH/2, WINDOW_HEIGHT/2]


# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
Biba_magenta = (187, 38, 73)



# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False

# 게임 반복 구간
x=0
px = 0
py = 0
dx = 20
dy = 20
poly = np.array([[350,200], [250, 350], [450, 350]])    

degree = 1
dDegree = 1

radian = np.deg2rad(degree)
c = np.cos(radian)
s = np.sin(radian)
R = np.array( [[c, -s], [s,c]])
R, R.shape

#회전하고싶은 다각형의 좌표 배열과 각도를 입력받아 0,0을 기준으로 회전시키는 함수
def rotate(poly1, degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    Rr = np.array( [[ c, -s], [s, c] ] )
    ppT1 = Rr @ poly1.T 
    pp1 = ppT1.T
    return pp1 

#이동시킬 다각형 배열 g와 이동시기고 싶은 위치 백터 tvec를 입력하면 이동한 다각형 위치 g를 반환
def tranlate(g, tvec):
    tvec = np.array(tvec)
    for i in range(g.shape[0]): # translation by transl vector
        g[i] = g[i] + tvec
    return g 
    #

#랜덤한 색상을 반환
def randomColor():
    return (np.random.randint(20, 240),np.random.randint(20, 240),np.random.randint(20, 240))


cor = np.array( [400, 200])
copypoly = poly.copy()
for p in range(copypoly.shape[0]):
    copypoly[p] = copypoly[p] - cor

copypoly, poly

#원하는 각의 숫자와 반지름을 입력하면 해당 정다각형의 좌표 배열을 반환하는 함수
def nRegularGons(ngon, radi):
    mygons = []
    for i in range(ngon):
        deg = i * 360 / ngon
        radianGons = deg * np.pi/180
        c = np.cos(radianGons)
        s = np.sin(radianGons)
        x = radi * c
        y = radi * s
        mygons.append([x, y])

    mygonsCopy = np.array(mygons)

    return mygonsCopy

#다각형과 색상을 입력하는 경우 해당 다각형의 각 꼭짓점을 이어 별을 그려주는 함수
def drawStar(g5, color):
    n = g5.shape[0]
    for i in range(n):
        pygame.draw.line(screen, color, g5[i%n], g5[(i+2)%n], 5)
    return


gons = []
radius = 100
gons5 = np.array(gons)

#4각형에서 12각형까지의 다각형과 별 좌표를 생성해 랜덤한 좌표를 배정
hwgons = []
for i in range(4, 13):
    newgon = nRegularGons(i, 50)
    tranlate(newgon, [i*20, i*10])
    hwgons.append(newgon)

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

    #각 가속도를 1도/프래임으로 주고 30을 넘어가는 경우 각가속도의 방향을 반대로 전환
    degree= degree + dDegree
    dDegree += 0.5
    if degree >560 or  degree < -560:
        dDegree *=-1 



    poly2= rotate(poly, degree)
    tranlate(poly2, CENTER)
    pygame.draw.polygon(screen, randomColor() ,poly2, 7)


    t = np.array([700, 500])

    new = nRegularGons(7, 100)
    tranlate(new, CENTER)
    for i in range(new.shape[0]):
        new[i] = new[i] + t 
    pygame.draw.polygon(screen, BLACK, new, 5)
    drawStar(new, RED)

    for i in range(0, 9):
        empty = rotate(hwgons[i], degree + i*30)
        tranlate(empty, CENTER)
        pygame.draw.polygon(screen, randomColor(), empty, 5)
        drawStar(empty, randomColor())


    


    # 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
    font = pygame.font.SysFont('FixedSys', 40, True, False)


    # 화면에 텍스트 표시


    # 화면 업데이트
    pygame.display.flip()

    # 초당 60 프레임으로 업데이트
    clock.tick(20)

# 게임 종료
pygame.quit()