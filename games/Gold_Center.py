class Gold_Center():
    def __init__(self):
        #規則 http://lol.hibest.tw/Kill
        self.self_value = [[300, 350, 408, 475, 500], [300, 275, 220, 176, 141, 112, 90, 72, 58, 50]]

    def set_self_value_when_death(self, champ):
        if champ.self_value_idx[0] == 0:
            champ.self_value_idx = (1, 0)
        else:
            champ.self_value_idx = (champ.self_value_idx[0], champ.self_value_idx[1]+1)

    def set_self_value_when_kill(self, champ):
        if champ.self_value_idx[0] == 0:
            champ.self_value_idx = (0, champ.self_value_idx[1]+1)
        else:
            champ.self_value_idx = (0, 0)

    def set_self_value_when_assist(self, champ):
        if champ.self_value_idx[0] == 1:
            champ.self_value_idx = (1, champ.self_value_idx[1]-1)

    def give_gold(self, killer, victim):
        gold = 0
        #if是first blood
        if self.total_death_count == 1:
            gold = 400
        else:
            gold = self.self_value[victim.self_value_idx[0]][victim.self_value_idx[1]]

        killer.gold += gold
        return "%s got %s gold, total %s gold\n" % (killer.name, gold, killer.gold)