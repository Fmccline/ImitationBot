class Trajectory:
    STATE = 'state'
    TEAM = 'team'
    CARS = ['self', 'ally', 'opponent_1', 'opponent_2']
    CAR_STATES = ['location', 'velocity', 'rotation']
    SCORE = 'score'
    SELF_BOOST = 'SELF_BOOST'
    BALL = 'ball'
    BALLS = ['ball_0.0', 'ball_1.0', 'ball_2.0', 'ball_3.0']
    BALL_STATES = ['location', 'velocity']
    BOOSTS = 'boosts'
    BOOST_STATES = ['boost_3', 'boost_4', 'boost_15', 'boost_18', 'boost_29', 'boost_30']
    ACTION = 'actions'
    ACTIONS = ['throttle', 'steer', 'pitch', 'yaw', 'roll', 'jump', 'boost', 'handbrake']

