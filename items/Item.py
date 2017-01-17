import copy

class Item():
	def __init__(self, name=None, code=None, cost=None, sell=None):
		self.name = name
		self.code = code
		self.cost = cost
		self.sell = sell
		self.sub_items = [] #下層的item

	def stats(self, champ):
		pass

	@staticmethod
	def passive_effect(champ):
		pass
		
	def remove_stats(self, champ):
		pass

	def bought(self, champ):
		if self.cost > champ.gold:
			return
		champ.gold -= self.cost
		print("%s bought %s, costs %d" % (champ.name, self.name, self.cost))
		self.stats(champ)

	def sold(self, champ):
		champ.gold += self.sell
		print("%s sold %s, get %d" % (champ.name, self.name, self.sell))
		self.remove_stats(champ)

	@staticmethod
	def gen_item_info(item):
		info = copy.deepcopy(item.__dict__)
		del info['sub_items']
		return info

	@staticmethod
	def search_sub_item(item, structure, item_info):
		if item.sub_items is None:
			return
		
		for sub_item in item.sub_items:
			if item.code not in structure:
				structure[item.code] = {}
			if item.code not in item_info:
				item_info[item.code] = Item.gen_item_info(item)
				
			structure[item.code].update({sub_item.code:{}})
			Item.search_sub_item(sub_item, structure[item.code], item_info)

	def get_data(self):
		structure = {self.code:{}}
		item_info = {self.code:self.gen_item_info(self)}
		self.search_sub_item(self, structure, item_info)
		print("%s %s" % (self.name, structure))
		print(item_info)


class Cool_Down_Item():
	def __init__(self):
		pass

	@staticmethod
	def decrease_cooldown(champ, percent):
		champ.q.cooldown_arr = [champ.q.cooldown_arr[i] - x*percent for i, x in enumerate(champ.q.cooldown_arr_backup)]
		champ.w.cooldown_arr = [champ.w.cooldown_arr[i] - x*percent for i, x in enumerate(champ.w.cooldown_arr_backup)]
		champ.e.cooldown_arr = [champ.e.cooldown_arr[i] - x*percent for i, x in enumerate(champ.e.cooldown_arr_backup)]
		champ.r.cooldown_arr = [champ.r.cooldown_arr[i] - x*percent for i, x in enumerate(champ.r.cooldown_arr_backup)]

	@staticmethod
	def increase_cooldown(champ, percent):
		champ.q.cooldown_arr = [champ.q.cooldown_arr[i] + x*percent for i, x in enumerate(champ.q.cooldown_arr_backup)]
		champ.w.cooldown_arr = [champ.w.cooldown_arr[i] + x*percent for i, x in enumerate(champ.w.cooldown_arr_backup)]
		champ.e.cooldown_arr = [champ.e.cooldown_arr[i] + x*percent for i, x in enumerate(champ.e.cooldown_arr_backup)]
		champ.r.cooldown_arr = [champ.r.cooldown_arr[i] + x*percent for i, x in enumerate(champ.r.cooldown_arr_backup)]
		#return [arr[i] + x*percent for i, x in enumerate(arr_backup)]
#http://leagueoflegends.wikia.com/wiki/Item