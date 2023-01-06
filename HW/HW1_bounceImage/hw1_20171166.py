# -*- coding: utf-8 -*- 
import pygame
import numpy as np 
import os


# 게임 윈도우 크기
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 색 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("20171166 hw1")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

#assets 경로 설정
current_path = os.path.dirname(__file__)
assets_path = os.path.join(current_path, 'assets')
image_path = os.path.join(assets_path, 'sogangimage')


# 학생 이미지 초기 설정
student_image = pygame.image.load(os.path.join(assets_path, 'student.png'))
student_x = int(WINDOW_WIDTH / 2)
student_y = int(WINDOW_HEIGHT / 2)
student_dx = 0
student_dy = 0

#소리 경로 설정 
myBeepSound = pygame.mixer.Sound( os.path.join(assets_path, "20171166_beep.wav" ))
myBeepSound.set_volume(0.01)

#10가지 이미지 딕셔너리 생성 
image = {"1" : "sogang1.png", "2": "sogang2.png", "3" : "sogang3.png", "4" : "sogang4.png", "5":"sogang5.png",
        "6":"sogang6.png", "7":"sogang7.png", "8":"sogang8.png", "9":"sogang9.png", "10":"sogang10.png"}



class sogangImage:
    def __init__(self,):
        self.x = np.random.randint(low=100, high=200)
        self.y = np.random.randint(low=100, high=200)
        self.dx = np.random.randint(-9, 10)
        self.dy = np.random.randint(-10, 11)


        self.time = pygame.time.get_ticks()
        self.period = np.random.uniform(1000, 6000)

        self.imageNum = np.random.randint(low=1, high=10)
        
        self.image = pygame.image.load(os.path.join(image_path, image[str(self.imageNum)]))

        self.width = self.image.get_width() 
        self.height = self.image.get_height()


    def update(self,):
        update_flag = 0
        if 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.time > self.period: # milisecond
                self.dx = np.random.randint(-19, 20)
                self.dy = np.random.randint(-20, 21)
                self.time = current_time
                pass

        self.x += self.dx 
        self.y += self.dy 

        if self.x + self.width > WINDOW_WIDTH:  # right side bounce
            self.dx *= -1
            update_flag = 1

        if self.x < 0: # left side bounce
            self.dx *= -1            
            update_flag = 1


        if self.y + self.height > WINDOW_HEIGHT: # bootom side bounce
            self.dy *= -1
            update_flag = 1

        if self.y < 0: # top side bounce
            self.dy *= -1
            update_flag = 1

        return update_flag


    def draw(self, screen):
        screen.blit(self.image, [self.x, self.y])

# 게임 종료 전까지 반복
done = False

sogang = sogangImage()
print(sogang)
listOfSogangImages = []
for i in range(101):
    sogang = sogangImage()
    listOfSogangImages.append(sogang)

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        # 키가 눌릴 경우
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                student_dx = -3
            elif event.key == pygame.K_RIGHT:
                student_dx = 3
            elif event.key == pygame.K_UP:
                student_dy = -3
            elif event.key == pygame.K_DOWN:
                student_dy = 3
        # 키가 놓일 경우
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                student_dx = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                student_dy = 0

    # 게임 로직 구간
    # 속도에 따라 원형 위치 변경: state update / logic update / parameter update

    student_x += student_dx
    student_y += student_dy

    # -----------------------------------
    # update ball 2
    # your update code here

    for i in range(len(listOfSogangImages)):
        sogang = listOfSogangImages[i]
        soundFlag= sogang.update()
        print(soundFlag)
        if soundFlag == 1:
            myBeepSound.play(0, 1, 1)
            myBeepSound.stop


    # -----------------------------------
    # 윈도우 화면 채우기
    screen.fill(WHITE)

    # 화면 그리기 구간


    screen.blit(student_image, [student_x, student_y])

    for i in range(len(listOfSogangImages)):
        sogang = listOfSogangImages[i]
        sogang.draw(screen)

    # 화면 업데이트
    pygame.display.flip()
    # 초당 60 프레임으로 업데이트
    clock.tick(60) # 60 frames per second
                   # ball_dx = 4
                   # ball_velocity_x = 4 pixels / 1 frame * 60 (frames / second)
                    #                = 240 pixels / second
# 게임 종료
pygame.quit()