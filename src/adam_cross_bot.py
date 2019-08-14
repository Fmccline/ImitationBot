from simple_nn_bot import SimpleNNRLBot
import bot_models


class AdamBot(SimpleNNRLBot):

    def load_model(self):
        return bot_models.AdamCrossModel().load_model_from_json()