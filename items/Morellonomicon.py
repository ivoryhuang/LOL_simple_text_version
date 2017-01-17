from items.Item import Item
from items.Fiendish_Codex import Fiendish_Codex
from items.Lost_Chapter import Lost_Chapter
from items.Amplifying_Tome import Amplifying_Tome

class Morellonomicon(Item):
	def __init__(self):
		Item.__init__(self, name='Morellonomicon', code=3165, cost=2900, sell=2030)
		self.sub_items = [Fiendish_Codex(), Lost_Chapter(), Amplifying_Tome()]

	def stats(self, champ):
		champ.ap_dmg += 100
		champ.max_mana += 400
		champ.q.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.q.cooldown_arr_backup, 0.2)
		champ.w.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.w.cooldown_arr_backup, 0.2)
		champ.e.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.e.cooldown_arr_backup, 0.2)
		champ.r.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.r.cooldown_arr_backup, 0.2)
		print(champ.q.cooldown_arr)
		print("%s ap damage increase %d, mana increase %d, cooldown decrease %d" % (champ.name, 100, 400, 20) +'%')

	def remove_stats(self, champ):
		champ.ap_dmg -= 100
		champ.max_mana -= 400
		champ.q.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.q.cooldown_arr_backup, 0.2)
		champ.w.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.w.cooldown_arr_backup, 0.2)
		champ.e.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.e.cooldown_arr_backup, 0.2)
		champ.r.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.r.cooldown_arr_backup, 0.2)
		print(champ.q.cooldown_arr)
		print("%s ap damage decrease %d, mana decrease %d, cooldown increase %d" % (champ.name, 100, 400, 20) +'%')
