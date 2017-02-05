from items.Item import Item, Cool_Down_Item
from items.Fiendish_Codex import Fiendish_Codex
from items.Lost_Chapter import Lost_Chapter
from items.Amplifying_Tome import Amplifying_Tome

class Morellonomicon(Item, Cool_Down_Item):
	def __init__(self):
		Item.__init__(self, name='Morellonomicon', code=3165, cost=2900, sell=2030)
		self.sub_items = [Fiendish_Codex(), Lost_Chapter(), Amplifying_Tome()]

	def stats(self, champ):
		champ.ap_dmg += 100
		champ.max_mana += 400
		self.decrease_cooldown(champ, 0.2)
		return "%s ap damage increase %d, mana increase %d, cooldown decrease %d" % (champ.name, 100, 400, 20) +'%'

	def remove_stats(self, champ):
		champ.ap_dmg -= 100
		champ.max_mana -= 400
		self.increase_cooldown(champ, 0.2)
		return "%s ap damage decrease %d, mana decrease %d, cooldown increase %d" % (champ.name, 100, 400, 20) +'%'
