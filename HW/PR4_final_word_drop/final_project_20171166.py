import pygame
import random
import sys
import numpy as np
from os import path

img_dir = path.join(path.dirname(__file__), 'assets')
snd_dir = path.join(path.dirname(__file__), 'snd')

WIDTH = 1200
HEIGHT = 700
FPS = 60
MAX_WORD =20

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
background = pygame.image.load(path.join(img_dir, "background.jpg"))
background_rect = background.get_rect()
voca_list = ['fire', 'summary','red', 'have', 'crowd', 'money', 'get', 'phone', 'python','degree', 'certificate', 'demand', 'profit', 'quota', 'management', 'president', 'statement', 'branch', 'evaluate', 'payroll', 'patent', 'presence', 'compensation', 'proficient']
clock = pygame.time.Clock()
base_font = pygame.font.SysFont("malgungothic", 80)


class word():
    def __init__(self, screen):
        self.voca = voca_list[np.random.randint(len(voca_list))]
        font = pygame.font.Font(pygame.font.match_font('arial'), 32)
        self.text = font.render(self.voca, True, BLACK)
        self.screen = screen
        self.x = (WIDTH-100)* np.random.random_sample()
        self.y = 0
        self.speedy = random.randrange(1, 2)
        self.destroyFlag = False

    def update(self,):
        self.y +=self.speedy


    def draw(self, ):
        self.screen.blit(self.text, (self.x, self.y) )

    def checkCollision(self,):
        if (self.y > HEIGHT - 100):
            self.destroyFlag == True
            return True
        else:
            return False

    def __del__(self):
        print("del : ", self.voca)

def isGameEnd(life):
    if life <= 0:
        return True
    else:
        return False
    

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def printScore(screen, score):
    draw_text(screen, "score : "+str(score), 18, 100, 40)

def printGoal(screen, goal):
    draw_text(screen, "goal : "+str(goal), 18, 100, 60)

def printLife(screen, life):
    draw_text(screen, "Life : "+str(life), 18, 100, 80)

def printLevel(screen, level):
    draw_text(screen, "level : "+str(level) , 18, 100, 20)


def checkCollect(userWord, other_word):
    if userWord == other_word:
        return True
    else:
        return False
    

def show_go_screen(screen,):
    screen.blit(background, background_rect)
    draw_text(screen, "Words drop!", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "type the words and depend your area", 22,
              WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

def level(num):
    levelList = [360, 240, 120, 60, 30]
    if 1<= num <= 5 :
        return levelList[num-1] 

def main():
    pygame.init()

    #배경음악 설정
    pygame.mixer.init()
    mySound = pygame.mixer.Sound( path.join(img_dir, "bgm.wav" ))
    mySound.play(-1)

    #스크린 설정
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("word drop!")
    font_name = pygame.font.match_font('arial')
    base_font = pygame.font.Font(font_name, 36) 

    user_text = ''
    
    #텍스트 상자 만들기 

    input_rect = pygame.Rect(50, HEIGHT-200, 140, 50)
    color = pygame.Color('lightskyblue3')
    show_go_screen(screen,)
    curlevel = 1
    levelGoal = {1 : 1000, 2 : 2000, 3 : 3000, 4 : 4000, 5 : 5000} 
    period = level(curlevel)
    counter = 0 
    wordList = []
    life = 100
    score = 0
    colorByLevel = {1:(255,255,255), 2:(255,215,215), 3:(255,175,175), 4:(255,145,145), 5:(255,135,135)}

    while True:
        for event in pygame.event.get():

        # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_KP_ENTER:
                    user_text = ''
                else:
                    user_text += event.unicode

        counter += 1
        if counter >= period and len(wordList)<MAX_WORD:
            new = word(screen)
            wordList.append(new)
            counter = 0

        #배경화면 색상 출력 
        screen.fill(colorByLevel[curlevel])
        pygame.draw.line(screen, RED, [0, HEIGHT-100], [WIDTH, HEIGHT-100], 5)
        
        for i in wordList:
            i.draw()
            if checkCollect(user_text, i.voca):
                score +=100
                user_text = ''
                i.destroyFlag = True
            if i.checkCollision(): 
                life -=10
                i.destroyFlag = True
                print('life down')
            i.update()

        #만약 내가 지금 입력한 문자가 워드 리스트상에 존재한다면 스코어 상승 및 해당 문자 삭제 


        #플레이어가 입력한 단어를 화면에 출력
        printScore(screen, score)
        printGoal(screen, levelGoal[curlevel])
        printLife(screen, life)
        printLevel(screen, curlevel )

        pygame.draw.rect(screen, color, input_rect)

        text_surface = base_font.render(user_text, True, (255, 255, 255))
        
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))

        input_rect.w = max(100, text_surface.get_width()+10)

        cur = 0 
        loop = len(wordList) 
        count = 0 

        while True:
            if count >= loop:
                break
            if wordList[cur].destroyFlag:
                del wordList[cur]
                count+=1
                continue
            else:
                count += 1
                cur += 1


        if levelGoal[curlevel]<=score and curlevel<5:
            curlevel+=1
        if isGameEnd(life):

            break

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    

if __name__=='__main__':
    main()
    quit()