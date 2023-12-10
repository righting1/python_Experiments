import pygame,sys
# 导入随机函数模块
import random
from settings import Settings
from pygame.sprite import Sprite
class start(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.screen_width=self.settings.screen_width
        self.screen_height=self.settings.screen_height

        
        self.images=[
            pygame.image.load('images/star/star1.png'),
            pygame.image.load('images/star/star2.2.png'),
            #pygame.image.load('images/star/star3.png'),
            pygame.image.load('images/star/star4.png'),
            pygame.image.load('images/star/star5.png'),
            pygame.image.load('images/star/star6.png'),
            pygame.image.load('images/star/star7.png'),
            pygame.image.load('images/star/star8.png'),
            pygame.image.load('images/star/star9.png'),
                     ]
        #self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen.
        #self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position.
        #self.x = float(self.rect.x)
        
        #每个星星的位置还有每个星星的运动方向
        self.xx=[]
        self.yy=[]
        self.dx=[-1,-1,-1,0,0,1,1,1]
        self.dy=[-1,0,1,-1,1,-1,0,1]
        self.d=[]
        self.lim=100
        self.speed=0.25#运动速度
        self.dis=self.lim#多少次运动然后改变运动的方向
        
    def update(self):
        #print('update')
        for i in range(0,30):
            self.xx.append(random.randint(0,self.screen_width))
            self.yy.append(random.randint(0,self.screen_height))
            t=random.randint(0,len(self.dx)-1)
            self.d.append(t)
    
    #实现星星的运动
    def move(self):
        #print(len(self.xx))
        if len(self.xx)==0:
            self.update()
        for i in range(len(self.xx)):
            self.xx[i]+=self.speed*self.dx[self.d[i]]
            self.yy[i]+=self.speed*self.dy[self.d[i]]
            #print(self.d[i])
            if self.xx[i]>self.screen_width or self.xx[i]<0:
                self.xx[i]=random.randint(0,self.screen_width)
                self.yy[i]=random.randint(0,self.screen_height)
            elif self.yy[i]>self.screen_height or self.yy[i]<0:
                self.xx[i]=random.randint(0,self.screen_width)
                self.yy[i]=random.randint(0,self.screen_height)
        if self.dis==0:
            for i in range(len(self.d)):
                t=random.randint(0,len(self.dx)-1)
                self.d[i]=t
            self.dis=self.lim
        else:
            self.dis-=1
    
    
    def blitme(self):
        self.move()
        #print('1')
        #self.screen.blit(self.image, self.rect)
        for i in range(len(self.xx)):
            #print(i)
            t=i%(len(self.images))
            self.screen.blit(self.images[t], (self.xx[i],self.yy[i]))
            
        