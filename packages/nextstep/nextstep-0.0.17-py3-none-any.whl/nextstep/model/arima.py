from statsmodels.tsa.arima_model import ARIMA
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_pacf
from nextstep.model.base_model import base_model
import pandas as pd
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")


class arima(base_model):
    """arima class."""
    def __init__(self, config):
        """constructor method

        :param config: configuration for adaboost model
        :type config: python dictionary
        """
        super().__init__()
        self._config = config
        self._model = None
    
    def build_model(self, data):
        """building the arima model, including train-test split and model evaluation.

        :param data: dataset
        :type data: pandas dataframe
        :return: fitted adaboost model
        """
        print('Building arima model.')

        size = int(len(data) * self._config['train_size'])
        data = data[self._config['label_column']].values
        train, test = data[:size].tolist(), data[size:]

        model = ARIMA(train,
                        order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
        fitted_model = model.fit()
        
        predictions = fitted_model.forecast(steps = len(test))[0]
        
        print('Evaluating arima performance.')
        self.evaluation(test, predictions)

        model = ARIMA(data,
                      order=(self._config['lag'], self._config['differencing'], self._config['window_size']))
        model_fitted = model.fit()
        self._model = model_fitted
        return model
    
    def predict_next_n(self, step):
        """use fitted module for prediction.

        :param step: the number of values to be predicted
        :type X_new: int
        """
        return self._model.forecast(steps = step)[0]

    def autocorrelation(self, data, number_of_time_step = 20):
        """plot autocorrelation.

        :param data: dataset
        :type data: pandas dataframe
        :param number_of_time_step: number of time step needs to be considered for autocorrelation
        :type number_of_time_step: int, default to be 20

        .. note::
            data length must be larger than specified number_of_time_step.
        """
        print("Autocorrelation")
        try:
            autocorrelation_plot(data[self._config['label_column']][:number_of_time_step])
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter number of time step. to be below 20.')
        return None
    
    def partial_autocorrelation(self, data, lags = 20):
        """plot partial autocorrelation.

        :param data: dataset
        :type data: pandas dataframe
        :param lags: number of lags needs to be considered for partial autocorrelation
        :type lags: int, default to be 20

        .. note::
            data length must be larger than specified lags.
        """
        print("Partial Autocorrelation")
        try:
            plot_pacf(data[self._config['label_column']], lags = lags)
            pyplot.show()
        except:
            print('Data time step is below 20, please specify paramter lags to be below 20.')
        return None
    
    def residual_plot(self):
        """plot residual.
        """
        print("Residual Plot")
        df = pd.DataFrame(self._model.resid)
        df.plot()
        df.plot(kind='kde')
        pyplot.show()
        print("residual mean is {}".format(sum(self._model.resid)/len(self._model.resid)))
        return None
    
    def residual_density_plot(self):
        """plot residual density plot.
        """
        print("Residual Density Plot")
        pd.DataFrame(self._model.resid).plot(kind='kde')
        pyplot.show()
        return None        
        
    
    
