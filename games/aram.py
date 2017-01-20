#-*- coding: utf-8 -*-
import random
from games.Gold_Center import Gold_Center

class ARAM(Gold_Center):
    def __init__(self):
        Gold_Center.__init__(self)
        self.champs = []
        self.assigned_champs = []
        self.dmg_rcrd = []
        self.tmp_dmg_rcrd = []
        self.total_death_count = 0 #用來看first blood
        self.cont_kill_descript = ['kill', 'Double Kill',
        'Triple Kill', 'Quadra Kill', 'Penta Kill', 'Hexakill', 'Lengendary Kill']
        self.kill_descript = ['Killing spree', 'Rampage', 'Unstoppable', 'Dominating',
        'Godlike', 'Legendary']

    def compose_team(self, champs):
        self.champs = {i: champs[i] for i in range(0, len(champs))}
        self.assign_champ_record()

    def assign_champ_record(self):
        self.assigned_champs = list(range(len(self.champs)))
        random.shuffle(self.assigned_champs)

    def random_assign_champ(self):
        return self.assigned_champs.pop()

    def update_dmg(self, data):
        self.dmg_rcrd.append(data)
        self.tmp_dmg_rcrd = [data] + self.tmp_dmg_rcrd
        attacker_name = self.champs[data[0]].name
        target = self.champs[data[1]]
        dmg = data[2]
        ability_name = data[3]
        return "%s %s attacks %s, causes %s damage, %s %s health left.\n" % (attacker_name, ability_name, target.name, dmg, target.name, target.health)

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

        msg = ''
        msg += self.death_announce(killer, victim) +'\n'

        msg += "%s is dead\n" % (victim.name)
        msg += self.give_gold(killer, victim) +'\n'
        return msg

    def intro(self):
        def member_intro(x):
            print('team'+x.team_idx)
            x.self_intro()
        list(map(member_intro , self.champs))

    def death_announce(self, killer, victim):
        victim.alive = False
        return "%s %s %s\n" % (killer.name, self.cont_kill_descript[killer.cont_kill_count-1], victim.name)
        if self.aced(victim):
            return "%s aced\n" % (killer.name)
        
    def aced(self, victim):
        victim_team_idx = victim.team_idx
        for player_idx, champ in self.champs.items():
            if champ.team_idx == victim_team_idx and champ.alive:
                return False
        return True

    
        
