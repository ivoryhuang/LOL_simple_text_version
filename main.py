#-*- coding: utf-8 -*-
import sys
sys.path.append("./champs")
from brand import Brand
from ziggs import Ziggs
from aram import ARAM

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

Brand.trigger_q((0, 0))

Ziggs.trigger_q((10, 10))
Ziggs.trigger_w((10, 10))
Ziggs.trigger_e((10, 10))
Ziggs.trigger_r((10, 10))
Ziggs.trigger_r((10, 10))
Ziggs.trigger_r((10, 10))