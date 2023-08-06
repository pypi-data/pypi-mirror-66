from sklearn.ensemble import AdaBoostRegressor
from nextstep.model.base_model import base_model


class adaboost(base_model):
    """adaboost class
    """
    def __init__(self, config):
        """constructor method

        :param config: configuration for adaboost model
        :type config: python dictionary
        """
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        """building the adaboost model, including train-test split and model evaluation.

        :param data: dataset
        :type data: pandas dataframe
        :return: fitted adaboost model
        """
        print('Building adaboost model.')
        model = AdaBoostRegressor(base_estimator = self._config['base_estimator'],
                                  n_estimators = self._config['n_estimators'],
                                  learning_rate = self._config['learning_rate'],
                                  loss = self._config['loss'],
                                  random_state = self._config['seed'])
        self._model = model
        
        X_train, X_test, y_train, y_test = self.split(data,
                                                      self._config['label_column'],
                                                      self._config['train_size'],
                                                      self._config['seed'])
        
        self._model.fit(X_train, y_train)
        y_predicted = self._model.predict(X_test)

        print('Evaluating adaboost performance.')
        self.evaluation(y_test, y_predicted)
        return model
    
    def predict(self, X_new):
        '''use fitted module for prediction.

        :param X_new: data of shape (n_samples, n_features)
        :type X_new: array-like
        '''
        return self._model.predict(X_new)
    
    
