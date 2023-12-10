from alien_invasion import AlienInvasion

import pytest
import random

random.seed(123)

#测试参建了一颗子弹
def test_fire_bullet():
    ai = AlienInvasion()
    ai._fire_bullet()
    assert len(ai.bullets) == 1

def generate_random_data():
    param1 = random.randint(1, 100)
    param2 = random.randint(1, 100)
    return param1,param2

@pytest.mark.parametrize(['param1', 'param2'], [(generate_random_data()) for i in range(100)]) 

#测试子弹的运动，设置子弹的移动速度为param1,设置初始的y为param2
def test_random_data(param1, param2):
    ai = AlienInvasion()
    ai._fire_bullet
    ai.settings.bullet_speed=param1
    for bullet in ai.bullets:
        bullet.sety(param2)
        ai._update_bullets()
        for bullet in ai.bullets:
            assert bullet.gety()==(param2-param1)
