import json
from json import JSONDecodeError


class RLBotTrajectoryReader:

    def __init__(self):
        self.bot_name = None

    def get_trajectories_from_file(self, filename, bot_name):
        self.bot_name = bot_name
        with open(filename) as file:
            contents = file.read()
        possible_trajectories = self.get_possible_trajectories(contents)
        return self.get_trajectories(possible_trajectories)

    def get_possible_trajectories(self, contents):
        filter_info = f' - {self.bot_name} - INFO - '
        filter_date = '2019'
        contents = contents.split(filter_info)
        possible_trajectories = []
        for index in range(0, len(contents)):
            content = contents[index]
            content = content.split(filter_date)
            possible_trajectory = content[0].replace('\n', '')
            if len(possible_trajectory) > 0 and possible_trajectory[0] == '[':
                possible_trajectories.append(possible_trajectory)
        return possible_trajectories

    def get_trajectories(self, possible_trajectories):
        trajectories = []
        total_misses = 0
        for possible_trajectory in possible_trajectories:
            trajectory_as_json = possible_trajectory.replace('\'', '\"')
            trajectory_as_json = trajectory_as_json.replace('(', '[')
            trajectory_as_json = trajectory_as_json.replace(')', ']')
            try:
                trajectory_list = json.loads(trajectory_as_json)
                for trajectory in trajectory_list:
                    trajectories.append(trajectory)
            except JSONDecodeError:
                total_misses += 1
        print(f'Missed trajectories from exceptions: {total_misses}')
        print(f'Total trajectories: {len(trajectories)}\n')
        return trajectories