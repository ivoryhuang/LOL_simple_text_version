import math
import time

class Champ():
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)

	def self_intro(self):
		print('I am lv {} {} {}.'.format(self.lv, self.nickname, self.name))

	def move(self, coord):
		self.coord = coord
		print("%s moves to %s" % (self.name, self.coord))

	def learn_q(self):
		self.q.lvup()

	def learn_w(self):
		self.w.lvup()

	def learn_e(self):
		self.e.lvup()

	def learn_r(self):
		self.r.lvup()

	def trigger_basic(self, target):
		self.basic.trigger(target, self)

	def learnt_q(self):
		if self.q.lv == 0:
			print("You haven't leant Q")
			return False
		return True

	def learnt_w(self):
		if self.w.lv == 0:
			print("You haven't leant W")
			return False
		return True

	def learnt_e(self):
		if self.e.lv == 0:
			print("You haven't leant E")
			return False
		return True

	def learnt_r(self):
		if self.r.lv == 0:
			print("You haven't leant R")
			return False
		return True



class Champ_In_ARAM():
	def __init__(self, aram_center=None, team_idx=None, member_idx=None):
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
		self._coord = (1, 1)
		self.aram_center = aram_center
		self.team_idx = team_idx
		self.member_idx = member_idx

	def distance(self, target):
		return sqrt(math.pow(self.x - target.x, 2) + math.pow(self.y - target.y, 2))

	def inform_dmg(self, attacker_idx, dmg, ability_name):
		time_stamp = time.time()
		self.aram_center.update_dmg((attacker_idx, self.member_idx, dmg, ability_name, time_stamp))

	def inform_death(self):
		self.aram_center.update_death(self.member_idx)


	@property
	def gold(self):
		return self._gold

	@gold.setter
	def gold(self, val):
		if val < 0:
			val = 0
		if val - self._gold < 0:
			print("not enough gold")
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
	def coord(self):
		return self._coord

	@coord.setter
	def coord(self, val):
		if val[0] < -1 or val[0] > 10000 or val[1] < -1 or val[1] > 10000:
			print("超出可移動範圍了")
			return
		self._coord = val

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

	@property
	def armor(self):
		return self._armor

	@property
	def atk_speed(self):
		return self._atk_speed

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


