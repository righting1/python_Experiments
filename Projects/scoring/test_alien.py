from alien_invasion import AlienInvasion

import pytest
import random

random.seed(124)

#测试初始化的时候创建了6个外星人
def test_aline_cnt():
    ai = AlienInvasion()
    assert len(ai.aliens)==6

    
def generate_random_data3():
    param3 = random.randint(1, 100)
    return param3

@pytest.mark.parametrize('param3', [generate_random_data3() for i in range(100)]) 

#在原来的参加建了若干个外星人之后，有创建了param3个外星人
def test__create_alien(param3):
    ai = AlienInvasion()
    t=len(ai.aliens)
    for i in range(param3):
        ai._create_alien(1,1)
    assert len(ai.aliens)==(t+param3)