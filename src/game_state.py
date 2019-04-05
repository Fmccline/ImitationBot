class GameState:
    LOCATION = 'location'
    VELOCITY = 'velocity'
    SELF = 'self'
    OPPONENT_1 = 'opponent_1'
    OPPONENT_2 = 'opponent_2'
    ALLY = 'ally'
    BALL = 'ball'
    BOOST = 'boosts'
    TEAM = 'team'
    SELF_BOOST = 'SELF_BOOST'

    def __init__(self, field_info):
        self.big_pads = self.add_big_pads(field_info)

    def add_big_pads(self, field_info):
        big_pads = []
        for i in range(field_info.num_boosts):
            pad = field_info.boost_pads[i]
            if pad.is_full_boost:
                big_pads.append(i)
        return big_pads

    def get_game_state(self, packet, team, name, ball_prediction):
        state = {}
        self.add_team_state(state, team)
        self.add_car_states(state, packet, team, name)
        self.add_ball_state(state, packet, ball_prediction)
        self.add_boost_states(state, packet)
        return state

    def add_team_state(self, state, team):
        state[self.TEAM] = team

    def add_car_states(self, state, packet, team, name):
        cars = packet.game_cars
        for car_index in range(packet.num_cars):
            car = packet.game_cars[car_index]
            if car.team != team:
                if self.OPPONENT_1 not in state.keys():
                    state[self.OPPONENT_1] = self.get_car_state(car)
                else:
                    state[self.OPPONENT_2] = self.get_car_state(car)
            elif car.name == name:
                state[self.SELF] = self.get_car_state(car)
                state[self.SELF_BOOST] = int(car.boost)
            else:
                state[self.ALLY] = self.get_car_state(car)

    def get_car_state(self, car):
        car_location = car.physics.location
        location_x = int(car_location.x)
        location_y = int(car_location.y)
        location_z = int(car_location.z)
        location = (location_x, location_y, location_z)

        car_velocity = car.physics.velocity
        velocity_x = int(car_velocity.x)
        velocity_y = int(car_velocity.y)
        velocity_z = int(car_velocity.z)
        velocity = (velocity_x, velocity_y, velocity_z)
        
        car_state = {}
        car_state[self.LOCATION] = location
        car_state[self.VELOCITY] = velocity
        return car_state

    def add_ball_state(self, state, packet, ball_prediction):
        ball_states = {}
        for ball_slice in [0, 60, 120, 180]: # gets ball prediction in 0, 1, 2, and 3 seconds
            ball = ball_prediction.slices[ball_slice]
            ball_location = ball.physics.location
            location_x = int(ball_location.x)
            location_y = int(ball_location.y)
            location_z = int(ball_location.z)
            location = (location_x, location_y, location_z)
            ball_velocity = ball.physics.velocity
            velocity_x = int(ball_velocity.x)
            velocity_y = int(ball_velocity.y)
            velocity_z = int(ball_velocity.z)
            velocity = (velocity_x, velocity_y, velocity_z)
            ball_state = {}
            ball_state[self.LOCATION] = location
            ball_state[self.VELOCITY] = velocity
            ball_states[f'{self.BALL}_{ball_slice/60}'] = ball_state
        state[self.BALL] = ball_states

    def add_boost_states(self, state, packet):
        boost_states = {}
        boosts = packet.game_boosts
        for game_boost in self.big_pads:
            boost = boosts[game_boost]
            boost_name = f'boost_{game_boost}'
            boost_value = 1 if boost.is_active else 0
            boost_states[boost_name] = boost_value
        state[self.BOOST] = boost_states
            
        