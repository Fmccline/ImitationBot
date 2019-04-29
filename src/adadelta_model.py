from bot_model import BotModel


class AdadeltaModel(BotModel):
	
	def get_name(self):
		return 'AdadeltaModel'

	def compile_model(self, model):
		model.compile(optimizer ='adadelta', loss='mean_squared_error', metrics=['accuracy'])
		return model
