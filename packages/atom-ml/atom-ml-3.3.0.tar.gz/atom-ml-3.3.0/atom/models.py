# -*- coding: utf-8 -*-

"""Automated Tool for Optimized Modelling (ATOM).

Author: tvdboom
Description: Module containing all the available models for the fit method
             of the ATOM class. All classes must have the following structure:

        Name
        ----
        Name of the model's class in camel case format.

        Attributes
        ----------
        name: string
            Short acronym of the model's longname for calling.

        longname: string
            Name of the model.

        Methods
        -------
        __init__(self, *args):
            Class initializer (contains super() to parent class).

        get_params(self, x):
            Return a dictionary of the model´s hyperparameters.

        get_model(self, params={}):
            Return the model object with unpacked parameters.

        get_domain(self):
            Return a list of the bounds for the hyperparameters.

        get_init_values(self):
            Return the default values of the model's hyperparameters.


To add a new model:
    1. Add the model's class to models.py
    2. Add the model to the list model_list in atom.py
    3. Add the name to all the relevant variables in atom.py and basemodel.py

"""

# << ============ Import Packages ============ >>

# Standard packages
import numpy as np
from .basemodel import BaseModel

# Sklearn models
from sklearn.gaussian_process import (
    GaussianProcessClassifier, GaussianProcessRegressor
    )
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import (
    LinearRegression, RidgeClassifier, Ridge as RidgeRegressor,
    Lasso as LassoRegressor, ElasticNet as ElasticNetRegressor,
    BayesianRidge, LogisticRegression as LR
    )
from sklearn.discriminant_analysis import (
    LinearDiscriminantAnalysis as LDA, QuadraticDiscriminantAnalysis as QDA
    )
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import (
    BaggingClassifier, BaggingRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor,
    RandomForestClassifier, RandomForestRegressor,
    AdaBoostClassifier, AdaBoostRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor
    )
from sklearn.svm import LinearSVC, LinearSVR, SVC, SVR
from sklearn.linear_model import (
    PassiveAggressiveClassifier as PAC, PassiveAggressiveRegressor as PAR,
    SGDClassifier, SGDRegressor
    )
from sklearn.neural_network import MLPClassifier, MLPRegressor


# << ============ Functions ============ >>

def set_init(class_, scaled=False):
    """Return BaseModel's (class) parameters as dictionary.

    Parameters
    ----------
    class_: class
        ATOM class.

    scaled: bool, optional (default=False)
        whether the model needs the features to be scaled.

    """
    try:  # Can fail if called from feature_selection
        # Create dict with data attributes
        if scaled and not class_._is_scaled:
            params = {'X_train': class_.X_train_scaled,
                      'X_test': class_.X_test_scaled}
        else:
            params = {'X_train': class_.X_train,
                      'X_test': class_.X_test}

        for attr in ('y_train', 'y_test'):
            params[attr] = getattr(class_, attr)

    except AttributeError:
        params = {}

    finally:
        params['T'] = class_  # ATOM or FeatureSelector class

    return params


# << ============ Classes ============ >>

class GaussianProcess(BaseModel):
    """Gaussian process model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'GP', 'Gaussian Process'

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return GaussianProcessClassifier(random_state=self.T.random_state,
                                             n_jobs=self.T.n_jobs)
        else:
            return GaussianProcessRegressor(random_state=self.T.random_state)


class GaussianNaïveBayes(BaseModel):
    """Gaussian Naïve Bayes model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'GNB', 'Gaussian Naïve Bayes'

    def get_model(self, params={}):
        """Call the model object."""
        return GaussianNB()


