from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np

class base_model:
    """base model class"""
    def __init__(self):
        """constructor method"""
    def split(self, data, label_column, train_size, seed):
        """perform train test split.
        
        :param data: dataset
        :type data: pandas dataframe
        :param label_column: label column name
        :type label_column: string
        :param train_size: training size as a ratio over entire data size
        :param seed: pseudorandom number generator initializing value, if you provide same seed value before generating random data it will produce the same data
        :type seed: int
        """
        y = data[label_column]
        X = data.drop(label_column, axis = 1)
        X_train,X_test,y_train,y_test = train_test_split(X, y, train_size=train_size, random_state=seed)
        return X_train, X_test, y_train, y_test

    def split_noshuffle(self, data, label_column, train_size, seed):
        """perform train test split in the non-shuffle manner.
        
        :param data: dataset
        :type data: pandas dataframe
        :param label_column: label column name
        :type label_column: string
        :param train_size: training size as a ratio over entire data size
        :param seed: pseudorandom number generator initializing value, if you provide same seed value before generating random data it will produce the same data
        :type seed: int
        """
        y = data[label_column]
        X = data.drop(label_column, axis = 1)
        X_train,X_test,y_train,y_test = train_test_split(X, y, train_size=train_size, random_state=seed, shuffle=False)
        return X_train, X_test, y_train, y_test
    
    def evaluation(self, y_pre, y_true):
        """model evaluation method. Metrics include MAE, MSE and RMSE
        
        :param y_pre: predicted values
        :type y_pre: array-like, such as python list
        :param y_true: true values
        :type y_true: array-like, such as python list        
        """
        print("MAE : {}".format(metrics.mean_absolute_error(y_true, y_pre)))
        print("MSE : {}".format(metrics.mean_squared_error(y_true, y_pre)))
        print("RMSE : {}".format(np.sqrt(metrics.mean_squared_error(y_true, y_pre))))
        return None
