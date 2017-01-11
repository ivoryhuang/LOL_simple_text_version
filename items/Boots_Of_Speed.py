from Item import Item

class Boots_Of_Speed(Item):
	def __init__(self):
		Item.__init__(self, name='Boots of Speed', code=1001, cost=300, sell=210)
		self.sub_items = None

	def stats(self, champ):
		champ.move_speed += 25
		print("%s move speed increase %d" % (champ.name, 25))

	def remove_stats(self, champ):
		champ.move_speed -= 25
		print("%s move speed decrease %d" % (champ.name, 25))