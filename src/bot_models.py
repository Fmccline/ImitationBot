from bot_model import BotModel


class AdadeltaModel(BotModel):
	
	def get_name(self):
		return 'Adadelta'

	def compile_model(self, model):
		from keras import optimizers
		adadelta = optimizers.Adadelta(lr=0.75)
		model.compile(optimizer=adadelta, loss='binary_crossentropy', metrics=['accuracy'])
		return model


class SGDModel(BotModel):

	def get_name(self):
		return 'SGD'

	def compile_model(self, model):
		from keras import optimizers
		sgd = optimizers.SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
		model.compile(optimizer=sgd, loss='mean_squared_error', metrics=['accuracy'])
		return model