class MultinomialNaïveBayes(BaseModel):
    """Multinomial Naïve Bayes model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'MNB', 'Multinomial Naïve Bayes'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        prior = [True, False]
        params = {'alpha': round(x[0, 0], 2),
                  'fit_prior': prior[int(x[0, 1])]}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return MultinomialNB(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 5, 101)},
                {'name': 'fit_prior',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[1, 0]])


class BernoulliNaïveBayes(BaseModel):
    """Bernoulli Naïve Bayes model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'BNB', 'Bernoulli Naïve Bayes'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        prior = [True, False]
        params = {'alpha': round(x[0, 0], 2),
                  'fit_prior': prior[int(x[0, 1])]}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return BernoulliNB(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 5, 101)},
                {'name': 'fit_prior',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[1, 0]])


class OrdinaryLeastSquares(BaseModel):
    """Linear Regression without regularization (OLS)."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'OLS', 'Ordinary Least Squares'

    def get_model(self, params={}):
        """Call the model object."""
        return LinearRegression(n_jobs=self.T.n_jobs)


class Ridge(BaseModel):
    """Linear Regression/Classification with ridge regularization."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name = 'Ridge'
        if self.T.task != 'regression':
            self.longname = 'Ridge Classification'
        else:
            self.longname = 'Ridge Regression'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'max_iter': int(x[0, 0]),
                  'alpha': round(x[0, 1], 2)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return RidgeClassifier(random_state=self.T.random_state, **params)
        else:
            return RidgeRegressor(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        # alpha cannot be 0 for numerical reasons
        return [{'name': 'max_iter',
                 'type': 'discrete',
                 'domain': range(100, 1010, 10)},
                {'name': 'alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0.05, 5, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[500, 1.0]])


class Lasso(BaseModel):
    """Linear Regression with lasso regularization."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'Lasso', 'Lasso Regression'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'max_iter': int(x[0, 0]),
                  'alpha': round(x[0, 1], 2)}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return LassoRegressor(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        # alpha cannot be 0 for numerical reasons
        return [{'name': 'max_iter',
                 'type': 'discrete',
                 'domain': range(100, 1010, 10)},
                {'name': 'alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0.05, 5, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[500, 1.0]])


class ElasticNet(BaseModel):
    """Linear Regression with both lasso and ridge regularization."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'EN', 'ElasticNet Regression'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'max_iter': int(x[0, 0]),
                  'alpha': round(x[0, 1], 2),
                  'l1_ratio': round(x[0, 2], 2)}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return ElasticNetRegressor(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'max_iter',
                 'type': 'discrete',
                 'domain': range(100, 1010, 10)},
                {'name': 'alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0.05, 5, 100)},
                {'name': 'l1_ratio',
                 'type': 'discrete',
                 'domain': np.linspace(0.05, 0.95, 19)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[1000, 1.0, 0.5]])


class BayesianRegression(BaseModel):
    """Linear Bayesian Regression model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'BR', 'Bayesian Regression'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'n_iter': int(x[0, 0])}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return BayesianRidge(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_iter',
                 'type': 'discrete',
                 'domain': range(100, 1010, 10)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[300]])


class LogisticRegression(BaseModel):
    """Logistic Regression model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'LR', 'Logistic Regression'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        regularization = ['l2', 'none']
        class_weight = [None, 'balanced']
        params = {'max_iter': int(x[0, 0]),
                  'C': round(x[0, 1], 3),
                  'penalty': regularization[int(x[0, 2])],
                  'class_weight': class_weight[int(x[0, 3])]}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return LR(random_state=self.T.random_state,
                  n_jobs=self.T.n_jobs,
                  **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'max_iter',
                 'type': 'discrete',
                 'domain': range(100, 1010, 10)},
                {'name': 'C',
                 'type': 'discrete',
                 'domain': (1e-3, 0.01, 0.1, 1, 10, 100)},
                {'name': 'penalty',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'class_weight',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 1.0, 0, 0]])


