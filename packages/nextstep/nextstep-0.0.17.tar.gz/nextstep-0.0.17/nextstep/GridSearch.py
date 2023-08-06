import pandas as pd 
import numpy as np
import itertools

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.model_selection import cross_validate

from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error, mean_absolute_error
import xgboost as xgb
from sklearn.ensemble import RandomForestRegressor
import statsmodels.api as sm
import statsmodels


# can change the print statement to return statement,
# depends on how do we want to put everything together 

def GridSearch(model_name, x, y):
    """utlising GridSearch to detect the best set of parameters for the desired model.

    :param model_name: name of the model
    :type model_name: string name of the desired model (ARIMA, SARIMA, Random Forest, XGboost)
    :param x: Xarray-like or sparse matrix of shape (n_samples, n_features).
    :type x: pandas dataframe
    :param y: The target values (real numbers in regression)
    :type y: Array-like of shape (n_samples,) or (n_samples, n_outputs)
    :return: a list [best_score, best_param]
    """

    if model_name == 'SARIMA':
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p,d,q))
        seasonal_pdq = [(x[0], x[1], x[2], 48) for x in list(itertools.product(p, d, q))]
        
        dic = dict()
        RMSE = []
        
        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(y,
                                                   order=param,
                                                   seasonal_order=param_seasonal,
                                                   enforce_stationary=False,
                                                   enforce_invertibility=False)
                    
                    results = mod.fit()
                    
                    
                    rmse = np.sqrt(mean_squared_error(y, results.fittedvalues))
                    mae = mean_absolute_error(y, results.fittedvalues)
                    
                    dic[str(rmse)] = [param, param_seasonal]
                    RMSE.append(rmse)
                
                except:
                    continue
                    
        print("MIN RMSE: {}, with ARIMA{}x{}48".format(min(RMSE), dic[str(min(RMSE))][0], dic[str(min(RMSE))][1]))
        
        return [min(RMSE), dic[str(min(RMSE))][0], dic[str(min(RMSE))][1]]   
                                                   
                    
    
    elif model_name == 'ARIMA':
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p,d,q))
        
        dic = dict()
        RMSE = []
        for param in pdq:
            try:
                mod = statsmodels.tsa.arima_model.ARIMA(y,
                                               order=param
                                                       )

                results = mod.fit()
                rmse = np.sqrt(mean_squared_error(y, results.fittedvalues))
                mae = mean_absolute_error(y, results.fittedvalues)

                dic[str(rmse)] = param
                RMSE.append(rmse)
            
            except:
                continue

        print("MIN RMSE: {}, with SARIMA{}".format(min(RMSE), dic[str(min(RMSE))]))
        return [min(RMSE), dic[str(min(RMSE))]]         
                                    
        
    elif model_name == 'Random Forest':
        model = RandomForestRegressor()

        parameters = {
          'criterion':['mse'],
          'max_depth': [5, 20, 60],
          'min_samples_leaf': [1, 5, 10],
          'max_features': [20, 70, 100],
          'bootstrap': [True, False],
          'n_estimators': [15, 20, 40]
        
        }
            
        grid = GridSearchCV(model,
                            parameters,
                            scoring = 'neg_mean_squared_error',
                            cv = 4,
                            n_jobs = -1,
                            verbose=True)

        grid.fit(x, y)
        print(np.sqrt(abs(grid.best_score_)))
        print(grid.best_params_)
        return [np.sqrt(abs(grid.best_score_)), grid.best_params_]
    
    elif model_name == 'XGboost':
        model = xgb.XGBRegressor()

        parameters = {#'nthread':[4], #when use hyperthread, xgboost may become slower
          'objective':['reg:linear'],
          'learning_rate': [0.05, 0.07, 0.1], #so called `eta` value
          'max_depth': [5, 20, 60],
          'min_child_weight': [1, 4, 7],
          'silent': [1],
          'subsample': [0.7],
          'colsample_bytree': [0.7],
          'n_estimators': [15, 20, 40]}
            
        grid = GridSearchCV(model,
                            parameters,
                            scoring = 'neg_mean_squared_error',
                            cv = 4,
                            n_jobs = -1,
                            verbose=True)

        grid.fit(x, y)
        print(np.sqrt(abs(grid.best_score_)))
        print(grid.best_params_)
        return [np.sqrt(abs(grid.best_score_)), grid.best_params_]


        
    else:
        print("Please enter the correct model name (ARIMA, SARIMA, Random Forest or XGboost)")
        
