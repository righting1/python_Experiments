import pygame

import random

from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.game=ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        
        self.colors=['red','blue','green','pink','purple','yellow']#设置攻击小球的颜色
        self.color = random.choice(self.colors)#随机选取的颜色
        

        # Create a bullet rect at (0, 0) and then set correct position.
        #self.rect = pygame.Rect(0, 0, self.settings.bullet_width,self.settings.bullet_height)
        #self.image = pygame.image.load('images/attck10.1.png')
        #self.rect = self.image.get_rect()
        #self.rect = pygame.Rect(0, 0, self.settings.bullet_width,self.settings.bullet_height)
        self.rect = pygame.Rect(0, 0, 1, 1)
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a float.
        self.rect.y=self.y = float(self.rect.y)
        self.rect.x=self.x = float(ai_game.ship.rect.x+ai_game.ship.mid-0.5)

    def update(self):
        """Move the bullet up the screen."""
        # Update the exact position of the bullet.
        self.y -= self.settings.bullet_speed
        # Update the rect position.
        self.rect.y = self.y
        
    def gety(self):
        return self.y
    def sety(self,y):
        self.y=y
    
    #让子弹在屏幕上显示
    def draw_bullet(self):
        """Draw the bullet to the screen."""
        #pygame.draw.rect(self.screen, self.color, self.rect)
        #self.screen.blit(self.image, self.rect)
        #self.game.draw.filled_circle((self.rect.x,self.res.y),self.settings.bullet_r,self.color)
        pygame.draw.circle(self.screen, self.color, (self.x,self.y), self.settings.bullet_r) 