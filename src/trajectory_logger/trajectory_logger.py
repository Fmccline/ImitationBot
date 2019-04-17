import logging
import datetime
from game_state import GameState
from game_actions import GameActions


class TrajectoryLogger:

    LOG_DELAY = 60.0
    TRAJECTORY_DELAY = 1.0
    STATE = 'state'
    ACTIONS = 'actions'
    PATH = 'C:/Users/Administrator/Programming/ReliefBot/logs/'

    def __init__(self, agent):
        self.agent = agent
        self.game_state = GameState(agent.get_field_info())
        self.trajectories = self.make_new_trajectories()
        self.logger = self.setup_trajectory_logger()
        self.last_log = 0
        self.last_trajectory = 0

    def setup_trajectory_logger(self):
        name = self.agent.name
        today = datetime.date.today()
        trajectory_logger = logging.getLogger(name)
        trajectory_logger.setLevel(logging.INFO)
        # create file handler which logs INFO messages
        fh = logging.FileHandler(f'{self.PATH}{name}-{today}.log')
        fh.setLevel(logging.INFO)
        # create console handler with a higher log level
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        trajectory_logger.addHandler(fh)
        trajectory_logger.addHandler(ch)
        return trajectory_logger

    def make_new_trajectories(self):
        trajectories = []
        return trajectories

    def log(self, game_packet, controller):
        seconds_elapsed = game_packet.game_info.seconds_elapsed

        if self.should_add_trajectory(seconds_elapsed):
            self.add_trajectory(game_packet, controller, seconds_elapsed)
        else:
            return
        
        if self.should_log_to_file(seconds_elapsed):
            self.logger.info(str(self.trajectories))
            self.last_log = seconds_elapsed
            self.trajectories = self.make_new_trajectories()

    def add_trajectory(self, game_packet, controller, seconds_elapsed):
        team = self.agent.team
        name = self.agent.name
        ball_prediction = self.agent.get_ball_prediction_struct()
        state = self.game_state.get_game_state(game_packet, team, name, ball_prediction)
        actions = GameActions.get_actions(controller)

        trajectory = {self.STATE: state, self.ACTIONS: actions}
        self.trajectories.append(trajectory)
        self.last_trajectory = seconds_elapsed

    def should_add_trajectory(self, seconds_elapsed):
        return seconds_elapsed - self.last_trajectory > self.TRAJECTORY_DELAY

    def should_log_to_file(self, seconds_elapsed):
        return seconds_elapsed - self.last_log > self.LOG_DELAY

