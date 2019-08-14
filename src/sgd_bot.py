from simple_nn_bot import SimpleNNRLBot
import bot_models


class SGDBot(SimpleNNRLBot):

    def load_model(self):
        return bot_models.SGDModel().load_model_from_json()
