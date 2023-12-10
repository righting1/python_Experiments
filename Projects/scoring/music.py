import pygame  
import time  
  
class music:  
    def __init__(self):  
        pygame.init()  
        pygame.mixer.init()  
        self.mymixer = pygame.mixer.music.load('music/bg.mp3')  
        self.tim = 5  
        self.mytime = time.time()  # Add tim to current time to set the time to stop playing music  
  
       
  
    def stop_music(self):  
        pygame.mixer.music.stop()  # Stop the music if needed  
  
    #背景音乐的播放
    def display(self):  
        #self.start_music()   
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(loops=0,start=0)
    #子弹生产的音效
    def bullet_display(self):
        p=pygame.mixer.Sound('music/get.mp3')
        p.play()
    #爆炸的音效
    def collsion_display(self):
        p=pygame.mixer.Sound('music/colles.mp3')
        p.play()
        