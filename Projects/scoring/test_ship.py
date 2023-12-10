from alien_invasion import AlienInvasion

import pytest
import random

random.seed(123)


def generate_random_data2():
    param1 = random.randint(1, 100)
    param2 = random.randint(1, 100)
    param3 = random.randint(0,1)
    return param1,param2,param3

@pytest.mark.parametrize(['param1', 'param2','param3'], [(generate_random_data2()) for i in range(100)]) 
#测试飞船的运动，假设运动速度为param1,位置为param2,并设置方向，0代表向右移动，1代表向左移动
def test_ship_update(param1, param2,param3):
    ai = AlienInvasion()
    ai.ship.update()
    ai.settings.ship_speed=param1
    ai.ship.x=param2
    t=1
    if param3:
        ai.ship.moving_left=True
        t*=-1
    else:
        ai.ship.moving_right=True
    ai.ship.update()
    assert ai.ship.x==(param2+param1*t)
        
    
