import csv

from trajectory import Trajectory


class RLBotTrajectoryWriter:

    failed_states = 0

    @staticmethod
    def write_trajectories_to_csv(trajectories, filename):
        column_names = ['team',
                        'self_score', 'self_x', 'self_y', 'self_z',
                        'self_vx', 'self_vy', 'self_vz',
                        'self_rx', 'self_ry', 'self_rz',
                        'ally_score', 'ally_x', 'ally_y', 'ally_z',
                        'ally_vx', 'ally_vy', 'ally_vz',
                        'ally_rx', 'ally_ry', 'ally_rz',
                        'opp1_score', 'opp1_x', 'opp1_y', 'opp_1_z',
                        'opp1_vx', 'opp1_vy', 'opp1_vz',
                        'opp1_rx', 'opp1_ry', 'opp1_rz',
                        'opp_2_score', 'opp2_x', 'opp2_y', 'opp2_z',
                        'opp2_vx', 'opp2_vy', 'opp2_vz',
                        'opp2_rx', 'opp2_ry', 'opp2_rz',
                        'ball0_x', 'ball0_y', 'ball0_z',
                        'ball0_vx', 'ball0_vy', 'ball0_vz',
                        'ball1_x', 'ball1_y', 'ball1_z',
                        'ball1_vx', 'ball1_vy', 'ball1_vz',
                        'ball2_x', 'ball2_y', 'ball2_z',
                        'ball2_vx', 'ball2_vy', 'ball2_vz',
                        'ball3_x', 'ball3_y', 'ball3_z',
                        'ball3_vx', 'ball3_vy', 'ball3_vz',
                        'boost0', 'boost1', 'boost2', 'boost3', 'boost4', 'boost5', 'self_boost',
                        'throttle', 'steer', 'pitch', 'yaw', 'roll', 'jump', 'boost', 'handbrake']

        failed_states = 0
        t_num = 0
        with open(filename, "w+", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            for trajectory in trajectories:
                as_csv = []
                state = trajectory[Trajectory.STATE]
                actions = trajectory[Trajectory.ACTION]
                try:
                    RLBotTrajectoryWriter.add_team(as_csv, state)
                    RLBotTrajectoryWriter.add_cars(as_csv, state)
                    RLBotTrajectoryWriter.add_balls(as_csv, state)
                    RLBotTrajectoryWriter.add_boosts(as_csv, state)
                    RLBotTrajectoryWriter.add_actions(as_csv, actions)
                    t_num += 1
                    if t_num % 25000 == 0:
                        print(f"Written {t_num} trajectories so far")
                except Exception as e:
                    failed_states += 1
                    continue
                as_csv = RLBotTrajectoryWriter.normalize_data_list(as_csv)
                writer.writerow(as_csv)
            print(f'Trajectories out of bounds {Trajectory.OUT_OF_BOUNDS}')
            print(f'Missed {failed_states} states/actions')
            print(f'Wrote {len(trajectories) - failed_states} total trajectories to {filename} with {len(column_names)} features')

    @staticmethod
    def add_team(as_csv, state):
        team = state[Trajectory.TEAM]
        as_csv.append(team)

    @staticmethod
    def add_cars(as_csv, state):
        for car_name in Trajectory.CARS:
            car = state[car_name]                
            as_csv.append(car[Trajectory.SCORE])
            for car_state in Trajectory.CAR_STATES:
                if car_state == Trajectory.LOCATION:
                    as_csv += Trajectory.get_normalized_location(car[car_state])
                elif car_state == Trajectory.VELOCITY:
                    as_csv += Trajectory.get_normalized_velocity(car[car_state])
                elif car_state == Trajectory.ROTATION:
                    as_csv += Trajectory.get_normalized_rotation(car[car_state])
                else:
                    raise Exception(f"Invalid car state {car_state}")

    @staticmethod
    def add_balls(as_csv, state):
        ball_states = state[Trajectory.BALL]
        for ball_name in Trajectory.BALLS:
            ball = ball_states[ball_name]
            for ball_state in Trajectory.BALL_STATES:
                if ball_state == Trajectory.LOCATION:
                    as_csv += Trajectory.get_normalized_location(ball[ball_state])
                elif ball_state == Trajectory.VELOCITY:
                    as_csv += Trajectory.get_normalized_velocity(ball[ball_state])
                else:
                    raise Exception(f"Invalid ball state {ball_state}")

    @staticmethod
    def add_boosts(as_csv, state):
        boosts = state[Trajectory.BOOSTS]
        for boost_state in Trajectory.BOOST_STATES:
            as_csv.append(boosts[boost_state])
        as_csv.append(state[Trajectory.SELF_BOOST])

    @staticmethod
    def add_actions(as_csv, actions):
        for action_name in Trajectory.ACTIONS:
            action = round(actions[action_name] * 4) / 4.0
            as_csv.append(action)

    @staticmethod
    def normalize_data_list(data):
        for index in range(len(data)):
            data[index] = round(data[index], 5)
        return data
