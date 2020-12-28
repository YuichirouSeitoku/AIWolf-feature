class PlayerInfo:

    def __init__(self, name, day):
        self.name = name
        self.day = day
        self.number_of_seer = 0
        self.divined_me_human_count = 0
        self.divined_me_wolf_count = 0
        self.I_divined_human_count = 0
        self.I_divined_wolf_count = 0
        self.is_seer = 0
        self.seer_order = 0
        self.vote_target = 0
        self.vote_change_count = 0
        self.dead_or_alive = 0
        self.positive_dict = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }
        self.negative_dict = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0
        }

    def update_number_of_seer(self):
        print("update_number_of_seer")
        self.number_of_seer += 1

    def update_divined_me_human_count(self):
        self.divined_me_human_count += 1

    def update_divined_me_wolf_count(self):
        self.divined_me_wolf_count += 1

    def update_I_divined_human_count(self):
        self.I_divined_human_count += 1

    def update_I_divined_wolf_count(self):
        self.I_divined_wolf_count += 1

    def update_is_seer(self):
        self.is_seer = 1

    def update_seer_order(self):
        self.seer_order = self.number_of_seer

    def update_vote_target(self, agent_num):
        self.vote_target = agent_num

    def update_vote_change_count(self):
        self.vote_target += 1
