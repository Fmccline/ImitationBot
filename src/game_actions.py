class GameActions:
    THROTTLE = 'throttle'
    STEER = 'steer'
    PITCH = 'pitch'
    YAW = 'yaw'
    ROLL = 'roll'
    JUMP = 'jump'
    BOOST = 'boost'
    HANDBRAKE = 'handbrake'

    @staticmethod
    def get_actions(controller):
        actions = {}
        actions[GameActions.THROTTLE] = controller.throttle
        actions[GameActions.STEER] = controller.steer
        actions[GameActions.PITCH] = controller.pitch
        actions[GameActions.YAW] = controller.yaw
        actions[GameActions.ROLL] = controller.roll
        actions[GameActions.JUMP] = controller.jump
        actions[GameActions.BOOST] = controller.boost
        actions[GameActions.HANDBRAKE] = controller.handbrake
        return actions
