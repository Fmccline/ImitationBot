class Trajectory:
    FIELD_X = 8192 / 2.0
    FIELD_Y = 11964 / 2.0 # found through testing and bounding between [-1, 1]
    FIELD_Z = 2044.0
    MAX_ROTATION = 10.0
    MAX_SPEED = 3950.0 # found through testing and bounding between [-1, 1]

    SPEEDS = ['NEG_FAST', 'NEG_SLOW', 'ZERO', 'SLOW', 'FAST']

    LOCATION = 'location'
    VELOCITY = 'velocity'
    ROTATION = 'rotation'
    STATE = 'state'
    TEAM = 'team'
    CARS = ['self', 'ally', 'opponent_1', 'opponent_2']
    CAR_STATES = [LOCATION, VELOCITY, ROTATION]
    SCORE = 'score'
    SELF_BOOST = 'SELF_BOOST'
    BALL = 'ball'
    BALLS = ['ball_0.0', 'ball_1.0', 'ball_2.0', 'ball_3.0']
    BALL_STATES = [LOCATION, VELOCITY]
    BOOSTS = 'boosts'
    BOOST_STATES = ['boost_3', 'boost_4', 'boost_15', 'boost_18', 'boost_29', 'boost_30']
    ACTION = 'actions'
    ACTIONS = ['throttle', 'steer', 'pitch', 'yaw', 'roll', 'jump', 'boost', 'handbrake']

    OUT_OF_BOUNDS = 0

    @staticmethod
    def get_normalized_location(position):
        x = position[0] / Trajectory.FIELD_X
        y = position[1] / Trajectory.FIELD_Y
        z = position[2] / Trajectory.FIELD_Z
        positions = [x, y, z]
        Trajectory.test_in_bounds(positions, 'position')
        return positions

    @staticmethod
    def get_normalized_velocity(velocity):
        vx = velocity[0] / Trajectory.MAX_SPEED
        vy = velocity[1] / Trajectory.MAX_SPEED
        vz = velocity[2] / Trajectory.MAX_SPEED
        velocities = [vx, vy, vz]
        Trajectory.test_in_bounds(velocities, 'velocity')
        return velocities

    @staticmethod
    def get_normalized_rotation(rotation):
        x = rotation[0] / Trajectory.MAX_ROTATION
        y = rotation[1] / Trajectory.MAX_ROTATION
        z = rotation[2] / Trajectory.MAX_ROTATION
        rotations = [x, y, z]
        Trajectory.test_in_bounds(rotations, 'rotation')
        return rotations

    @staticmethod
    def test_in_bounds(data, message):
        for index in range(len(data)):
            x = data[index]
            if x > 1 or x < -1:
                # print(f'{x} at index {index} is not within bounds: {message}')
                Trajectory.OUT_OF_BOUNDS += 1

