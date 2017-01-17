from items.Item import Item
from items.Needlessly_Large_Rod import Needlessly_Large_Rod
from items.Blasting_Wand import Blasting_Wand
from items.Amplifying_Tome import Amplifying_Tome


class Rabadons_Deathcap(Item):
	def __init__(self):
		Item.__init__(self, name="Rabadon's Deathcap", code=3089, cost=3800, sell=2660)
		self.sub_items = [Needlessly_Large_Rod(), Blasting_Wand(), Amplifying_Tome()]

	def stats(self, champ):
		champ.ap_dmg += 120
		print("%s ap damage increase %d" % (champ.name, 120))

	@staticmethod
	def passive_effect(champ):
		champ.ap_dmg *= 1.35
		print("%s ap damage increase %d" % (champ.name, 35) + '%')

	def remove_stats(self, champ):
		champ.ap_dmg -= 120
		champ.ap_dmg /= 1.35
		print("%s ap damage decrease %d, damage decrease %d" % (champ.name, 120, 35) +'%')
