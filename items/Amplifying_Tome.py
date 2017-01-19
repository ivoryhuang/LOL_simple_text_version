from items.Item import Item

class Amplifying_Tome(Item):
	def __init__(self):
		Item.__init__(self, name='Amplifying Tome', code=1052, cost=435, sell=305)
		self.sub_items = None

	def stats(self, champ):
		champ.ap_dmg += 20
		return "%s ap damage increase %d" % (champ.name, 20)

	def remove_stats(self, champ):
		champ.ap_dmg -= 20
		return "%s ap damage decrease %d" % (champ.name, 20)