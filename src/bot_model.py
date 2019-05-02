class BotModel:

	BASE_PATH = 'C:/Users/Frank\'s Laptop/Desktop/Programming/Python/ImitationBot/src/models/'
	MODEL_PATH = f'{BASE_PATH}'
	WEIGHTS_PATH = f'{BASE_PATH}'

	def __init__(self, input_num = 0, output_num = 0, layers = []):
		self.input_num = input_num
		self.output_num = output_num
		self.layers = layers
		self.activation = 'tanh'
		self.model = None

	def compile_model(self, model):
		pass

	def get_name(self):
		pass

	def get_model_path(self):
		return f'{self.MODEL_PATH}{self.get_name()}.json'

	def get_model_weights(self):
		return f'{self.WEIGHTS_PATH}{self.get_name()}.h5'

	def get_model(self):
		if self.model is None:
			from keras.models import Sequential
			from keras.layers import Dense
			
			model = Sequential()
			model.add(Dense(self.layers[0], input_dim=self.input_num, activation=self.activation))
			for layer in self.layers[1:]:
				model.add(Dense(layer, activation=self.activation))
			model.add(Dense(self.output_num, activation=self.activation))
			model = self.compile_model(model)
			self.model = model
		return self.model

	def save_model_to_file(self):
		# serialize model to JSON
		model = self.model
		model_json = model.to_json()
		with open(self.get_model_path(), "w+") as json_file:
			json_file.write(model_json)
		# serialize weights to HDF5
		model.save_weights(self.get_model_weights())
		print(f"Saved model to {self.get_model_path()} and weights to {self.get_model_weights()}")

	def load_model_from_json(self):
		from keras.models import model_from_json
		with open(self.get_model_path(), 'r') as json_file:
			loaded_model_json = json_file.read()

		loaded_model = model_from_json(loaded_model_json)
		loaded_model.load_weights(self.get_model_weights())
		loaded_model = self.compile_model(loaded_model)
		return loaded_model
