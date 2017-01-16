from Item import Item

class Blasting_Wand(Item):
	def __init__(self):
		Item.__init__(self, name='Blasting Wand', code=1026, cost=850, sell=595)
		self.sub_items = None

	def stats(self, champ):
		champ.ap_dmg += 40
		print("%s ap damage increase %d" % (champ.name, 40))

	def remove_stats(self, champ):
		champ.ap_dmg -= 40
		print("%s ap damage decrease %d" % (champ.name, 40))