import copy
import player_info

class OkawaFeature:

    def __init__(self, path):
        self.isTest = 'false'
        self.game_dict = {}
        self.current_day = 0
        self.path = path
        self.agree_list = []
        self.disagree_list = []

        self.boolean_dict = {
            "log":{
                "AGREE":0,
                "DISAGREE":0
             },
            "copy_game_dict":0,
            "make_player_instance":0,
            "update_instance_number_of_seer":0,
            "update_instance_divined_me":{
                "HUMAN":0,
                "WEREWOLF":0
            },
            "update_instance_I_divined":{
                "HUMAN":0,
                "WEREWOLF":0
            },
            "update_instance_is_seer":0,
            "update_instance_seer_order":0,
            "update_instance_vote_target":0,
            "update_instance_vote_change_count":0,
            "update_instance_dead_of_alive":{
                "execute":0,
                "attack":0
            },
            "update_instance_positive_opinions_count":{
                "AGREE":0,
                "ESTIMATE":0
            },
            "update_instance_negative_opinions_count":{
                "DISAGREE":0,
                "ESTIMATE":0
            }
        }

    def get_player_vector_list(self):

        with open(self.path) as lines:
            for line in lines:
                info = line.split(',')
                if info[1] == 'talk':
                    talk_info = info[5].split()
                    if talk_info[0] == 'AGREE' or talk_info[0] == 'DISAGREE':
                        if talk_info[1] == 'TALK':
                            if talk_info[0] == 'AGREE':
                                agree_day = int(talk_info[2][3])
                                agree_id = int(talk_info[3].split(':')[1])
                                self.agree_list.append({'day':agree_day,'id':agree_id,'talker':int(info[4])})
                                self.boolean_dict["log"]["AGREE"] += 1
                            elif talk_info[0] == 'DISAGREE':
                                disagree_day = int(talk_info[2][3])
                                disagree_id = int(talk_info[3].split(':')[1])
                                self.disagree_list.append({'day':disagree_day,'id':disagree_id,'talker':int(info[4])})
                                self.boolean_dict["log"]["DISAGREE"] += 1
                        else:
                            print("AGREE LOG ERROR:{}".format(info))

        with open(self.path) as lines:
            for line in lines:
                info = line.split(',')

                self.current_day = int(info[0])
                self.copy_game_dict(info)
                self.make_player_instance(info)

                self.update_instance_number_of_seer(info)
                self.update_instance_divined_me(info)
                self.update_instance_I_divined(info)
                self.update_instance_is_seer(info)
                self.update_instance_seer_order(info)
                self.update_instance_vote_target(info)
                self.update_instance_vote_change_count(info)
                self.update_instance_dead_or_alive(info)

                self.update_instance_positive_opinions_count(info)
                self.update_instance_negative_opinions_count(info)

        player_vector_dict = self.instance_to_json(info)

        return player_vector_dict

    def copy_game_dict(self, info):
        if self.current_day not in self.game_dict:
            self.game_dict[self.current_day] = {}
            if self.current_day != 0:
                for key, value in self.game_dict[self.current_day - 1].items():
                    self.game_dict[self.current_day][key] = copy.deepcopy(value)
                    self.game_dict[self.current_day][key].day = self.current_day
                    self.boolean_dict["copy_game_dict"] += 1

    def make_player_instance(self, info):
        if info[0] == '0' and info[1] == 'status':
            if info[2] not in self.game_dict[self.current_day]:
                self.game_dict[self.current_day][int(info[2])] = player_info.PlayerInfo(info[5], self.current_day)
                self.boolean_dict["make_player_instance"] += 1

    def update_instance_number_of_seer(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'COMINGOUT' and talk_info[2] == 'SEER':
                for player_dict in self.game_dict[self.current_day].values():
                    player_dict.number_of_seer += 1
                    self.boolean_dict["update_instance_number_of_seer"] += 1

    def update_instance_divined_me(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'DIVINED':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                if talk_info[2] == 'HUMAN':
                    self.game_dict[self.current_day][agent_num].divined_me_human_count += 1
                    self.boolean_dict["update_instance_divined_me"]["HUMAN"] += 1
                if talk_info[2] == 'WEREWOLF':
                    self.game_dict[self.current_day][agent_num].divined_me_wolf_count += 1
                    self.boolean_dict["update_instance_divined_me"]["WEREWOLF"] += 1

    def update_instance_I_divined(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'DIVINED':
                if talk_info[2] == 'HUMAN':
                    self.game_dict[self.current_day][int(info[4])].I_divined_human_count += 1
                    self.boolean_dict["update_instance_I_divined"]["HUMAN"] += 1
                if talk_info[2] == 'WEREWOLF':
                    self.game_dict[self.current_day][int(info[4])].I_divined_wolf_count += 1
                    self.boolean_dict["update_instance_I_divined"]["WEREWOLF"] += 1

    def update_instance_is_seer(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'COMINGOUT' and talk_info[2] == 'SEER':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                if int(info[4]) == agent_num:
                    self.boolean_dict["update_instance_is_seer"] += 1
                    self.game_dict[self.current_day][int(info[4])].is_seer = 1
                else:
                    print(info)
                    print('error')

    def update_instance_seer_order(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'COMINGOUT' and talk_info[2] == 'SEER':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                if int(info[4]) == agent_num:
                    self.game_dict[self.current_day][int(info[4])].seer_order = self.game_dict[self.current_day][int(info[4])].number_of_seer
                    self.boolean_dict["update_instance_seer_order"] += 1
                else:
                    print(info)
                    print('error')

    def update_instance_vote_target(self, info):
        if info[1] == 'talk':
            talk_info = info[5].split()
            if talk_info[0] == 'VOTE':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                self.game_dict[self.current_day][int(info[4])].vote_target = agent_num
                self.boolean_dict["update_instance_vote_target"] += 1
        
    def update_instance_vote_change_count(self, info):
        if info[1] == 'vote':
            if self.game_dict[self.current_day][int(info[2])].vote_target != 0:
                if self.game_dict[self.current_day][int(info[2])].vote_target != info[3]:
                    self.game_dict[self.current_day][int(info[2])].vote_change_count
                    self.boolean_dict["update_instance_vote_change_count"] += 1

    def update_instance_dead_or_alive(self, info):
        if info[1] == 'execute':
            self.game_dict[self.current_day][int(info[2])].dead_or_alive = 1
            self.boolean_dict["update_instance_dead_of_alive"]["execute"] += 1
        if info[1] == 'attack':
            self.game_dict[self.current_day][int(info[2])].dead_or_alive = 2 
            self.boolean_dict["update_instance_dead_of_alive"]["attack"] += 1


    def update_instance_positive_opinions_count(self, info):
        if info[1] == 'talk':
            for self.agree_dict in self.agree_list:
                if int(info[0]) == self.agree_dict['day'] and int(info[2]) == self.agree_dict['id']:
                    self.game_dict[self.current_day][self.agree_dict["talker"]].positive_dict[int(info[4])] += 1
                    self.boolean_dict["update_instance_positive_opinions_count"]["AGREE"] += 1
            talk_info = info[5].split()
            if talk_info[0] == 'ESTIMATE' and talk_info[2] == 'VILLAGER':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                self.game_dict[self.current_day][int(info[4])].positive_dict[agent_num] += 1
                self.boolean_dict["update_instance_positive_opinions_count"]["ESTIMATE"] += 1
                    
    def update_instance_negative_opinions_count(self, info):
        if info[1] == 'talk':
            for self.disagree_dict in self.disagree_list:
                if int(info[0]) == self.disagree_dict['day'] and int(info[2]) == self.disagree_dict['id']:
                    self.game_dict[self.current_day][self.disagree_dict["talker"]].negative_dict[int(info[4])] += 1
                    self.boolean_dict["update_instance_negative_opinions_count"]["DISAGREE"] += 1
            talk_info = info[5].split()
            if talk_info[0] == 'ESTIMATE' and talk_info[2] == 'WEREWOLF':
                agent_num = talk_info[1].split('[')[1][:2]
                if agent_num[0] == '0':
                    agent_num = int(agent_num[1])
                else:
                    agent_num = int(agent_num)
                self.game_dict[self.current_day][int(info[4])].negative_dict[agent_num] += 1
                self.boolean_dict["update_instance_negative_opinions_count"]["ESTIMATE"] += 1

    def instance_to_json(self, info):
        
        player_vector_list = []
        player_instance_dict = {}

        for player_dict in self.game_dict.values():
            for key, player_instance in player_dict.items():
                player_instance_dict = {
                    "daily_elements": {
                        "days": player_instance.day,
                        "name": player_instance.name,
                        "number_of_seer": player_instance.number_of_seer
                    },
                    "player_elements": {
                        "other_divined_me": {
                            "divined_human_count": player_instance.divined_me_human_count,
                            "divined_wolf_count": player_instance.divined_me_wolf_count
                        },
                        "I_divined_other": {
                            "divined_human_count": player_instance.I_divined_human_count,
                            "divined_wolf_count": player_instance.I_divined_wolf_count
                        },
                        "co_order": {
                            "is_seer": player_instance.is_seer,
                            "seer_order": player_instance.seer_order
                        },
                        "vote": {
                            "vote_target": player_instance.vote_target,
                            "vote_change_count": player_instance.vote_change_count
                        },
                        'dead_or_alive': player_instance.dead_or_alive,
                        'number_of_positive': {
                            '1':player_instance.positive_dict[1],
                            '2':player_instance.positive_dict[2],
                            '3':player_instance.positive_dict[3],
                            '4':player_instance.positive_dict[4],
                            '5':player_instance.positive_dict[5]
                        },
                        'number_of_negative': {
                            '1':player_instance.negative_dict[1],
                            '2':player_instance.negative_dict[2],
                            '3':player_instance.negative_dict[3],
                            '4':player_instance.negative_dict[4],
                            '5':player_instance.negative_dict[5]
                        },
                    }
                }
                del player_instance_dict["player_elements"]["number_of_positive"][str(key)]
                del player_instance_dict["player_elements"]["number_of_negative"][str(key)]
                player_vector_list.append(player_instance_dict)

        if self.isTest == 'true':
            print("self.boolean_dict")
            print(self.boolean_dict)

        return player_vector_list
