from keras.models import Sequential
from keras.layers import Dense
import numpy as np
from sklearn.model_selection import train_test_split

X = 'x'
Y = 'y'


def main():
    filename = 'csv/2019-04-21_2019-04-22-trajectories.csv'
    print(f"Loading data from {filename}")
    train_data, test_data = get_input_output_data(filename)
    print("Created X and Y training data")
    model = get_model()
    batch_size = 50
    epochs = 10
    model.fit(train_data[X], train_data[Y], epochs=epochs, batch_size=batch_size)
    print(f"Evaluating the model with batch size {batch_size} over {epochs} epochs")
    scores = model.evaluate(test_data[X], test_data[Y])
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    save_model_to_file(model, "models/model.json", "models/model.h5")
    total_predictions = 10
    x_data = test_data[X][:total_predictions, :]
    prediction = model.predict(x_data)
    print(f'\n*****Predictions are\n{prediction}\n*****')


def get_input_output_data(filename):
    dataset = np.loadtxt(filename, delimiter=",", skiprows=1)
    Y_data = dataset[:, 72:80]
    X_data = get_x_data(dataset)
    X_train, X_test, Y_train, Y_test = train_test_split(X_data, Y_data, test_size=0.15)
    return {X: X_train, Y: Y_train}, {X: X_test, Y: Y_test}


def get_x_data(dataset):
    skipped_data = [1]
    x0 = dataset[:, 0:1]
    x1 = dataset[:, 2:11]
    x2 = dataset[:, 41:47]
    rows = dataset.shape[0]
    X_data = np.zeros((rows, x0.shape[1] + x1.shape[1] + x2.shape[1]))
    for row_index in range(rows):
        column_index = 0
        for column in range(x0.shape[1]):
            X_data[row_index, column_index] = x0[row_index, column]
            column_index += 1
        for column in range(x1.shape[1]):
            X_data[row_index, column_index] = x1[row_index, column]
            column_index += 1
        for column in range(x2.shape[1]):
            X_data[row_index, column_index] = x2[row_index, column]
            column_index += 1
    return X_data


def get_model():
    model = Sequential()
    model.add(Dense(16, input_dim=16, activation='tanh'))
    # model.add(Dense(32, activation='tanh'))
    model.add(Dense(8, activation='tanh'))
    model.compile(optimizer ='sgd', loss='mean_absolute_error', metrics=['accuracy'])
    return model


def save_model_to_file(model, model_path, weight_path):
    # serialize model to JSON
    model_json = model.to_json()
    with open(model_path, "w+") as json_file:
        json_file.write(model_json)
    # serialize weights to HDF5
    model.save_weights(weight_path)
    print(f"Saved model to {model_path} and weights to {weight_path}")


if __name__ == '__main__':
    main()
