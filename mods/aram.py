#-*- coding: utf-8 -*-

class Gold_Rule():
    def __init__(self):
        #規則 http://lol.hibest.tw/Kill
        self.self_value = [[300, 350, 408, 475, 500], [300, 275, 220, 176, 141, 112, 90, 72, 58, 50]]

    def set_self_value_when_death(self, champ):
        if champ.self_value_idx[0] == 0:
            champ.self_value_idx = (1, 0)
        else:
            champ.self_value_idx = (champ.self_value_idx[0], champ.self_value_idx[1]+1)

    def set_self_value_when_kill(self, champ):
        if champ.self_value_idx[0] == 0:
            champ.self_value_idx = (0, champ.self_value_idx[1]+1)
        else:
            champ.self_value_idx = (0, 0)

    def set_self_value_when_assist(self, champ):
        if champ.self_value_idx[0] == 1:
            champ.self_value_idx = (1, champ.self_value_idx[1]-1)

    def give_gold(self, killer, victim):
        gold = 0
        #if是first blood
        if self.total_death_count == 1:
            gold = 400
        else:
            gold = self.self_value[victim.self_value_idx[0]][victim.self_value_idx[1]]

        killer.gold += gold
        print("%s got %s gold, total %s gold" % (killer.name, gold, killer.gold))

class ARAM(Gold_Rule):
    def __init__(self):
        Gold_Rule.__init__(self)
        self.champs = []
        self.dmg_rcrd = []
        self.tmp_dmg_rcrd = []
        self.total_death_count = 0 #用來看first blood
        self.cont_kill_descript = ['kill', 'Double Kill',
        'Triple Kill', 'Quadra Kill', 'Penta Kill', 'Hexakill', 'Lengendary Kill']
        self.kill_descript = ['Killing spree', 'Rampage', 'Unstoppable', 'Dominating',
        'Godlike', 'Legendary']

    def compose_team(self, champs):
        self.champs = champs

    def update_dmg(self, data):
        self.dmg_rcrd.append(data)
        self.tmp_dmg_rcrd = [data] + self.tmp_dmg_rcrd
        attacker_name = self.champs[data[0]].name
        target = self.champs[data[1]]
        dmg = data[2]
        ability_name = data[3]
        print("%s %s attacks %s, causes %s damage, %s %s health left." % (attacker_name, ability_name, target.name, dmg, target.name, target.health))

    def clean_tmp_dmg_rcrd(self, victim_idx):
        self.tmp_dmg_rcrd = list(filter(lambda x: x[1] != victim_idx, self.tmp_dmg_rcrd))

    def set_champ_dead(self, champ):
        champ.alive = False
        champ.death_count += 1
        champ.cont_kill_count = 0
        champ.death_after_kill += 1
        self.total_death_count += 1
        champ.move((-1, -1)) #死了就離開地圖
        self.set_self_value_when_death(champ)

    def set_champ_kill(self, champ):
        champ.kill_count += 1
        champ.cont_kill_count += 1
        champ.death_after_kill = 0
        self.set_self_value_when_kill(champ)

    def set_champ_assist(self, champ):
        champ.assist_count += 1
        champ.death_after_kill -= 1
        self.set_self_value_when_assist(champ)

    def cal_kill_assist(self, victim_idx):
        #在目標死前 10 秒內對其造成傷害(非擊殺)，就可算是一次助攻
        killer_idx = ''
        assist_idxs = []
        death_time = 0
        for rcrd in self.tmp_dmg_rcrd:
            victim = rcrd[1]
            if victim != victim_idx:
                continue
            attacker_idx = rcrd[0]
            if not killer_idx:
                killer_idx = attacker_idx
                death_time = rcrd[4]
            elif attacker_idx not in assist_idxs:
                assist_time = rcrd[4]
                if death_time - assist_time <= 10:
                    assist_idxs.append(attacker_idx)
        return [killer_idx, assist_idxs]

    def update_death(self, victim_idx):
        victim = self.champs[victim_idx]

        result = self.cal_kill_assist(victim_idx)
        
        killer_idx = result[0]
        assist_idxs = result[1]

        killer = self.champs[killer_idx]
        assists = list(map(lambda x: self.champs[x] ,assist_idxs))

        self.clean_tmp_dmg_rcrd(victim_idx)

        self.set_champ_kill(killer)
        self.set_champ_dead(victim)
        list(map(lambda x: self.set_champ_assist(x), assists))

        self.death_announce(killer, victim)

        self.give_gold(killer, victim)

    def intro(self):
        def member_intro(x):
            print('team'+x.team_idx)
            x.self_intro()
        list(map(member_intro , self.champs))

    def death_announce(self, killer, victim):
        print("%s %s %s" % (killer.name, self.cont_kill_descript[killer.cont_kill_count-1], victim.name))
        if self.aced(victim):
            print("%s aced" % (killer.name))
        
    def aced(self, victim):
        victim_team_idx = victim.team_idx
        for champ in self.champs:
            if champ.team_idx == victim_team_idx and champ.alive:
                return False
        return True
        
