# -*- coding: utf-8 -*-

"""Automated Tool for Optimized Modelling (ATOM).

Author: tvdboom
Description: Module containing utility functions.

"""


# << ============ Import Packages ============ >>

# Standard packages
import logging
import numpy as np
import pandas as pd
from time import time
from datetime import datetime
from typing import Union, Sequence


# << ============ Global variables ============ >>

# Variable types
cal = Union[str, callable]
scalar = Union[int, float]
X_types = Union[dict, Sequence[Sequence], np.ndarray, pd.DataFrame]
y_types = Union[int, str, list, tuple, dict, np.ndarray, pd.Series]
train_types = Union[Sequence[scalar], np.ndarray]

# Tuple of models that need to import an extra package
optional_packages = (('XGB', 'xgboost'),
                     ('LGB', 'lightgbm'),
                     ('CatB', 'catboost'))

# List of models that need feature scaling
# Logistic regression can use regularization. Bayesian regression uses ridge
scaling_models = ['OLS', 'Ridge', 'Lasso', 'EN', 'BR', 'LR', 'KNN',
                  'XGB', 'LGB', 'CatB', 'lSVM', 'kSVM', 'PA', 'SGD', 'MLP']

# List of models that only work for regression/classification tasks
only_classification = ['BNB', 'GNB', 'MNB', 'LR', 'LDA', 'QDA']
only_regression = ['OLS', 'Lasso', 'EN', 'BR']

# List of models that don't use the Bayesian Optimization
no_BO = ['GP', 'GNB', 'OLS']


# << ============ Functions ============ >>

def prepare_logger(log):
    """Prepare logging file.

    Parameters
    ----------
    log: string
        Name of the logging file. 'auto' for default name with date and time.
        None to not save any log.

    Returns
    -------
    logger: callable
        Logger object.

    """
    if log is None:  # No logger
        return None

    if not log.endswith('.log'):
        log += '.log'

    if log == 'auto.log' or log.endswith('/auto.log'):
        current = datetime.now().strftime("%d%b%y_%Hh%Mm%Ss")
        log = log.replace('auto', 'ATOM_logger_' + current)

    # << ============ Create logging handler ============ >>

    # Define file handler and set formatter
    file_handler = logging.FileHandler(log)
    formatter = logging.Formatter('%(asctime)s: %(message)s')
    file_handler.setFormatter(formatter)

    # Define logger
    logger = logging.getLogger('ATOM_logger')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    if logger.hasHandlers():  # Remove existing handlers
        logger.handlers.clear()
    logger.addHandler(file_handler)  # Add file handler to logger

    return logger


def time_to_string(t_init):
    """Convert time integer to string.

    Convert a time duration to a neat string in format 00h:00m:00s
    or 1.000s if under 1 min.

    Parameters
    ----------
    t_init: float
        Time to convert (in seconds).

    """
    t = time() - t_init  # Total time in seconds
    h = int(t/3600.)
    m = int(t/60.) - h*60
    s = t - h*3600 - m*60
    if h < 1 and m < 1:  # Only seconds
        return f'{s:.3f}s'
    elif h < 1:  # Also minutes
        return f'{m}m:{int(s):02}s'
    else:  # Also hours
        return f'{h}h:{m:02}m:{int(s):02}s'


def to_df(data, columns=None, pca=False):
    """Convert a dataset to pd.Dataframe.

    Parameters
    ----------
    data: list, tuple or np.array
        Dataset to convert to a dataframe.

    columns: list, tuple or None
        Name of the columns in the dataset. If None, the names are autofilled.

    pca: bool
        whether the columns need to be called Features or Components.

    """
    if columns is None and not pca:
        columns = ['Feature ' + str(i) for i in range(len(data[0]))]
    elif columns is None:
        columns = ['Component ' + str(i) for i in range(len(data[0]))]
    return pd.DataFrame(data, columns=columns)


def to_series(data, name=None):
    """Convert a column to pd.Series.

    Parameters
    ----------
    data: list, tuple or np.array
        Data to convert.

    name: string or None
        Name of the target column. If None, the name is set to 'target'.

    """
    return pd.Series(data, name=name if name is not None else 'target')


def merge(X, y):
    """Merge pd.DataFrame and pd.Series into one dataframe."""
    return X.merge(y.to_frame(), left_index=True, right_index=True)


def check_scaling(X):
    """Check if the provided data is already scaled."""
    mean = X.mean(axis=1).mean()
    std = X.std(axis=1).mean()
    return True if mean < 0.05 and 0.5 < std < 1.5 else False


def variable_return(X, y):
    """Return one or two arguments depending on if y is None."""
    if y is None:
        return X
    else:
        return X, y


def check_is_fitted(is_fitted):
    """Check if the class has been fitted."""
    if not is_fitted:
        raise AttributeError("Run the pipeline before calling this method!")


# << ============ Decorators ============ >>

def composed(*decs):
    """Add multiple decorators in one line.

    Parameters
    ----------
    decs: tuple
        Decorators to run.

    """
    def deco(f):
        for dec in reversed(decs):
            f = dec(f)
        return f
    return deco


def crash(f):
    """Save program crashes to log file."""
    def wrapper(*args, **kwargs):
        try:  # Run the function
            result = f(*args, **kwargs)
            return result

        except Exception as exception:
            log = args[0].T.log if hasattr(args[0], 'T') else args[0].log

            # Write exception to log and raise it
            if type(log) == logging.Logger:
                log.exception("Exception encountered:")
            raise eval(type(exception).__name__)(exception)

    return wrapper


def params_to_log(f):
    """Save function's Parameters to log file."""
    def wrapper(*args, **kwargs):
        log = args[0].T.log if hasattr(args[0], 'T') else args[0].log
        kwargs_list = ['{}={!r}'.format(k, v) for k, v in kwargs.items()]
        args_list = [str(i) for i in args[1:]]
        args_list = args_list + [''] if len(kwargs_list) != 0 else args_list
        if log is not None:
            if f.__name__ == '__init__':
                log.info(f"Method: {args[0].__class__.__name__}.{f.__name__}" +
                         f"(X, y, {', '.join(kwargs_list)})")
            else:
                log.info('')  # Empty line first
                log.info(f"Method: {args[0].__class__.__name__}.{f.__name__}" +
                         f"({', '.join(args_list)}{', '.join(kwargs_list)})")

        result = f(*args, **kwargs)
        return result

    return wrapper
