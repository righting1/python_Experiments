import sys
import csv
from time import sleep
from pygame import mixer

import pygame
import random
import time

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from start import start
from music import music


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        
        #设置屏幕以及屏幕的标题
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("外星人大战")
        
        #一开始不是全屏
        self.full_screen=False
        
        self.cnt=0
        
        #设置一个数，代表飞船每次射击了lim个外星人之后会改变一次方向，siz是随机数的区间，now是此时距离上一次改变方向之后射击了几个外星人
        self.siz=10
        self.lim=random.randint(0,self.siz)
        self.now=0
        
        # Create an instance to store game statistics,
        #and create a scoreboard.
        #游戏开始，初试分数，游戏关卡
        self.stats = GameStats(self)
        #游戏屏幕上显示的关卡，最高分，和此时的分数
        self.sb = Scoreboard(self)

        #游戏的飞船和动态的星星，音乐初始化
        self.ship = Ship(self)
        self.start=start(self)
        self.music=music()
        
        #子弹组合外星人组
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        #参建外星人群
        self._create_fleet()

        # Start Alien Invasion in an inactive state.
        #游戏还在正常运行
        self.game_active = False
        self.getscore=False

        # Make the Play button.
        #玩游戏的'play'键
        self.play_button = Button(self, "Play")
    
    #保存每次游戏完成后的成绩
    def savescore(self):
        with open('database/score.csv','a',newline='') as f:
            writer = csv.writer(f)
            now=str(self.stats.score)
            writer.writerow([now])
    
    #游戏运行
    def run_game(self):
        """Start the main loop for the game."""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.music.display()
            self.clock.tick(60)

    #监听键盘
    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:#点击了关闭游戏，保存成绩并关掉屏幕
                self.savescore()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        #print('2')
        if not self.game_active :
            #print('3')
            self.savescore()
        if button_clicked and not self.game_active:#重新开始游戏，一些数据需要重置，比如外星人和飞船的速度什么的，
            # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            #self.stats.score=0
            #重置分数，关卡，ship_left,以及更新各种需要显示的一些数据，把游戏的状态改变为游戏正在玩的状态
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            

            # Get rid of any remaining bullets and aliens.
            #释放子弹，外星人的精灵组
            self.bullets.empty()
            self.aliens.empty() 

            # Create a new fleet and center the ship.
            #重新创建外星人群
            self._create_fleet()
            #重新把飞船居中
            self.ship.center_ship()

            # Hide the mouse cursor.
            #鼠标在游戏屏幕可见
            pygame.mouse.set_visible(True)

    #判断键盘是否按下
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        if event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_SPACE:
            self._fire_bullet()
        if event.key==pygame.K_F1:
            #print("1")
            self.full_screen=not self.full_screen
            #全屏和半屏之间的转化
            if self.full_screen:
                #print('2')
                self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height),pygame.FULLSCREEN,32)
            else:
                #print('3')
                self.screen=pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height),0,32)
                
                
    #判断键盘的释放
    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
            
    #发出子弹
    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        #self.music.bullet_display()
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            self.now+=1
            self.music.bullet_display()

    #更新子弹的位置
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        #判断子弹是否达到最上面，如果到达，就移除这颗子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    #判断子弹和外星人之间的碰撞
    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Remove any bullets and aliens that have collided.
        #使用两个精灵组之间的检测碰撞函数，并且两个碰撞的精灵都会消失，都有True
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
       
        #如果发生了碰撞，则播放碰撞的音乐并且加上相应的分数
        if collisions:
            self.music.collsion_display()
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        #如果所有的外星人都被射击了，那么清空子弹，关卡更新，屏幕上显示的关卡信息也更新
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level.
            self.stats.level += 1
            self.sb.prep_level()
    
    #如果外星人已经入侵到需要保护的区域
    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        #如果血量还大于0，血量-1
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Get rid of any remaining bullets and aliens.
            #然后重新更新外星人的和子弹
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship.
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            #表示游戏结束
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        #如果射击外星人的数量等于lim,那么这时候我们需要更新这群外星人的方向
        if self.now==self.lim:
            #print(self.now)
            self._change_fleet_direction()
            self.lim=random.randint(0,self.siz)
            self.now=0
        #判断碰撞到左右边界
        self._check_fleet_edges()
        #更新外星人的位置
        self.aliens.update()

        # Look for alien-ship collisions.
        #判断飞船和外星人之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen.
        self._check_aliens_bottom()
 
    #判断外星人是否进入保护的区域
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break

    #创建外星人群
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        #设置了屏幕的限制，每进入一个更后面的关卡，外星人占屏幕就越大，（但是我们也设置了最大的限度） 还有每个外星人之间的间隔
        while (current_y) < (self.settings.maxh*self.settings.screen_height ):
            while (current_x )< (self.settings.maxw*self.settings.screen_width ):
                self._create_alien(current_x, current_y)
                current_x += self.settings.interval * alien_width

            # Finished a row; reset x value, and increment y value.
            current_x = alien_width
            current_y += max(1,(self.settings.interval-0.5)) * alien_height
        
    #生成一个外星人
    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet."""
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        self.cnt+=1
    
    #判断外星人到达左右边界
    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    #改变外星人的方向
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    #更新游戏画面
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.start.blitme()

        self.aliens.draw(self.screen)
        #self.image = pygame.image.load('./aatck1.png')
        #self.rect = self.image.get_rect()
        #self.screen.blit(self.image, self.rect)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        #如果游戏结束，那么显示玩游戏的键
        if not self.game_active:
            # print('1')
            # self.savescore()
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
     