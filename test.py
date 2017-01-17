#-*- coding: utf-8 -*-
from games import ARAM
from items import *
from champs import Brand, Ziggs

aram = ARAM()

#member_idx: assume每隊5人, team1 0~4, team2 5~9

Brand = Brand(aram_center=aram, team_idx=0, member_idx=0)
Ziggs = Ziggs(aram_center=aram, team_idx=1, member_idx=1)
aram.compose_team([Brand, Ziggs])

Brand.move((10, 10))
Ziggs.move((20, 20))
Brand.lvup()
Brand.learn_q()
Brand.learn_w()
Brand.learn_e()
Brand.learn_r()

Ziggs.learn_q()
Ziggs.learn_w()
Ziggs.learn_e()
Ziggs.learn_r()

Lost_Chapter = Lost_Chapter()
Boots_Of_Speed = Boots_Of_Speed()
Morellonomicon = Morellonomicon()
Amplifying_Tome = Amplifying_Tome()
Morellonomicon.get_data()

Ziggs.buy_item(Lost_Chapter)
Ziggs.buy_item(Boots_Of_Speed)
Ziggs.sell_item(Boots_Of_Speed)

#Ziggs.buy_item(Morellonomicon)
#Ziggs.sell_item(Morellonomicon)



Brand.trigger_q((0, 0))

Ziggs.trigger_q((10, 10))
Ziggs.trigger_w((10, 10))
Ziggs.trigger_e((10, 10))
Ziggs.trigger_r((10, 10))
Ziggs.trigger_r((10, 10))
Ziggs.trigger_r((10, 10))