class LinearDiscriminantAnalysis(BaseModel):
    """Linear Discriminant Analysis model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'LDA', 'Linear Discriminant Analysis'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        solver_types = ['svd', 'lsqr', 'eigen']
        solver = solver_types[int(x[0, 0])]
        params = {'solver': solver}

        if solver != 'svd':  # Add extra parameter: shrinkage
            params['shrinkage'] = round(x[0, 1], 1)

        return params

    def get_model(self, params={}):
        """Call the model object."""
        return LDA(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'solver',
                 'type': 'discrete',
                 'domain': range(3)},
                {'name': 'shrinkage',
                 'type': 'discrete',
                 'domain': np.linspace(0.0, 1.0, 11)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[0, 0]])


class QuadraticDiscriminantAnalysis(BaseModel):
    """Quadratic Discriminant Analysis model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'QDA', 'Quadratic Discriminant Analysis'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'reg_param': round(x[0, 0], 1)}
        return params

    def get_model(self, params={}):
        """Call the model object."""
        return QDA(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'reg_param',
                 'type': 'discrete',
                 'domain': np.linspace(0.0, 1.0, 11)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[0]])


class KNearestNeighbors(BaseModel):
    """K-Nearest Neighbors model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'KNN', 'K-Nearest Neighbors'

    @staticmethod
    def get_params(x):
        """Return a dictionary of the model´s hyperparameters."""
        weights = ['distance', 'uniform']
        params = {'n_neighbors': int(x[0, 0]),
                  'leaf_size': int(x[0, 1]),
                  'p': int(x[0, 2]),
                  'weights': weights[int(x[0, 3])]}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return KNeighborsClassifier(n_jobs=self.T.n_jobs, **params)
        else:
            return KNeighborsRegressor(n_jobs=self.T.n_jobs, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_neighbors',
                 'type': 'discrete',
                 'domain': range(1, 101)},
                {'name': 'leaf_size',
                 'type': 'discrete',
                 'domain': range(20, 41)},
                {'name': 'p',
                 'type': 'discrete',
                 'domain': range(1, 3)},
                {'name': 'weights',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[5, 30, 2, 1]])


class DecisionTree(BaseModel):
    """Single Decision Tree."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'Tree', 'Decision Tree'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        splitter = ['best', 'random']
        if self.T.task != 'regression':
            criterion = ['gini', 'entropy']
        else:
            criterion = ['mse', 'mae', 'friedman_mse']

        params = {'criterion': criterion[int(x[0, 0])],
                  'splitter': splitter[int(x[0, 1])],
                  'max_depth': int(x[0, 2]),
                  'max_features': round(x[0, 3], 1),
                  'min_samples_split': int(x[0, 4]),
                  'min_samples_leaf': int(x[0, 5]),
                  'ccp_alpha': round(x[0, 6], 3)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return DecisionTreeClassifier(random_state=self.T.random_state,
                                          **params)
        else:
            return DecisionTreeRegressor(random_state=self.T.random_state,
                                         **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'criterion',
                 'type': 'discrete',
                 'domain': range(2 if self.T.task != 'regression' else 3)},
                {'name': 'splitter',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(3, 11)},
                {'name': 'max_features',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'min_samples_split',
                 'type': 'discrete',
                 'domain': range(2, 21)},
                {'name': 'min_samples_leaf',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'ccp_alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 0.035, 8)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[0, 0, 10, 1.0, 2, 1, 0.0]])


class Bagging(BaseModel):
    """Bagging model (with decision tree as base estimator)."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name = 'Bag'
        if self.T.task != 'regression':
            self.longname = 'Bagging Classifier'
        else:
            self.longname = 'Bagging Regressor'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        bootstrap = [True, False]
        params = {'n_estimators': int(x[0, 0]),
                  'max_samples': round(x[0, 1], 1),
                  'max_features': round(x[0, 2], 1),
                  'bootstrap': bootstrap[int(x[0, 3])],
                  'bootstrap_features': bootstrap[int(x[0, 4])]}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return BaggingClassifier(random_state=self.T.random_state,
                                     n_jobs=self.T.n_jobs,
                                     **params)
        else:
            return BaggingRegressor(random_state=self.T.random_state,
                                    n_jobs=self.T.n_jobs,
                                    **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(10, 501)},
                {'name': 'max_samples',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'max_features',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'bootstrap',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'bootstrap_features',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[10, 1.0, 1.0, 0, 1]])


class ExtraTrees(BaseModel):
    """Extremely Randomized Trees."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'ET', 'Extra-Trees'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        bootstrap = [True, False]
        if self.T.task != 'regression':
            criterion = ['gini', 'entropy']
        else:
            criterion = ['mse', 'mae']

        params = {'n_estimators': int(x[0, 0]),
                  'max_depth': int(x[0, 1]),
                  'max_features': round(x[0, 2], 1),
                  'criterion': criterion[int(x[0, 3])],
                  'min_samples_split': int(x[0, 4]),
                  'min_samples_leaf': int(x[0, 5]),
                  'ccp_alpha': round(x[0, 6], 3),
                  'bootstrap': bootstrap[int(x[0, 7])]}

        if params['bootstrap']:
            params['max_samples'] = round(x[0, 8], 1)

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return ExtraTreesClassifier(random_state=self.T.random_state,
                                        n_jobs=self.T.n_jobs,
                                        **params)
        else:
            return ExtraTreesRegressor(random_state=self.T.random_state,
                                       n_jobs=self.T.n_jobs,
                                       **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(20, 501)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(3, 11)},
                {'name': 'max_features',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'criterion',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'min_samples_split',
                 'type': 'discrete',
                 'domain': range(2, 21)},
                {'name': 'min_samples_leaf',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'ccp_alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 0.035, 8)},
                {'name': 'bootstrap',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'max_samples',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 0.9, 5)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 10, 1.0, 0, 2, 1, 0.0, 1, 0.9]])


