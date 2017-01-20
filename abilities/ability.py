import time
import math

class Ability():
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)
		self._lv = 0
		self.cooldown_arr_backup = self._cooldown_arr
		self.timestamp = 0

	def intro(self):
		print("This is lv %s %s \n %s attack" %(self.lv, self.name, self._dmg))

	def ability_cost(self, champ):
		if self._cost_type is None:
			return
		cost = self._cost_arr[self.lv-1]
		if self._cost_type == 'mana':
			champ.mana -= cost
		elif self._cost_type == 'health':
			champ.health -= cost
		return "%s cost %s %s" % (champ.name, cost, self._cost_type)

	def cal_real_dmg(self, attacker, target, dmg, ability_name):
		origin_health = target.health
		target.health -= dmg
		msg = ''
		if target.health > 0:
			real_dmg = dmg
			return target.inform_dmg(attacker.member_idx, real_dmg, ability_name)
		else:
			real_dmg = origin_health
			msg += target.inform_dmg(attacker.member_idx, real_dmg, ability_name)
			msg += target.inform_death()
			return msg

	@property
	def lv(self):
		return self._lv

	@lv.setter
	def lv(self, val):
		if val < 0 or val > self.max_lv:
			return
		self._lv = val

	@property
	def cooldown_arr(self):
		return self._cooldown_arr

	@cooldown_arr.setter
	def cooldown_arr(self, val):
		self._cooldown_arr = val

	def lvup(self):
		self.lv += 1

	def finish_ability(self):
		pass



class Target_Finder():
	def __init__(self, range=None, radius=None):
		self.range = range
		self.radius = radius

	@staticmethod
	def distance(cor1, cor2):
		return math.sqrt(math.pow(cor1[0] - cor2[0], 2) + math.pow(cor1[1] - cor2[1], 2))

	def valid_range(self, attacker_coord, target_coord):
		if self.distance(attacker_coord, target_coord) > self.range:
			return False
		return True


class Unit_Targeted_Ability(Target_Finder):
	def __init__(self, range=None):
		Target_Finder.__init__(self, range=range)
		self.radius = 2

	def find_single_target_by_point(self, attacker, target_coord):
		target = ''
		for player_idx, champ in attacker.aram_center.champs.items():
			if champ.member_idx == attacker.member_idx:
				continue
			if not champ.alive:
				continue

			champ_distance_from_targeted_center = self.distance(target_coord, champ.coord)
			#if target在技能範圍內
			if champ_distance_from_targeted_center > self.radius:
				continue
			target = champ
		return target

	def find_target(self, attacker, coord):
		return self.find_single_target_by_point(attacker, coord)

	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return "超過施放範圍"
		target = self.find_target(attacker, coord)
		if not target:
			return "沒打到人"

		msg = self.start_attack(attacker, target)
		self.finish_attack(attacker, target)
		return msg


class Direct_Targeted_Ability(Target_Finder):
	def __init__(self, range=None, radius=None):
		Target_Finder.__init__(self, range=range, radius=radius)

	def find_target(self, attacker, coord, multi):
		target = []
		attacker_coord_when_aimed = attacker.coord
		vector = (coord[0] - attacker_coord_when_aimed[0], coord[1] - attacker_coord_when_aimed[1])
		'''
		if vector[0] == 0:
			vector = (0.1, vector[1])
		if vector[1] == 0:
			vector = (vector[0], 0.1)
		'''
		for player_idx, champ in attacker.aram_center.champs.items():
			if champ.member_idx == attacker.member_idx:
				continue
			if not champ.alive:
				continue
			ability_vector = (champ.coord[0] - attacker_coord_when_aimed[0], champ.coord[1] - attacker_coord_when_aimed[1])
			#if target和attacker指向的方向在同一直線上, 且在range內

			if ability_vector[0]/vector[0] == ability_vector[1]/vector[1] and self.distance(attacker_coord_when_aimed, champ.coord) <= self.range:
				target.append(champ)
				#if 指向技有多個目標(可穿透)
				if not multi:
					break

		return target

class Ground_Targeted_Ability(Target_Finder):
	def __init__(self, range=None, radius=None):
		Target_Finder.__init__(self, range=range, radius=radius)

	def find_multi_target_by_point(self, attacker, target_coord):
		target = []
		for player_idx, champ in attacker.aram_center.champs.items():
			if champ.member_idx == attacker.member_idx:
				continue
			if not champ.alive:
				continue

			champ_distance_from_targeted_center = self.distance(attacker.coord, champ.coord)

			if champ_distance_from_targeted_center > self.radius:
				continue
			target.append(champ)
		return target

	def find_target(self, attacker, coord):
		return self.find_multi_target_by_point(attacker, coord)

	#標準流程
	def trigger(self, attacker, coord):
		if not self.valid_range(attacker.coord, coord):
			return "超過施放範圍"
		
		msg = ''
		msg += self.ability_cost(attacker)
		
		targets = self.find_target(attacker, coord)

		if not targets:
			msg += "沒打到人"
			return msg

		for target in targets:
			msg += self.start_attack(attacker, target)
			self.finish_attack(attacker, target)
		return msg

