import numpy as np
import math

from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from keras import Sequential
from keras.src.layers import LSTM, Dense

class Lstm:
    def __init__(self, sequence_length=30, epochs=10, batch_size=32):
        self.sequence_length = sequence_length
        self.epochs = epochs
        self.batch_size = batch_size
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        self.model = None

    def preprocess(self, data):
        scaled_data = self.scaler.fit_transform(data)
        feature, target = self.__create_sequence(scaled_data, seq_length=self.sequence_length)
        return np.array(feature), np.array(target)

    def build_train_predict(self, feature, target):
        x_feature, x_test, y_feature, y_test = train_test_split(feature, target, test_size=0.2, shuffle=False)
        print(x_feature)
        print(y_feature)
        input_shape = (feature[0].shape[0], feature[0].shape[1])
        model = self.__build_model(input_shape)
        model.fit(x_feature, y_feature, epochs=self.epochs, batch_size=self.batch_size, verbose=1)
        predictions = model.predict(x_test)
        predictions = self.scaler.inverse_transform(predictions)
        y_test = self.scaler.inverse_transform(y_test)
        stats = self.__stats(y_test, predictions)
        return predictions, stats

    @staticmethod
    def __build_model(input_shape):
        model = Sequential()
        model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
        model.add(LSTM(units=50))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mean_squared_error')
        return model

    @staticmethod
    def __create_sequence(data, seq_length):
        feature, target = [], []
        for i in range(len(data) - seq_length):
            feature.append(data[i:i + seq_length])
            target.append(data[i + seq_length])
        return feature, target

    @staticmethod
    def __stats(true, predicted):
        rmse = math.sqrt(mean_squared_error(true, predicted))
        mse = mean_squared_error(true, predicted)
        mae = mean_absolute_error(true, predicted)
        mape = mean_absolute_percentage_error(true, predicted)
        stats = {'MSE': mse, 'RMSE': rmse, 'MAE': mae, 'MAPE': mape}
        return stats