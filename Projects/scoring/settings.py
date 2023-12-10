import random
class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings，屏幕的颜色，长宽高
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (1, 1, 65)
        
        
        #每个外星人之间的间隔，间隔的减少数度，屏幕h的最大占比，w的最大占比,h的上限，w的上限
        self.interval=2.3
        self.interval_limit=1.5
        self.decase=0.05
        self.maxh=0.45
        self.maxw=0.45
        self.limh=0.65
        self.limw=0.65
        
        # Ship settings，血量
        self.ship_limit = 3

        # Bullet settings，子弹的半径
        # self.bullet_width = 3
        # self.bullet_height = 15
        self.bullet_r=10
        self.colors=['red','blue','green','pink','purple','yellow']
        #self.color = random.choice(self.colors)
        
        # self.bullet_color =random.choice(self.colors)
        #在这个屏幕里面最多可以发多少子弹
        self.bullets_allowed = 3
        self.bullets_add=1

        # Alien settings，外星人的下降速度
        self.fleet_drop_speed = 10

        # How quickly the game speeds up,每一个关卡的速度的改变速度
        self.speedup_scale = 1.5
        # How quickly the alien point values increase，每一个关卡一个外星人的分数的增加速度
        self.score_scale = 1.5
        self.sepeed_limit=25

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):#初始化动态信息
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 2
        self.alien_speed = 1.0

        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring settings
        self.alien_points = 10

    def increase_speed(self):#增加速度和子弹的限制，还有外星人在屏幕里面的占比
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale
        self.ship_speed=min(self.ship_speed,self.sepeed_limit)
        self.bullet_speed *= self.speedup_scale
        self.bullet_speed=min(self.bullet_speed,self.sepeed_limit)
        self.alien_speed *= self.speedup_scale
        self.alien_speed=min(self.alien_speed,self.sepeed_limit)
        self.interval-=self.decase
        self.interval=max(self.interval,self.interval_limit)
        self.maxh+=0.05
        self.maxh=min(self.maxh,self.limh)
        self.maxw+=0.05
        self.maxw=min(self.maxw,self.limw)
        
        if (self.bullets_allowed+self.bullets_add)<=10:
            self.bullets_allowed+=self.bullets_add
        self.alien_points = int(self.alien_points * self.score_scale)
    

            