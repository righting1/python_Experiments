import csv
class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

        # High score should never be reset.
        self.high_score = 0
        #每次初始化都会打卡数据的csv文件，从里面选择最大的那一个作为最高分在屏幕上面显示
        with open('database/score.csv','r')as f:
            reader = csv.reader(f)
            for row in reader:
                for x in row:
                    self.high_score=max(self.high_score,int(x))
            
    #重置游戏的状态，ship_left是血量
    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1