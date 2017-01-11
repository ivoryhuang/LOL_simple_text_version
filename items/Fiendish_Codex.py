from Item import Item
from Amplifying_Tome import Amplifying_Tome

class Fiendish_Codex(Item):
	def __init__(self):
		Item.__init__(self, name='Fiendish Codex', code=3108, cost=900, sell=630)
		self.sub_items = [Amplifying_Tome()]

	def stats(self, champ):
		champ.ap_dmg += 30
		champ.q.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.q.cooldown_arr_backup, 0.1)
		champ.w.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.w.cooldown_arr_backup, 0.1)
		champ.e.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.e.cooldown_arr_backup, 0.1)
		champ.r.cooldown_arr = self.decrease_cooldown(champ.q.cooldown_arr, champ.r.cooldown_arr_backup, 0.1)
		print("%s ap damge increase %d, cooldown decrease %d" % (champ.name, 30, 10) + '%')

	def remove_stats(self, champ):
		champ.ap_dmg -= 30
		champ.q.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.q.cooldown_arr_backup, 0.1)
		champ.w.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.w.cooldown_arr_backup, 0.1)
		champ.e.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.e.cooldown_arr_backup, 0.1)
		champ.r.cooldown_arr = self.increase_cooldown(champ.q.cooldown_arr, champ.r.cooldown_arr_backup, 0.1)
		print("%s ap damge decrease %d, cooldown increase %d" % (champ.name, 30, 10) + '%')
