import csv

from Trajectory import Trajectory


class RLBotTrajectoryWriter:

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
                        'boost0', 'boost1', 'boost2', 'boost3', 'boost4', 'boost5',
                        'self_boost']

        with open(filename, "w+", newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            for trajectory in trajectories:
                state = trajectory[Trajectory.STATE]
                team = state[Trajectory.TEAM]
                as_csv = [team]
                for car_name in Trajectory.CARS:
                    car = state[car_name]
                    as_csv.append(car[Trajectory.SCORE])
                    for car_state in Trajectory.CAR_STATES:
                        for car_state_item in car[car_state]:
                            as_csv.append(car_state_item)

                ball_states = state[Trajectory.BALL]
                for ball_name in Trajectory.BALLS:
                    ball = ball_states[ball_name]
                    for ball_state in Trajectory.BALL_STATES:
                        for ball_state_item in ball[ball_state]:
                            as_csv.append(ball_state_item)

                boosts = state[Trajectory.BOOSTS]
                for boost_state in Trajectory.BOOST_STATES:
                    as_csv.append(boosts[boost_state])

                as_csv.append(state[Trajectory.SELF_BOOST])
                writer.writerow(as_csv)
            print(f'Wrote {len(trajectories)} total trajectories to {filename}')
