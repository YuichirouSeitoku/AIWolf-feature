import glob
import os
import json

from okawa_feature import OkawaFeature

def save_json(file_path, player_vector_dict):
    output_dir_name = file_path.split('/')
    output_dir_path = os.path.join('.','output', output_dir_name[2], output_dir_name[3])
    os.makedirs(output_dir_path, exist_ok=True)

    output_file_name = output_dir_name[4].replace('.log', '.json')
    output_file_path = os.path.join(output_dir_path, output_file_name)
    print(output_file_path)

    with open(output_file_path, 'w') as f:
        json.dump(player_vector_dict, f, indent=2)

def main(contest_name):

    total_count = 0
    player_dict = {
        'ALL': {
            'SEER': 0,
            'MEDIUM': 0,
            'BODYGUARD': 0,
            'VILLAGER': 0,
            'WEREWOLF': 0,
            'POSSESSED': 0,
            'NOCOMINGOUT': 0
        }
    }

    dires = os.listdir(contest_path)

    for dire in dires:
        dire_path = os.path.join(contest_path, dire, '*.log')
        file_paths = glob.glob(dire_path)

        for file_path in file_paths:

            total_count += 1
            player_vector_dict = OkawaFeature(file_path).get_player_vector_list()
            
            save_json(file_path, player_vector_dict)

if __name__ == '__main__':
    contest_path = './dataset/gat2017log05'
    main(contest_path)
