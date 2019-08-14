from simple_nn_bot import SimpleNNRLBot
import bot_models


class AdadeltaBot(SimpleNNRLBot):

    def load_model(self):
        return bot_models.AdadeltaModel().load_model_from_json()
