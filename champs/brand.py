#-*- coding: utf-8 -*-
from abilities import Ability, AP_Dmg_Effect, Stun_Effect, Slow_Effect, \
Direct_Targeted_Ability, Ground_Targeted_Ability, Unit_Targeted_Ability
from champs.champion import Champ, Champ_In_ARAM
import time

class Brand(Champ, Champ_In_ARAM):
    def __init__(self, aram_center=None, team_idx=None, member_idx=None, item_shop=None):
        Champ.__init__(self, name='Brand', nickname='the Burning Vengeance',
        attrs=['mage'], _max_health=507.68, _max_mana=375.6, _ap_dmg=57.04, _atk_speed=0.625,
        _move_speed=340, _health_regen=5.42, _mana_regen=8.005, _magic_resist=30, _armor=21.88,
        _health_incr_per_lv=76, _mana_incr_per_lv=42, _atk_speed_incr_per_lv=3, _dmg_incr_per_lv=1.36,
        _move_speed_incr_per_lv=0, _health_regen_incr_per_lv=0.55,
        _mana_regen_incr_per_lv=0.6, _armor_incr_per_lv=3.5, ap_penetrat=0, ad_penetrat=0,
        _magic_resist_incr_per_lv=0, innate=Blaze(), basic=Basic(), q=Sear(), w=Pillar_Of_Flame(), e=Conflagration(), r=Pyroclasm())
        Champ_In_ARAM.__init__(self, aram_center=aram_center, team_idx=team_idx, member_idx=member_idx, item_shop=item_shop)


class Blaze():
    def __init__(self):
        pass

    def explode(self, attacker, target):
        #time.sleep(2)
        dmg = target.max_health * (12 + 0.5 * attacker.lv) / 100 - target.magic_resist
        return self.cal_real_dmg(attacker, target, dmg, 'Blaze')

    def ablaze(self, target):
        for i in range(4):
            #time.sleep(1)
            target.health *= 0.98

    def has_blaze(self, target):
        if not hasattr(target, 'Blaze'):
            setattr(target, 'Blaze', 0)

    def innate_effect(self, attacker, target):
        self.ablaze(target)
        target.Blaze += 1
        return "Blaze"
        if target.Blaze == 3:
            return self.explode(attacker, target)

class Basic(AP_Dmg_Effect, Unit_Targeted_Ability):
    def __init__(self):
        Unit_Targeted_Ability.__init__(self, range=550)

    def trigger(self, attacker, coord):
        if not self.valid_range(attacker.coord, coord):
            return "超過施放範圍"
        target = self.find_target(attacker, coord)
        if not target:
            return "沒打到人"
        msg = ''
        msg += self.start_attack(attacker, target)
        return msg

class Sear(Direct_Targeted_Ability, Ability, AP_Dmg_Effect, Stun_Effect, Blaze):
    def __init__(self, aram_center=None):
        Ability.__init__(self, name='Sear', _keypress='q', _cooldown_arr=[8, 7.5, 7, 6.5, 6], _cost_arr=[50, 50, 50, 50, 50],
            _cost_type='mana', max_lv=5)
        Direct_Targeted_Ability.__init__(self, range=900)
        AP_Dmg_Effect.__init__(self, _dmg_arr=[80, 110, 140, 170, 210])
        Stun_Effect.__init__(self, _duration_arr=[1.5, 1.5, 1.5, 1.5, 1.5], delay=0)
        Blaze.__init__(self)

    def trigger(self, attacker, coord):
        if not self.valid_range(attacker.coord, coord):
            return "超過施放範圍"

        msg = ''
        msg += self.ability_cost(attacker) +'\n'
            
        target = self.find_target(attacker, coord, False)

        if not target:
            msg += '沒打到人'
            return msg

        target = target[0]

        msg += self.start_attack(attacker, target) +'\n'
        self.has_blaze(target)
        if target.Blaze >= 1:
            msg += self.do_cc(target) +'\n'
        self.finish_attack(attacker, target)
        
        msg += self.innate_effect(attacker, target)

        return msg

