from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import numpy as np
from trajectory import Trajectory
import bot_models


class SimpleNNRLBot(BaseAgent):
    BASE_PATH = 'C:/Users/Frank\'s Laptop/Desktop/Programming/Python/ImitationBot/src/models/'
    MODEL_PATH = f'{BASE_PATH}model.json'
    WEIGHTS_PATH = f'{BASE_PATH}model.h5'

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.model = bot_models.AdadeltaModel().load_model_from_json()

    def load_model(self):
        from keras.models import model_from_json
        with open(self.MODEL_PATH, 'r') as json_file:
            loaded_model_json = json_file.read()

        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(self.WEIGHTS_PATH)
        loaded_model.compile(optimizer ='adadelta', loss='mean_squared_error', metrics=['accuracy'])
        print("Loaded model from disk")
        return loaded_model

    def get_output(self, packet: GameTickPacket) -> SimpleControllerState:
        # Get state
        # Get input vector from state
        # Make predictions
        # Set controller state based on predictions
        # Return controller state
        input_vector = self.get_input_vector(packet)
        predictions = self.get_predictions(input_vector)
        return self.set_controller_state(predictions)

    def get_input_vector(self, packet):
        '''
        'team',
        'self_score', 'self_x', 'self_y', 'self_z',
        'self_vx', 'self_vy', 'self_vz',
        'self_rx', 'self_ry', 'self_rz'
        'ball0_x', 'ball0_y', 'ball0_z',
        'ball0_vx', 'ball0_vy', 'ball0_vz',
        '''
        input_vector = np.zeros((1, 16))
        for other_car in packet.game_cars:
            if other_car.name == self.name:
                car = other_car
        location = car.physics.location
        velocity = car.physics.velocity
        rotation = car.physics.rotation
        team = car.team
        score = car.score_info.score
        x = location.x
        y = location.y
        z = location.z
        vx = velocity.x
        vy = velocity.y
        vz = velocity.z
        rx = rotation.pitch
        ry = rotation.yaw
        rz = rotation.roll
        positions = Trajectory.get_normalized_location([x, y, z])
        velocities = Trajectory.get_normalized_velocity([vx, vy, vz])
        rotations = Trajectory.get_normalized_rotation([rx, ry, rz])
        car_input = [team] + positions + velocities + rotations

        ball = packet.game_ball.physics
        ball_location = ball.location
        ball_velocity = ball.velocity
        ball_x = ball_location.x
        ball_y = ball_location.y
        ball_z = ball_location.z
        ball_vx = ball_velocity.x
        ball_vy = ball_velocity.y
        ball_vz = ball_velocity.z
        ball_positions = Trajectory.get_normalized_location([ball_x, ball_y, ball_z])
        ball_velocities = Trajectory.get_normalized_velocity([ball_vx, ball_vy, ball_vz])
        ball_input = ball_positions + ball_velocities

        index = 0
        feature_list = car_input + ball_input
        for feature in feature_list:
            input_vector[0, index] = feature
            index += 1
        return input_vector

    def get_predictions(self, input_vector):
        predictions = self.model.predict(input_vector)
        for index in range(len(predictions)):
            predictions[0, index] = round(predictions[0, index] * 4) / 4.0
        return predictions

    def set_controller_state(self, predictions):
        cs = self.controller_state
        cs.throttle = predictions[0, 0]
        cs.steer = predictions[0, 1]
        cs.pitch = predictions[0, 2]
        cs.yaw = predictions[0, 3]
        cs.roll = predictions[0, 4]
        cs.jump = predictions[0, 5]
        cs.boost = predictions[0, 6]
        cs.brake = predictions[0, 7]
        return cs
