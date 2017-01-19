#-*- coding: utf-8 -*-
from abilities import Ability, AP_Dmg_Effect, Slow_Effect, \
Direct_Targeted_Ability, Ground_Targeted_Ability, Unit_Targeted_Ability
from champs.champion import Champ, Champ_In_ARAM
import time

class Ziggs(Champ, Champ_In_ARAM):
	def __init__(self, aram_center=None, team_idx=None, member_idx=None, item_shop=None):
		Champ.__init__(self, name='Ziggs', nickname='the Hexplosives Expert',
		attrs=['mage'], _max_health=524.4, _max_mana=384, _ap_dmg=54.208, _atk_speed=0.656,
		_move_speed=325, _health_regen=6.25, _mana_regen=6, _magic_resist=30, _armor=21.5,
		_health_incr_per_lv=80, _mana_incr_per_lv=47, _atk_speed_incr_per_lv=2, _dmg_incr_per_lv=3.1,
		_move_speed_incr_per_lv=0, _health_regen_incr_per_lv=0.6,
		_mana_regen_incr_per_lv=0.8, _armor_incr_per_lv=3.3, ap_penetrat=0, ad_penetrat=0,
		_magic_resist_incr_per_lv=0, innate=Short_Fuse())
		Champ_In_ARAM.__init__(self, aram_center=aram_center, team_idx=team_idx, member_idx=member_idx, item_shop=item_shop)
		self.q = Bouncing_Bomb(aram_center=aram_center)
		self.w = Satchel_Charge(aram_center=aram_center)
		self.e = Hexplosive_Minefield(aram_center=aram_center)
		self.r = Mega_Inferno_Bomb(aram_center=aram_center)

	def trigger_basic(self, target):
		self.basic.trigger(self, target)

	def trigger_q(self, coord):
		if self.learnt_q():
			self.q.trigger(self, coord) #target is a champ object

	def trigger_w(self, coord):
		if self.learnt_w():
			self.w.trigger(self, coord)

	def trigger_e(self, coord):
		if self.learnt_e():
			self.e.trigger(self, coord)

	def trigger_r(self, coord):
		if self.learnt_r():
			self.r.trigger(self, coord)
	

class Short_Fuse():
	def __init__(self):
		self._ap_bonus = [20, 24, 28, 32, 36, 40, 48, 56, 64, 72, 80, 88, 100, 112, 124, 136, 148, 160]
		self._cooldown = 12

class Basic(AP_Dmg_Effect, Unit_Targeted_Ability, Short_Fuse):
	def __init__(self):
		pass

	def start_attack(self, attacer, target):
		ap_bonus = self._ap_bonus[attacker.lv-1]
		dmg = self._dmg_arr[self.lv-1] + ap_bonus - target.magic_resist
		self.cal_real_dmg(attacker, target, dmg, self.name)

	def trigger(self, attacker, target):
		if not self.valid_range(attacker.coord, coord):
			return
		self.start_attack(attacker, target)
		self.finish_attack(attacker, target)

class Bouncing_Bomb(Ground_Targeted_Ability, Ability, AP_Dmg_Effect):
	def __init__(self, aram_center=None):
		Ability.__init__(self, name='Bouncing_Bomb', _keypress='q', _cooldown_arr=[6, 5.5, 5, 4.5, 4], _cost_arr=[50, 55, 60, 65, 70], _cost_type='mana', max_lv=5)
		Ground_Targeted_Ability.__init__(self, range=850, radius=150)
		AP_Dmg_Effect.__init__(self, _dmg_arr=[75, 120, 165, 210, 255])
		self.aram_center=aram_center

	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return
		targets = self.aim_ground(attacker, coord)
		if not targets:
			return
		self.ability_cost(attacker)
		for target in targets:
			self.start_attack(attacker, target)
			self.finish_attack(attacker, target)

class Satchel_Charge(Ground_Targeted_Ability, Ability, AP_Dmg_Effect):
	def __init__(self, aram_center=None):
		Ability.__init__(self, name='Satchel_Charge', _keypress='w', _cooldown_arr=[26, 24, 22, 20, 18], _cost_arr=[65, 65, 65, 65, 65], _cost_type='mana', max_lv=5)
		Ground_Targeted_Ability.__init__(self, range=1000, radius=325)
		AP_Dmg_Effect.__init__(self, _dmg_arr=[70, 105, 140, 175, 210])
		self.aram_center=aram_center

	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return
		targets = self.aim_ground(attacker, coord)
		if not targets:
			return
		self.ability_cost(attacker)
		for target in targets:
			self.start_attack(attacker, target)
			self.finish_attack(attacker, target)

class Hexplosive_Minefield(Ground_Targeted_Ability, Ability, AP_Dmg_Effect, Slow_Effect):
	def __init__(self, aram_center=None):
		Ability.__init__(self, name='Hexplosive_Minefield', _keypress='e', _cooldown_arr=[16, 16, 16, 16, 16], _cost_arr=[70, 80, 90, 100, 110], _cost_type='mana', max_lv=5)
		Ground_Targeted_Ability.__init__(self, range=900, radius=325)
		AP_Dmg_Effect.__init__(self, _dmg_arr=[40, 65, 90, 115, 140])
		Slow_Effect.__init__(self, _slow_percent_arr=[20, 25, 30, 35, 40], _duration_arr=[1.5, 1.5, 1.5, 1.5, 1.5])
		self.aram_center=aram_center

	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return
		targets = self.aim_ground(attacker, coord)
		if not targets:
			return
		self.ability_cost(attacker)
		for target in targets:
			self.do_cc(target)
			self.start_attack(attacker, target)
			self.finish_attack(attacker, target)

class Mega_Inferno_Bomb(Ground_Targeted_Ability, Ability, AP_Dmg_Effect):
	def __init__(self, aram_center=None):
		Ability.__init__(self, name='Mega_Inferno_Bomb', _keypress='r', _cooldown_arr=[120, 105, 90], _cost_arr=[100, 100, 100], _cost_type='mana', max_lv=3)
		Ground_Targeted_Ability.__init__(self, range=5300, radius=550)
		AP_Dmg_Effect.__init__(self, _dmg_arr=[200, 300, 400])
		self.aram_center=aram_center

	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return
		targets = self.aim_ground(attacker, coord)
		if not targets:
			return
		self.ability_cost(attacker)
		for target in targets:
			self.start_attack(attacker, target)
			self.finish_attack(attacker, target)