class RandomForest(BaseModel):
    """Random Forest model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'RF', 'Random Forest'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        bootstrap = [True, False]
        if self.T.task != 'regression':
            criterion = ['gini', 'entropy']
        else:
            criterion = ['mse', 'mae']

        params = {'n_estimators': int(x[0, 0]),
                  'max_depth': int(x[0, 1]),
                  'max_features': round(x[0, 2], 1),
                  'criterion': criterion[int(x[0, 3])],
                  'min_samples_split': int(x[0, 4]),
                  'min_samples_leaf': int(x[0, 5]),
                  'ccp_alpha': round(x[0, 6], 3),
                  'bootstrap': bootstrap[int(x[0, 7])]}

        if params['bootstrap']:
            params['max_samples'] = round(x[0, 8], 1)

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return RandomForestClassifier(random_state=self.T.random_state,
                                          n_jobs=self.T.n_jobs,
                                          **params)
        else:
            return RandomForestRegressor(random_state=self.T.random_state,
                                         n_jobs=self.T.n_jobs,
                                         **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(20, 501)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(3, 11)},
                {'name': 'max_features',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'criterion',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'min_samples_split',
                 'type': 'discrete',
                 'domain': range(2, 21)},
                {'name': 'min_samples_leaf',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'ccp_alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 0.035, 8)},
                {'name': 'bootstrap',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'max_samples',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 0.9, 5)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 10, 1.0, 0, 2, 1, 0.0, 0, 0.9]])


class AdaBoost(BaseModel):
    """Adaptive Boosting (with decision tree as base estimator)."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'AdaB', 'AdaBoost'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'n_estimators': int(x[0, 0]),
                  'learning_rate': round(x[0, 1], 2)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return AdaBoostClassifier(random_state=self.T.random_state,
                                      **params)
        else:
            return AdaBoostRegressor(random_state=self.T.random_state,
                                     **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(50, 501)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': np.linspace(0.01, 1, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[50, 1]])


class GradientBoostingMachine(BaseModel):
    """Gradient Boosting Machine model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=False))
        self.name, self.longname = 'GBM', 'Gradient Boosting Machine'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        criterion = ['friedman_mse', 'mae', 'mse']
        params = {'n_estimators': int(x[0, 0]),
                  'learning_rate': round(x[0, 1], 2),
                  'subsample': round(x[0, 2], 1),
                  'max_depth': int(x[0, 3]),
                  'max_features': round(x[0, 4], 1),
                  'criterion': criterion[int(x[0, 5])],
                  'min_samples_split': int(x[0, 6]),
                  'min_samples_leaf': int(x[0, 7]),
                  'ccp_alpha': round(x[0, 8], 3)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return GradientBoostingClassifier(random_state=self.T.random_state,
                                              **params)
        else:
            return GradientBoostingRegressor(random_state=self.T.random_state,
                                             **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(50, 501)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': (0.01, 1)},
                {'name': 'subsample',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(1, 11)},
                {'name': 'max_features',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'criterion',
                 'type': 'discrete',
                 'domain': range(3)},
                {'name': 'min_samples_split',
                 'type': 'discrete',
                 'domain': range(2, 21)},
                {'name': 'min_samples_leaf',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'ccp_alpha',
                 'type': 'discrete',
                 'domain': np.linspace(0, 0.035, 8)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 0.1, 1.0, 3, 1.0, 0, 2, 1, 0.0]])


class XGBoost(BaseModel):
    """Extreme Gradient Boosting."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'XGB', 'XGBoost'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'n_estimators': int(x[0, 0]),
                  'learning_rate': round(x[0, 1], 2),
                  'max_depth': int(x[0, 2]),
                  'gamma': round(x[0, 3], 2),
                  'min_child_weight': int(x[0, 4]),
                  'subsample': round(x[0, 5], 1),
                  'colsample_bytree': round(x[0, 6], 1),
                  'reg_alpha': round(x[0, 7], 3),
                  'reg_lambda': round(x[0, 8], 3)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        from xgboost import XGBClassifier, XGBRegressor
        # XGBoost can't handle random_state to be None
        rs = 0 if self.T.random_state is None else self.T.random_state
        if self.T.task != 'regression':
            return XGBClassifier(n_jobs=self.T.n_jobs,
                                 random_state=rs,
                                 verbosity=0,
                                 **params)
        else:
            return XGBRegressor(n_jobs=self.T.n_jobs,
                                random_state=rs,
                                verbosity=0,
                                **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(20, 501)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': np.linspace(0.01, 1, 100)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(1, 11)},
                {'name': 'gamma',
                 'type': 'discrete',
                 'domain': np.linspace(0, 1, 100)},
                {'name': 'min_child_weight',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'subsample',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'colsample_bytree',
                 'type': 'discrete',
                 'domain': np.linspace(0.3, 1.0, 8)},
                {'name': 'reg_alpha',
                 'type': 'discrete',
                 'domain': (0, 1e-3, 0.01, 0.1, 1, 10, 30, 100)},
                {'name': 'reg_lambda',
                 'type': 'discrete',
                 'domain': (0, 1e-3, 0.01, 0.1, 1, 10, 30, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 0.1, 3, 0.0, 1, 1.0, 1.0, 0, 1]])


class LightGBM(BaseModel):
    """Light Gradient Boosting Machine."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'LGB', 'LightGBM'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'n_estimators': int(x[0, 0]),
                  'learning_rate': round(x[0, 1], 2),
                  'max_depth': int(x[0, 2]),
                  'num_leaves': int(x[0, 3]),
                  'min_child_weight': int(x[0, 4]),
                  'min_child_samples': int(x[0, 5]),
                  'subsample': round(x[0, 6], 1),
                  'colsample_bytree': round(x[0, 7], 1),
                  'reg_alpha': round(x[0, 8], 3),
                  'reg_lambda': round(x[0, 9], 3)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        from lightgbm.sklearn import LGBMClassifier, LGBMRegressor
        if self.T.task != 'regression':
            return LGBMClassifier(n_jobs=self.T.n_jobs,
                                  random_state=self.T.random_state,
                                  **params)
        else:
            return LGBMRegressor(n_jobs=self.T.n_jobs,
                                 random_state=self.T.random_state,
                                 **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(20, 501)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': np.linspace(0.01, 1, 100)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(1, 11)},
                {'name': 'num_leaves',
                 'type': 'discrete',
                 'domain': range(20, 41)},
                {'name': 'min_child_weight',
                 'type': 'discrete',
                 'domain': range(1, 21)},
                {'name': 'min_child_samples',
                 'type': 'discrete',
                 'domain': range(10, 31)},
                {'name': 'subsample',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'colsample_bytree',
                 'type': 'discrete',
                 'domain': np.linspace(0.3, 1.0, 8)},
                {'name': 'reg_alpha',
                 'type': 'discrete',
                 'domain': (0, 1e-3, 0.01, 0.1, 1, 10, 30, 100)},
                {'name': 'reg_lambda',
                 'type': 'discrete',
                 'domain': (0, 1e-3, 0.01, 0.1, 1, 10, 30, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 0.1, 3, 31, 1, 20, 1.0, 1.0, 0, 0]])


class CatBoost(BaseModel):
    """Categorical Boosting Machine."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'CatB', 'CatBoost'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        params = {'n_estimators': int(x[0, 0]),
                  'learning_rate': round(x[0, 1], 2),
                  'max_depth': int(x[0, 2]),
                  'subsample': round(x[0, 3], 1),
                  'colsample_bylevel': round(x[0, 4], 1),
                  'reg_lambda': round(x[0, 5], 3)}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        from catboost import CatBoostClassifier, CatBoostRegressor
        if self.T.task != 'regression':
            # subsample only works when bootstrap_type=Bernoulli
            return CatBoostClassifier(bootstrap_type='Bernoulli',
                                      train_dir='',
                                      allow_writing_files=False,
                                      random_state=self.T.random_state,
                                      verbose=False,
                                      **params)
        else:
            return CatBoostRegressor(train_dir='',
                                     allow_writing_files=False,
                                     random_state=self.T.random_state,
                                     verbose=False,
                                     **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        # num_leaves and min_child_samples not availbale for CPU implementation
        return [{'name': 'n_estimators',
                 'type': 'discrete',
                 'domain': range(20, 501)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': np.linspace(0.01, 1, 100)},
                {'name': 'max_depth',
                 'type': 'discrete',
                 'domain': range(1, 11)},
                {'name': 'subsample',
                 'type': 'discrete',
                 'domain': np.linspace(0.5, 1.0, 6)},
                {'name': 'colsample_bylevel',
                 'type': 'discrete',
                 'domain': np.linspace(0.3, 1.0, 8)},
                {'name': 'reg_lambda',
                 'type': 'discrete',
                 'domain': (0, 1e-3, 0.01, 0.1, 1, 10, 30, 100)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[100, 0.1, 3, 1.0, 1.0, 0]])


class LinearSVM(BaseModel):
    """Linear Support Vector Machine."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'lSVM', 'Linear SVM'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        if self.T.task != 'regression':
            losses = ['hinge', 'squared_hinge']
        else:
            losses = ['epsilon_insensitive', 'squared_epsilon_insensitive']
        loss = losses[int(x[0, 1])]
        penalties = ['l1', 'l2']

        # l1 regularization can't be combined with hinge
        penalty = penalties[int(x[0, 2])] if loss == 'squared_hinge' else 'l2'

        # l1 regularization can't be combined with squared_hinge when dual=True
        dual = True if penalty == 'l2' else False

        params = {'C': round(x[0, 0], 3),
                  'loss': loss,
                  'dual': dual}

        if self.T.task != 'regression':
            params['penalty'] = penalty

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return LinearSVC(random_state=self.T.random_state, **params)
        else:
            return LinearSVR(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'C',
                 'type': 'discrete',
                 'domain': (1e-3, 0.01, 0.1, 1, 10, 100)},
                {'name': 'loss',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'penalty',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[1, 1, 1]])


class KernelSVM(BaseModel):
    """Kernel (non-linear) Support Vector Machine."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'kSVM', 'Kernel SVM'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        kernels = ['poly', 'rbf', 'sigmoid']
        kernel = kernels[int(x[0, 4])]
        gamma = ['auto', 'scale']
        shrinking = [True, False]

        params = {'C': round(x[0, 0], 3),
                  'degree': int(x[0, 1]),
                  'gamma': gamma[int(x[0, 2])],
                  'kernel': kernel,
                  'shrinking': shrinking[int(x[0, 5])]}

        if kernel != 'rbf':
            params['coef0'] = round(x[0, 3], 2)

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return SVC(random_state=self.T.random_state, **params)
        else:
            return SVR(**params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'C',
                 'type': 'discrete',
                 'domain': (1e-3, 0.01, 0.1, 1, 10, 100)},
                {'name': 'degree',
                 'type': 'discrete',
                 'domain': range(2, 6)},
                {'name': 'gamma',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'coef0',
                 'type': 'discrete',
                 'domain': np.linspace(-1.0, 1.0, 201)},
                {'name': 'kernel',
                 'type': 'discrete',
                 'domain': range(3)},
                {'name': 'shrinking',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[1, 3, 0, 0, 1, 0]])


class PassiveAggressive(BaseModel):
    """Passive Aggressive model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'PA', 'Passive Aggressive'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        if self.T.task != 'regression':
            loss = ['hinge', 'squared_hinge']
        else:
            loss = ['epsilon_insensitive', 'squared_epsilon_insensitive']
        average = [True, False]

        params = {'loss': loss[int(x[0, 0])],
                  'C': round(x[0, 1], 3),
                  'average': average[int(x[0, 2])]}

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return PAC(random_state=self.T.random_state,
                       n_jobs=self.T.n_jobs,
                       **params)
        else:
            return PAR(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'loss',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'C',
                 'type': 'discrete',
                 'domain': (1e-3, 0.01, 0.1, 1, 10, 100)},
                {'name': 'average',
                 'type': 'discrete',
                 'domain': range(2)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[0, 1, 1]])


class StochasticGradientDescent(BaseModel):
    """Stochastic Gradient Descent model."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'SGD', 'Stochastic Gradient Descent'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        if self.T.task != 'regression':
            loss = ['hinge', 'log', 'modified_huber', 'squared_hinge',
                    'perceptron', 'squared_loss', 'huber',
                    'epsilon_insensitive', 'squared_epsilon_insensitive']
        else:
            loss = ['squared_loss', 'huber',
                    'epsilon_insensitive', 'squared_epsilon_insensitive']

        penalties = ['none', 'l1', 'l2', 'elasticnet']
        penalty = penalties[int(x[0, 1])]

        average = [True, False]
        lr = ['constant', 'invscaling', 'optimal', 'adaptive']

        params = {'loss': loss[int(x[0, 0])],
                  'penalty': penalty,
                  'alpha': round(x[0, 2], 4),
                  'average': average[int(x[0, 3])],
                  'epsilon': round(x[0, 4], 4),
                  'learning_rate': lr[int(x[0, 6])],
                  'power_t': round(x[0, 8], 2)}

        if penalty == 'elasticnet':
            params['l1_ratio'] = round(x[0, 7], 2)

        if lr != 'optimal':
            params['eta0'] = round(x[0, 5], 4)

        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return SGDClassifier(random_state=self.T.random_state,
                                 n_jobs=self.T.n_jobs,
                                 **params)
        else:
            return SGDRegressor(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'loss',
                 'type': 'discrete',
                 'domain': range(9 if self.T.task != 'regression' else 4)},
                {'name': 'penalty',
                 'type': 'discrete',
                 'domain': range(4)},
                {'name': 'alpha',
                 'type': 'discrete',
                 'domain': (1e-4, 1e-3, 0.01, 0.1, 1)},
                {'name': 'average',
                 'type': 'discrete',
                 'domain': range(2)},
                {'name': 'epsilon',
                 'type': 'discrete',
                 'domain': (1e-4, 1e-3, 0.01, 0.1, 1)},
                {'name': 'eta0',
                 'type': 'discrete',
                 'domain': (1e-4, 1e-3, 0.01, 0.1, 1)},
                {'name': 'learning_rate',
                 'type': 'discrete',
                 'domain': range(4)},
                {'name': 'l1_ratio',
                 'type': 'discrete',
                 'domain': np.linspace(0.1, 0.9, 17)},
                {'name': 'power_t',
                 'type': 'discrete',
                 'domain': np.linspace(0.05, 1, 20)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[0, 2, 1e-4, 1, 0.1, 0.01, 2, 0.15, 0.25]])


