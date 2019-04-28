from bot_model import BotModel


class AdadeltaModel(BotModel):
	
	def __init__(self, input_num, output_num, layers):
		super().__init__(input_num, output_num, layers)
		self.name = 'AdadeltaModel'

	def compile_model(self, model):
		model.compile(optimizer ='adadelta', loss='mean_squared_error', metrics=['accuracy'])
		return model
