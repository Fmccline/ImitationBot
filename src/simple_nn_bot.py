from rlbot.agents.base_agent import BaseAgent, SimpleControllerState
from rlbot.utils.structures.game_data_struct import GameTickPacket
import numpy as np
from keras.models import model_from_json


class SimpleNNRLBot(BaseAgent):
    MODEL_PATH = 'models/model.json'
    WEIGHTS_PATH = 'models/model.h5'

    def initialize_agent(self):
        # This runs once before the bot starts up
        self.controller_state = SimpleControllerState()
        self.model = self.load_model()

    def load_model(self):
        with open(self.MODEL_PATH, 'r') as json_file:
            loaded_model_json = json_file.read()

        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(self.WEIGHTS_PATH)
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
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
        self.set_controller_state(predictions)
        return self.controller_state

    def get_input_vector(self, packet):
        '''
        'team',
        'self_score', 'self_x', 'self_y', 'self_z',
        'self_vx', 'self_vy', 'self_vz',
        'self_rx', 'self_ry', 'self_rz'
        'ball0_x', 'ball0_y', 'ball0_z',
        'ball0_vx', 'ball0_vy', 'ball0_vz',
        '''
        input_vector = np.array.zeros((1, 17))
        car = packet.game_cars[self.name]
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
        car_input = [team, score, x, y, z, vx, vy, vz, rx, ry, rz]

        ball = packet.game_ball.physics
        ball_location = ball.location
        ball_velocity = ball.velocity
        ball_x = ball_location.x
        ball_y = ball_location.y
        ball_z = ball_location.z
        ball_vx = ball_velocity.x
        ball_vy = ball_velocity.y
        ball_vz = ball_velocity.z
        ball_input = [ball_x, ball_y, ball_z, ball_vx, ball_vy, ball_vz]

        index = 0
        feature_list = car_input + ball_input
        for feature in feature_list:
            input_vector[0, index] = feature
            index += 1
        return input_vector

    def get_predictions(self, input_vector):
        predictions = self.model.predict(input_vector)
        return predictions

    def set_controller_state(self, predictions):
        print(predictions)
