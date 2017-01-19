from items import *

class Item_Shop():
    def __init__(self):
    	self.items = [Amplifying_Tome(), Blasting_Wand(), Boots_Of_Speed(), Fiendish_Codex(), Lost_Chapter(), Sapphire_Crystal(), Sorcerers_Shoes()]

    def display_items_to_sell(self):
        msg = "You want to buy:\n"
        for item in self.items:
            item_msg = "(%d) %s $%d\n" % (item.code, item.name, item.cost)
            msg += item_msg
        return msg

    @staticmethod
    def display_items_to_recycle(champ):
        msg = "You want to sell:\n"
        for idx, item in enumerate(champ.items):
            item_msg = "(%d) %s $%d\n" % (idx+1, item.name, item.sell)
            msg += item_msg
        return msg

    def order(self, champ, item_code):
        try:
            item = list(filter(lambda x: x.code == item_code, self.items))[0]
        except:
            return "No item"

        sub_items_in_item_list = []

        for sub_item in item.sub_item():
            for own_item in champ.items:
                if sub_item.code == own_item.code:
                    sub_items_in_item_list.append(sub_item)
                    break

        msg = ''
        if len(champ.items) == 6:
            if not sub_items_in_item_list:
                return "物品欄己滿"

        for sub_item in sub_items_in_item_list:
            msg += sub_item.upgrade(champ)
            self.del_item_by_obj(champ, sub_item)

        msg += item.bought(champ)
        champ.items.append(item)
        return msg
        
    def recycle(self, champ, idx):
        item = champ.items[idx]
        self.del_item_by_idx(champ, idx)
        return item.sold(champ)

    def del_item_by_obj(self, champ, del_item):
        for idx, item in enumerate(champ.items):
            if item.code == del_item.code:
                self.del_item_by_idx(champ, idx)

    @staticmethod
    def del_item_by_idx(champ, idx):
        del champ.items[idx]

