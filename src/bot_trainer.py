import numpy as np
from sklearn.model_selection import train_test_split
from adadelta_model import AdadeltaModel

X = 'x'
Y = 'y'


def main():
    filename = 'csv/2019-04-21_2019-04-22-trajectories.csv'
    print(f"Loading data from {filename}")
    train_data, test_data = get_input_output_data(filename)
    print("Created X and Y training data")
    adadelta_model = AdadeltaModel(16, 8, [32, 16, 8])
    model = adadelta_model.model
    batch_size = 50
    epochs = 5
    model.fit(train_data[X], train_data[Y], epochs=epochs, batch_size=batch_size)
    print(f"Evaluating the model with batch size {batch_size} over {epochs} epochs")
    scores = model.evaluate(test_data[X], test_data[Y])
    print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))
    adadelta_model.save_model_to_file()
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


if __name__ == '__main__':
    main()
