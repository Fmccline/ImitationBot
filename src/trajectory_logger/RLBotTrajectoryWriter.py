import json


class RLBotTrajectoryWriter:

    @staticmethod
    def write_trajectories_to_json(trajectories, filename):
        as_json = json.dumps(trajectories)
        with open(filename, "w+") as file:
            file.write(as_json)
