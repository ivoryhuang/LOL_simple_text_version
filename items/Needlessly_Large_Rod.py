from Item import Item

class Needlessly_Large_Rod(Item):
	def __init__(self):
		Item.__init__(self, name='Needlessly Large Rod', code=1058, cost=1250, sell=875)
		self.sub_items = None

	def stats(self, champ):
		champ.ap_dmg += 60
		print("%s ap damage increase %d" % (champ.name, 60))

	def remove_stats(self, champ):
		champ.ap_dmg -= 60
		print("%s ap damage decrease %d" % (champ.name, 60))