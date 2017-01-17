from items.Item import Item

class Sapphire_Crystal(Item):
	def __init__(self):
		Item.__init__(self, name='Sapphire Crystal', code=1027, cost=350, sell=245)
		self.sub_items = None

	def stats(self, champ):
		champ.max_mana += 250
		print("%s mana increase %d" % (champ.name, 250))

	def remove_stats(self, champ):
		champ.max_mana -= 250
		print("%s mana decrease %d" % (champ.name, 250))