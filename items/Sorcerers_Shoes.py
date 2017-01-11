from Item import Item
from Boots_Of_Speed import Boots_Of_Speed


class Sorcerers_Shoes(Item):
	def __init__(self):
		Item.__init__(self, name="Sorcerer's Shoes", code=3020, cost=1100, sell=770)
		self.sub_items = [Boots_Of_Speed()]

	def stats(self, champ):
		champ.move_speed += 45
		champ.ap_penetrat += 15
		print("%s move_speed increase %d, ap penetration increase %d" % (champ.name, 45, 15) +'%')

	def remove_stats(self, champ):
		champ.move_speed -= 45
		champ.ap_penetrat -= 15
		print("%s move_speed decrease %d, ap penetration decrease %d" % (champ.name, 45, 15) +'%')