class Pillar_Of_Flame(Ground_Targeted_Ability, Ability, AP_Dmg_Effect, Blaze):
    def __init__(self, aram_center=None):
        Ability.__init__(self, name='Pillar of Flame', _keypress='w', _cooldown_arr=[10, 9.5, 9, 8.5, 8], _cost_arr=[60, 70, 80, 90, 100], _cost_type='mp', max_lv=5)
        AP_Dmg_Effect.__init__(self, _dmg_arr=[75, 120, 165, 210, 255], delay=1)
        Ground_Targeted_Ability.__init__(self, range=900, radius=125)
        Blaze.__init__(self)

    def start_attack_with_blaze(self, attacker, target):
        dmg = (self._dmg_arr[self.lv-1] - target.magic_resist) * 1.25
        return self.cal_real_dmg(attacker, target, dmg, self.name)

    def trigger(self, attacker, coord):
        if not self.valid_range(attacker.coord, coord):
            return "超過施放範圍"
        
        msg = ''
        msg += self.ability_cost(attacker) +'\n'

        targets = self.find_target(attacker, coord)
        if not targets:
            msg += "沒打到人"
            return msg

        for target in targets:
            self.has_blaze(target)
            if target.Blaze >= 1:
                msg += self.start_attack_with_blaze(attacker, target) +'\n'
            else:
                msg += self.start_attack(attacker, target) +'\n'
            self.finish_attack(attacker, target)
            msg += self.innate_effect(attacker, target)
        return msg


class Conflagration(Unit_Targeted_Ability, Ability, AP_Dmg_Effect, Blaze):
    def __init__(self):
        Ability.__init__(self, name='Conflagration', _keypress='e', _cooldown_arr=[10, 9.5, 9, 8.5, 8], _cost_arr=[60, 70, 80, 90, 100], _cost_type='mp', max_lv=5)
        AP_Dmg_Effect.__init__(self, _dmg_arr=[75, 120, 165, 210, 255], delay=1)
        Unit_Targeted_Ability.__init__(self, range=625)
        Blaze.__init__(self)

    def trigger(self, attacker, coord):
        if not self.valid_range(attacker.coord, coord):
            return "超過施放範圍"

        target = self.find_target(attacker, coord)
        if not target:
            return "沒打到人"

        msg = ''
        msg += self.ability_cost(attacker) +'\n'
        
        self.has_blaze(target)

        if target.Blaze >= 1:
            #周圍爆, 算target的附近有誰
            msg += self.start_attack(attacker, target) +'\n'
        else:
            msg += self.start_attack(attacker, target) +'\n'
        msg += self.innate_effect(attacker, target)
        self.finish_attack(attacker, target)
        return msg

class Pyroclasm(Unit_Targeted_Ability, Ability, AP_Dmg_Effect, Slow_Effect, Blaze):
    def __init__(self):
        Ability.__init__(self, name='Pyroclasm', _keypress='r', _cooldown_arr=[105, 90, 75], _cost_arr=[100, 100, 100], _cost_type='mp', max_lv=3)
        AP_Dmg_Effect.__init__(self, _dmg_arr=[100, 200, 300], delay=1)
        Slow_Effect.__init__(self, _slow_percent_arr=[30, 45, 60])
        Unit_Targeted_Ability.__init__(self, range=750)
        Blaze.__init__(self)

    def trigger(self, attacker, coord):
        if not self.valid_range(attacker.coord, coord):
            return "超過施放範圍"

        target = self.find_target(attacker, coord)
        if not target:
            return "沒打到人"

        #反彈還沒寫

        msg = ''
        msg += self.ability_cost(attacker) +'\n'
        msg += self.start_attack(attacker, target) +'\n'
        if target.Blaze >= 1:
            self.do_cc(target)
        msg += self.innate_effect(attacker, target)
        self.finish_attack(attacker, target)
        return msg



 #CC: http://leagueoflegends.wikia.com/wiki/Crowd_control