class MultilayerPerceptron(BaseModel):
    """Multilayer Perceptron with 1 to 3 hidden layers."""

    def __init__(self, *args):
        """Class initializer (contains super() to parent class)."""
        super().__init__(**set_init(*args, scaled=True))
        self.name, self.longname = 'MLP', 'Multilayer Perceptron'

    def get_params(self, x):
        """Return a dictionary of the model´s hyperparameters."""
        # Set the number of neurons per layer
        n1, n2, n3 = int(x[0, 0]), int(x[0, 1]), int(x[0, 2])
        if n2 == 0:
            layers = (n1,)
        elif n3 == 0:
            layers = (n1, n2)
        else:
            layers = (n1, n2, n3)

        params = {'hidden_layer_sizes': layers,
                  'alpha': round(x[0, 3], 4),
                  'learning_rate_init': round(x[0, 4], 3),
                  'max_iter': int(x[0, 5]),
                  'batch_size': int(x[0, 6])}
        return params

    def get_model(self, params={}):
        """Return the model object with unpacked parameters."""
        if self.T.task != 'regression':
            return MLPClassifier(random_state=self.T.random_state, **params)
        else:
            return MLPRegressor(random_state=self.T.random_state, **params)

    def get_domain(self):
        """Return a list of the bounds for the hyperparameters."""
        return [{'name': 'hidden_layer_1',
                 'type': 'discrete',
                 'domain': range(10, 101)},
                {'name': 'hidden_layer_2',
                 'type': 'discrete',
                 'domain': range(101)},
                {'name': 'hidden_layer_3',
                 'type': 'discrete',
                 'domain': range(101)},
                {'name': 'alpha',
                 'type': 'discrete',
                 'domain': (1e-4, 1e-3, 0.01, 0.1)},
                {'name': 'learning_rate_init',
                 'type': 'discrete',
                 'domain': np.linspace(0.001, 0.1, 101)},
                {'name': 'max_iter',
                 'type': 'discrete',
                 'domain': range(100, 510, 10)},
                {'name': 'batch_size',
                 'type': 'discrete',
                 'domain': (1, 8, 32, 64)}]

    def get_init_values(self):
        """Return the default values of the model's hyperparameters."""
        return np.array([[20, 0, 0, 1e-4, 1e-3, 200, 32]])


# << ============ Global variables ============ >>

# List of all the available models
model_list = dict(GP=GaussianProcess,
                  GNB=GaussianNaïveBayes,
                  MNB=MultinomialNaïveBayes,
                  BNB=BernoulliNaïveBayes,
                  OLS=OrdinaryLeastSquares,
                  Ridge=Ridge,
                  Lasso=Lasso,
                  EN=ElasticNet,
                  BR=BayesianRegression,
                  LR=LogisticRegression,
                  LDA=LinearDiscriminantAnalysis,
                  QDA=QuadraticDiscriminantAnalysis,
                  KNN=KNearestNeighbors,
                  Tree=DecisionTree,
                  Bag=Bagging,
                  ET=ExtraTrees,
                  RF=RandomForest,
                  AdaB=AdaBoost,
                  GBM=GradientBoostingMachine,
                  XGB=XGBoost,
                  LGB=LightGBM,
                  CatB=CatBoost,
                  lSVM=LinearSVM,
                  kSVM=KernelSVM,
                  PA=PassiveAggressive,
                  SGD=StochasticGradientDescent,
                  MLP=MultilayerPerceptron)
