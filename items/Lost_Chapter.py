from Item import Item
from Amplifying_Tome import Amplifying_Tome
from Sapphire_Crystal import Sapphire_Crystal

class Lost_Chapter(Item):
	def __init__(self):
		Item.__init__(self, name='Lost Chapter', code=3802, cost=900, sell=630)
		self.sub_items = [Amplifying_Tome(), Sapphire_Crystal()]

	def stats(self, champ):
		champ.ap_dmg += 25
		champ.max_mana += 300
		print("%s ap damage increase %d, mana increase %d" % (champ.name, 25, 300))

	@staticmethod
	def passive_effect(champ):
		champ.mana *= 1.2

	def remove_stats(self, champ):
		champ.ap_dmg -= 25
		champ.max_mana -= 300
		print("%s ap damage decrease %d, mana decrease %d" % (champ.name, 25, 300))