#===============================================#
class Dmg_Effect():
	def __init__(self, _dmg_arr=None, _duration_arr=None, delay=None):
		self._dmg_arr = _dmg_arr

	def start_attack(self, attacker, target):
		pass

	def finish_attack(self, attacker, target):
		pass

	def set_dmg_record(self, target, attacker, dmg):
		target.set_dmg_record(self, attacker, dmg)


class AD_Dmg_Effect(Dmg_Effect):
	def __init__(self, _dmg_arr=None, _duration_arr=None, delay=None):
		Dmg_Effect.__init__(self, _dmg_arr=_dmg_arr,
			_duration_arr=_duration_arr, delay=delay)

	def start_attack(self, attacker, target):
		# ad_penetrat to be completed
		dmg = self._dmg_arr[self.lv-1] + attacker.ad_dmg - target.armor
		return self.cal_real_dmg(attacker, target, dmg, self.name)

class AP_Dmg_Effect(Dmg_Effect):
	def __init__(self, _dmg_arr=None, _duration_arr=None, delay=None):
		Dmg_Effect.__init__(self, _dmg_arr=_dmg_arr,
			_duration_arr=_duration_arr, delay=delay)

	def start_attack(self, attacker, target):
		# ap_penetrat to be completed
		dmg = self._dmg_arr[self.lv-1] + attacker.ap_dmg - target.magic_resist
		return self.cal_real_dmg(attacker, target, dmg, self.name)
#===============================================#

class Sup_Effect():
	def __init__(self, _duration_arr=None, delay=None):
		self.duration = duration
		self.delay = delay

	def start_sup(self, target):
		pass

	def finish_sup(self, target):
		pass
#===============================================#

class Regen_Effect(Sup_Effect):
	def __init__(self, regen=None, _duration_arr=None, delay=None):
		Sup_Effect.__init__(_duration_arr=_duration_arr, delay=delay)
		self.regen = regen

	def start_sup(self, target):
		target.health += self.regen

	def finish_sup(self, target):
		pass

#===============================================#
class CC_Effect():
	def __init__(self, cc_name=None, _duration_arr=None, delay=None):
		# http://leagueoflegends.wikia.com/wiki/Crowd_control
		self._duration_arr = _duration_arr

	def do_cc(self, target):
		msg = ''
		msg += self.start_cc(target)
		#time.sleep(self._duration_arr[self.lv-1])
		self.finish_cc(target)
		return msg

	def start_cc(self, target):
		pass

	def finish_cc(self, target):
		pass

	def get_status(self):
		return self.cc_name

	def effect_lvup(self):
		pass



#===============================================#

class Stun_Effect(CC_Effect):
	def __init__(self, _duration_arr=None, delay=None):
		CC_Effect.__init__(self, _duration_arr=_duration_arr, delay=delay)
		self.cc_name = 'stun'

	def start_cc(self, target):
		self.origin_speed = target.move_speed
		target.move_speed = 0
		return "%s stunned" % (target.name)

	def finish_cc(self, target):
		target.move_speed = self.origin_speed


class Blind_Effect(CC_Effect):
	def __init__(self, _duration_arr=None, delay=None):
		CC_Effect.__init__(cc_name = 'blind', _duration_arr=_duration_arr, delay=delay)

	def start_cc(self, target):
		self.origin_speed = target.move_speed
		target.move_speed = 0
		return "%s is blind" % (target.name)

	def finish_cc(self, target):
		target.move_speed = self.origin_speed


class Slow_Effect(CC_Effect):
	def __init__(self, _duration_arr=None, delay=None, _slow_percent_arr=None):
		CC_Effect.__init__(self, cc_name='slow', _duration_arr=_duration_arr, delay=delay)
		self._slow_percent_arr = _slow_percent_arr

	def start_cc(self, target):
		self.origin_speed = target.move_speed
		slow_percent = self._slow_percent_arr[self.lv-1]
		new_speed = self.origin_speed*(100 - slow_percent) /100
		target.move_speed = new_speed
		return "%s slows %s" %(target.name, slow_percent)+'%'

	def finish_cc(self, target):
		target.move_speed = self.origin_speed




#===============================================#

