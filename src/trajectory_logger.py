import logging


class TrajectoryLogger:

    LOG_DELAY = 20.0
    STATE = 'state'
    ACTIONS = 'actions'
    PATH = 'C:/Users/Administrator/Programming/ReliefBot/logs/'

    def __init__(self, name):
        self.logger = self.setup_trajectory_logger(name)
        self.last_log = 0
        self.trajectories = self.make_new_trajectories()

    def setup_trajectory_logger(self, name):
        # create logger with 'spam_application'
        trajectory_logger = logging.getLogger(name)
        trajectory_logger.setLevel(logging.INFO)
        # create file handler which logs INFO messages
        fh = logging.FileHandler(f'{self.PATH}{name}.log')
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
        trajectories = {self.STATE: [], self.ACTIONS: []}
        return trajectories

    def log(self, seconds_elapsed):
        if seconds_elapsed - self.last_log > self.LOG_DELAY:
            self.logger.info(str(self.trajectories))
            self.last_log = seconds_elapsed
            self.trajectories = self.make_new_trajectories()

    def add_trajectory(self, state, actions):
        self.trajectories[self.STATE].append(state)
        self.trajectories[self.ACTIONS].append(actions)
