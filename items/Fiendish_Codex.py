from items.Item import Item, Cool_Down_Item
from items.Amplifying_Tome import Amplifying_Tome

class Fiendish_Codex(Item, Cool_Down_Item):
	def __init__(self):
		Item.__init__(self, name='Fiendish Codex', code=3108, cost=900, sell=630)
		self.sub_items = [Amplifying_Tome()]

	def stats(self, champ):
		champ.ap_dmg += 30
		self.decrease_cooldown(champ, 0.1)
		return "%s ap damge increase %d, cooldown decrease %d" % (champ.name, 30, 10) + '%'

	def remove_stats(self, champ):
		champ.ap_dmg -= 30
		self.increase_cooldown(champ, 0.1)
		return "%s ap damge decrease %d, cooldown increase %d" % (champ.name, 30, 10) + '%'
