#-*- coding: utf-8 -*-
import math
import time
from games import Item_Shop

class Champ():
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def self_intro(self):
		print('I am lv {} {} {}.'.format(self.lv, self.nickname, self.name))

	def move(self, val):
		if val[0] < -1 or val[0] > 10000 or val[1] < -1 or val[1] > 10000:
			return "超出可移動範圍了"
		self.coord = val
		return "%s moves to %s" % (self.name, self.coord)

	def display_coord(self):
		return "%s at %s" % (self.name, self.coord)

	def learn_q(self):
		self.q.lvup()

	def learn_w(self):
		self.w.lvup()

	def learn_e(self):
		self.e.lvup()

	def learn_r(self):
		self.r.lvup()

	def trigger_basic(self, coord):
		self.basic.trigger(self, coord)

	def trigger_q(self, coord):
		if self.q.lv == 0:
			return "You haven't leant Q"
		return self.q.trigger(self, coord) #target is a champ object

	def trigger_w(self, coord):
		if self.w.lv == 0:
			return "You haven't leant W"
		return self.w.trigger(self, coord)

	def trigger_e(self, coord):
		if self.e.lv == 0:
			return "You haven't leant E"
		return self.e.trigger(self, coord)

	def trigger_r(self, coord):
		if self.r.lv == 0:
			return "You haven't leant R"
		return self.r.trigger(self, coord)


class Champ_In_ARAM():
	def __init__(self, aram_center=None, team_idx=None, member_idx=None, item_shop=None):
		self.alive = True
		self._lv = 3
		self.exp = 0
		self._gold = 1400
		self.self_value_idx = (0, 0)
		self.kill_count = 0
		self.death_count = 0
		self._death_after_kill = 0 #用來算gold
		self.assist_count = 0
		self.cont_kill_count = 0
		self._health = self._max_health
		self._mana = self._max_mana
		self.coord = (1, 1)
		self.items = []
		self.aram_center = aram_center
		self.item_shop = item_shop
		self.team_idx = team_idx
		self.member_idx = member_idx

	def buy_item(self, item_code):
		return self.item_shop.order(self, item_code)

	def sell_item(self, item_idx):
		return self.item_shop.recycle(self, item_idx)

	def display_items(self):
		msg = ''
		for idx, item in enumerate(self.items):
			item_msg = "(%d) %s\n" % (idx+1, item.name)
			msg += item_msg
		if not msg:
			msg = 'You have nothing'
		return msg

	def distance(self, target):
		return sqrt(math.pow(self.x - target.x, 2) + math.pow(self.y - target.y, 2))

	def inform_dmg(self, attacker_idx, dmg, ability_name):
		time_stamp = time.time()
		return self.aram_center.update_dmg((attacker_idx, self.member_idx, dmg, ability_name, time_stamp))

	def inform_death(self):
		return self.aram_center.update_death(self.member_idx)

	@property
	def gold(self):
		return self._gold

	@gold.setter
	def gold(self, val):
		if val < 0:
			return
		self._gold = val

	@property
	def death_after_kill(self):
		return self._death_after_kill

	@death_after_kill.setter
	def death_after_kill(self, val):
		if val < 0:
			val = 0
		self._death_after_kill = val

	@property
	def health_regen(self):
		return self._health_regen

	@health_regen.setter
	def health_regen(self, val):
		# check range
		self._health_regen = val

	@property
	def max_health(self):
		return self._max_health

	@max_health.setter
	def max_health(self, val):
		# check range
		self._max_health = val

	@property
	def max_mana(self):
		return self._max_mana

	@max_mana.setter
	def max_mana(self, val):
		# check range
		self._max_mana = val

	@property
	def mana_regen(self):
		return self._mana_regen

	@mana_regen.setter
	def mana_regen(self, val):
		# check range
		self._mana_regen = val

	@property
	def health(self):
		return self._health

	@health.setter
	def health(self, val):
		if val < 0:
			val = 0
		elif val > self._max_health:
			val = _max_health
		self._health = val

	@property
	def mana(self):
		return self._mana

	@mana.setter
	def mana(self, val):
		if val < 0:
			val = 0
		elif val > self._max_mana:
			val = self._max_mana
		self._mana = val

	@property
	def move_speed(self):
		return self._move_speed

	@move_speed.setter
	def move_speed(self, val):
		if val < 0:
			val = 0
		self._move_speed = val

	@property
	def lv(self):
		return self._lv

	@lv.setter
	def lv(self, val):
		if val >= 18:
			return
		self._lv = val

	@property
	def magic_resist(self):
		return self._magic_resist

	@magic_resist.setter
	def magic_resist(self, val):
		if val < 0:
			val = 0
		self._magic_resist = val

	@property
	def armor(self):
		return self._armor

	@armor.setter
	def armor(self, val):
		if val < 0:
			val = 0
		self._armor = val

	@property
	def atk_speed(self):
		return self._atk_speed

	@atk_speed.setter
	def atk_speed(self, val):
		if val < 0:
			val = 0
		self._atk_speed = val

	@property
	def ad_dmg(self):
		return self._ad_dmg

	@ad_dmg.setter
	def ad_dmg(self, val):
		if val < 0:
			return
		self._ad_dmg = val

	@property
	def ap_dmg(self):
		return self._ap_dmg

	@ap_dmg.setter
	def ap_dmg(self, val):
		if val < 0:
			return
		self._ap_dmg = val

	def lvup(self):
		self.lv += 1
		self.max_health += self._health_incr_per_lv
		self.health_regen +=  self._health_regen_incr_per_lv
		self.max_mana += self._mana_incr_per_lv
		self.mana_regen +=  self._mana_regen_incr_per_lv
		self.armor += self._armor_incr_per_lv
		self.magic_resist += self._magic_resist_incr_per_lv
		self.atk_speed *= 1+0.01*self._atk_speed_incr_per_lv
		self.move_speed += self._move_speed_incr_per_lv


