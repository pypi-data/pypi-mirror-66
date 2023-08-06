nextstep.model subpackage
==========================

base\_model
---------------------------------

.. automodule:: nextstep.model.base_model
   :members:
   :undoc-members:
   :show-inheritance:

XGboost
-----------------------------

.. automodule:: nextstep.model.XGboost
   :members:
   :undoc-members:
   :show-inheritance:

adaboost
------------------------------

.. automodule:: nextstep.model.adaboost
   :members:
   :undoc-members:
   :show-inheritance:

example config
::   

   user_config = {
      'label_column' : 'USEP', # label column name
      'train_size' : 0.9, # train-test split
      'seed' : 33, 
      'base_estimator': random_forest_model, # a fitted model
      'n_estimators' : 10, # number of estimators
      'learning_rate' : 1, # learning rate
      'loss' : 'square' # loss function
      } 

arima
---------------------------

.. automodule:: nextstep.model.arima
   :members:
   :undoc-members:
   :show-inheritance:


lstm
--------------------------

.. automodule:: nextstep.model.lstm
   :members:
   :undoc-members:
   :show-inheritance:

random\_forest
------------------------------------

.. automodule:: nextstep.model.random_forest
   :members:
   :undoc-members:
   :show-inheritance:

sarima
----------------------------

.. automodule:: nextstep.model.sarima
   :members:
   :undoc-members:
   :show-inheritance:
