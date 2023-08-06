# -*- coding: utf-8 -*-

"""Automated Tool for Optimized Modelling (ATOM).

Author: tvdboom
Description: Module containing the parent class for all model subclasses

"""

# << ============ Import Packages ============ >>

# Standard packages
import numpy as np
import math
from time import time
from collections import deque
from typeguard import typechecked
from typing import Optional, Union, Sequence, Tuple

# Sklearn
from sklearn.utils import resample
from sklearn.metrics import SCORERS, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold, StratifiedKFold, cross_val_score

# Others
from GPyOpt.methods import BayesianOptimization

# Plots
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

# Own package modules
from .utils import (
    cal, X_types, no_BO, composed, crash, params_to_log, time_to_string
    )
from .plots import (
        save, plot_bagging, plot_successive_halving, plot_learning_curve,
        plot_ROC, plot_PRC, plot_permutation_importance,
        plot_feature_importance, plot_confusion_matrix, plot_threshold,
        plot_probabilities, plot_calibration, plot_gains, plot_lift
        )


# << ====================== Classes ====================== >>

class BaseModel(object):
    """Parent class of all model subclasses."""

    def __init__(self, **kwargs):
        """Initialize class.

        Parameters
        ----------
        data: dict
            Dictionary of the data used for this model (train, test and all).

        T: class
            ATOM class. To avoid having to pass attributes throw params.

        """
        # Set attributes from ATOM to the model's parent class
        self.__dict__.update(kwargs)
        self.error = "No exceptions encountered!"

    @composed(crash, params_to_log, typechecked)
    def bayesian_optimization(self,
                              max_iter: int = 10,
                              max_time: Union[int, float] = np.inf,
                              init_points: int = 5,
                              cv: int = 3,
                              plot_bo: bool = False):
        """Run the bayesian optmization algorithm.

        Search for the best combination of hyperparameters. The function to
        optimize is evaluated either with a K-fold cross-validation on the
        training set or using a validation set.

        Parameters
        ----------
        max_iter: int, list or tuple, optional (default=10)
            Maximum number of iterations of the BO. If 0, skip the BO and fit
            the model on its default parameters.

        max_time: int, float, list or tuple, optional (default=np.inf)
            Maximum time allowed for the BO per model (in seconds). If 0, skip
            the BO and fit the model on its default parameters.

        init_points: int, list or tuple, optional (default=5)
            Initial number of tests of the BO before fitting the surrogate
            function.

        cv: int, list or tuple, optional (default=3)
            Strategy to fit and score the model selected after every step
            of the BO.
                - if 1, randomly split into a train and validation set
                - if >1, perform a k-fold cross validation on the training set

        plot_bo: bool, optional (default=False)
            whether to plot the BO's progress as it runs. Creates a canvas with
            two plots: the first plot shows the score of every trial and the
            second shows the distance between the last consecutive steps. Don't
            forget to call %matplotlib at the start of the cell if you are
            using jupyter notebook!

        """
        def animate_plot(x, y1, y2, line1, line2, ax1, ax2):
            """Plot the BO's progress as it runs.

            Creates a canvas with two plots. The first plot shows the score of
            every trial and the second shows the distance between the last
            consecutive steps.

            Parameters
            ----------
            x: list
                Values of both on the X-axis.

            y1, y2: list
                Values of the first and second plot on the y-axis.

            line1, line2: callable
                Line objects (from matplotlib) of the first and second plot.

            ax1, ax2: callable
                Axes objects (from matplotlib) of the first and second plot.

            """
            if line1 == []:  # At the start of the plot...
                # This is the call to matplotlib that allows dynamic plotting
                plt.ion()

                # Initialize plot
                fig = plt.figure(figsize=(10, 6))
                gs = GridSpec(2, 1, height_ratios=[2, 1])

                # First subplot (without xtick labels)
                ax1 = plt.subplot(gs[0])
                # Create a variable for the line so we can later update it
                line1, = ax1.plot(x, y1, '-o', alpha=0.8)
                ax1.set_title(f"Bayesian Optimization for {self.longname}",
                              fontsize=self.T.title_fontsize)
                ax1.set_ylabel(self.T.metric.name,
                               fontsize=self.T.label_fontsize,
                               labelpad=12)
                ax1.set_xlim(min(self.x)-0.5, max(self.x)+0.5)

                # Second subplot
                ax2 = plt.subplot(gs[1], sharex=ax1)
                line2, = ax2.plot(x, y2, '-o', alpha=0.8)
                ax2.set_title("Metric distance between last consecutive steps",
                              fontsize=self.T.title_fontsize)
                ax2.set_xlabel('Step',
                               fontsize=self.T.label_fontsize,
                               labelpad=12)
                ax2.set_ylabel('d',
                               fontsize=self.T.label_fontsize,
                               labelpad=12)
                ax2.set_xticks(self.x)
                ax2.set_xlim(min(self.x)-0.5, max(self.x)+0.5)
                ax2.set_ylim([-0.05, 0.1])

                plt.setp(ax1.get_xticklabels(), visible=False)
                plt.subplots_adjust(hspace=.0)
                plt.xticks(fontsize=self.T.tick_fontsize)
                plt.yticks(fontsize=self.T.tick_fontsize)
                fig.tight_layout()
                plt.show()

            # Update plot
            line1.set_xdata(x)
            line1.set_ydata(y1)
            line2.set_xdata(x)
            line2.set_ydata(y2)
            ax1.set_xlim(min(self.x)-0.5, max(self.x)+0.5)
            ax2.set_xlim(min(self.x)-0.5, max(self.x)+0.5)
            ax1.set_xticks(self.x)  # Update x-ticks
            ax2.set_xticks(self.x)  # Update x-ticks

            # Adjust y limits if new data goes beyond bounds
            lim = line1.axes.get_ylim()
            if np.nanmin(y1) <= lim[0] or np.nanmax(y1) >= lim[1]:
                ax1.set_ylim([np.nanmin(y1) - np.nanstd(y1),
                              np.nanmax(y1) + np.nanstd(y1)])
            lim = line2.axes.get_ylim()
            if np.nanmax(y2) >= lim[1]:
                ax2.set_ylim([-0.05, np.nanmax(y2) + np.nanstd(y2)])

            # Pause the data so the figure/axis can catch up
            plt.pause(0.01)

            # Return line and axes to update the plot again next iteration
            return line1, line2, ax1, ax2

        def optimize(x):
            """Optimization function for the baysisan optimization algorithm.

            Parameters
            ----------
            x: dict
                Dictionary of the model's  hyperparameters.

            Returns
            -------
            score: float
                Score achieved by the model.

            """
            t_iter = time()  # Get current time for start of the iteration

            params = self.get_params(x)
            self.BO['params'].append(params)

            # Print iteration and time
            self._iter += 1
            if self._iter > self.init_points:
                _iter = self._iter - self.init_points
                point = 'Iteration'
            else:
                _iter = self._iter
                point = 'Initial point'

            len_ = '-' * (46 - len(point) - len(str(self._iter)))
            self.T._log(f"{point}: {_iter} {len_}", 2)
            self.T._log(f"Parameters --> {params}", 2)

            algorithm = self.get_model(params)

            if self.cv == 1:
                # Split each iteration in different train and validation set
                X_subtrain, X_validation, y_subtrain, y_validation = \
                    train_test_split(self.X_train,
                                     self.y_train,
                                     test_size=self.T.test_size,
                                     shuffle=True)

                # Calculate metric on the validation set
                algorithm.fit(X_subtrain, y_subtrain)
                score = self.T.metric(algorithm, X_validation, y_validation)

            else:  # Use cross validation to get the output of BO

                # Determine number of folds for the cross_val_score
                if self.T.task != 'regression':
                    # Folds are made preserving the % of samples for each class
                    # Use same splits for every model
                    kfold = StratifiedKFold(n_splits=self.cv, random_state=1)
                else:
                    kfold = KFold(n_splits=self.cv, random_state=1)

                # Run cross-validation (get mean of results)
                score = cross_val_score(algorithm,
                                        self.X_train,
                                        self.y_train,
                                        cv=kfold,
                                        scoring=self.T.metric,
                                        n_jobs=self.T.n_jobs).mean()

            # Save output of the BO and plot progress
            self.BO['score'].append(score)
            self.T._log(f"Evaluation --> {self.T.metric.name}: {score:.4f}", 2)

            t = time_to_string(t_iter)
            t_tot = time_to_string(self._init_bo)
            self.BO['time'] = t
            self.BO['total_time'] = t_tot
            self.T._log(f"Time elapsed: {t}   Total time: {t_tot}", 2)

            if self.plot_bo:
                # Start to fill NaNs with encountered metric values
                if np.isnan(self.y1).any():
                    for i, value in enumerate(self.y1):
                        if math.isnan(value):
                            self.y1[i] = score
                            if i > 0:  # The first value must remain empty
                                self.y2[i] = abs(self.y1[i] - self.y1[i-1])
                            break
                else:  # If no NaNs anymore, continue deque
                    self.x.append(max(self.x)+1)
                    self.y1.append(score)
                    self.y2.append(abs(self.y1[-1] - self.y1[-2]))

                self.line1, self.line2, self.ax1, self.ax2 = \
                    animate_plot(self.x, self.y1, self.y2,
                                 self.line1, self.line2, self.ax1, self.ax2)

            return score

        # << ================= Running optimization ================= >>

        # Check parameters
        if max_iter < 0:
            raise ValueError("Invalid value for the max_iter parameter." +
                             f"Value should be >=0, got {max_iter}.")
        if max_time < 0:
            raise ValueError("Invalid value for the max_time parameter." +
                             f"Value should be >=0, got {max_time}.")
        if init_points < 1:
            raise ValueError("Invalid value for the init_points parameter." +
                             f"Value should be >0, got {init_points}.")
        if cv < 1:
            raise ValueError("Invalid value for the cv parameter." +
                             f"Value should be >0, got {cv}.")

        # Update attibutes
        self._has_BO = True if max_iter > 0 and max_time > 0 else False
        self.max_iter = max_iter
        self.max_time = max_time
        self.init_points = init_points
        self.cv = cv
        self.plot_bo = plot_bo

        # Skip BO for GNB and GP (no hyperparameter tuning)
        if self.name not in no_BO and self._has_BO:
            self.T._log(f"\n\nRunning BO for {self.longname}...", 1)

            # Save dictionary of BO steps
            self._iter = 0
            self._init_bo = time()
            self.BO = {}
            self.BO['params'] = []
            self.BO['score'] = []

            if self.plot_bo:  # Create plot variables
                maxlen = 15  # Maximum steps to show at once in the plot
                self.x = deque(list(range(maxlen)), maxlen=maxlen)
                self.y1 = deque([np.NaN for _ in self.x], maxlen=maxlen)
                self.y2 = deque([np.NaN for _ in self.x], maxlen=maxlen)
                self.line1, self.line2 = [], []  # Plot lines
                self.ax1, self.ax2 = 0, 0  # Plot axes

            # Default SKlearn or multiple random initial points
            kwargs = {}
            if self.init_points > 1:
                kwargs['initial_design_numdata'] = self.init_points
            else:
                kwargs['X'] = self.get_init_values()
            BO = BayesianOptimization(f=optimize,
                                      domain=self.get_domain(),
                                      model_update_interval=1,
                                      maximize=True,
                                      initial_design_type='random',
                                      normalize_Y=False,
                                      num_cores=self.T.n_jobs,
                                      **kwargs)

            # eps = Minimum distance in hyperparameters between two
            #       consecutive steps of the BO
            BO.run_optimization(max_iter=self.max_iter,
                                max_time=self.max_time,
                                eps=1e-8,
                                verbosity=False)

            # Optimal score of the BO (neg due to the implementation of GpyOpt)
            self.score_bo = -BO.fx_opt

            if self.plot_bo:
                plt.close()

            # Set to same shape as GPyOpt (2d-array)
            self.best_params = self.get_params(np.round([BO.x_opt], 4))

            # Save best model (not yet fitted)
            self.best_model = self.get_model(self.best_params)

            self.time_bo = time_to_string(self._init_bo)  # Get the BO duration

            # Print results
            self.T._log('', 2)  # Print extra line (note verbosity level 2)
            self.T._log(f"Final results for {self.longname}:{' ':9s}", 1)
            self.T._log("Bayesian Optimization ---------------------------", 1)
            self.T._log(f"Best hyperparameters: {self.best_params}", 1)
            self.T._log(f"Best score on the BO: {self.score_bo:.4f}", 1)
            self.T._log(f"Time elapsed: {self.time_bo}", 1)

        else:
            self.best_model = self.get_model()

    @composed(crash, params_to_log)
    def fit(self):
        """Fit the best model to the test set."""
        t_init = time()

        # In case the bayesian_optimization method wasn't called
        if not hasattr(self, 'best_model'):
            self.best_model = self.get_model()

        # Fit the selected model on the complete training set
        self.best_model_fit = self.best_model.fit(self.X_train, self.y_train)

        # Save predictions
        self.predict_train = self.best_model_fit.predict(self.X_train)
        self.predict_test = self.best_model_fit.predict(self.X_test)

        # Save probability predictions
        if self.T.task != 'regression':
            if hasattr(self.best_model_fit, 'predict_proba'):
                self.predict_proba_train = \
                    self.best_model_fit.predict_proba(self.X_train)
                self.predict_proba_test = \
                    self.best_model_fit.predict_proba(self.X_test)
            if hasattr(self.best_model_fit, 'decision_function'):
                self.decision_function_train = \
                    self.best_model_fit.decision_function(self.X_train)
                self.decision_function_test = \
                    self.best_model_fit.decision_function(self.X_test)

        # Save scores on complete training and test set
        self.score_train = self.T.metric(
                            self.best_model_fit, self.X_train, self.y_train)
        self.score_test = self.T.metric(
                            self.best_model_fit, self.X_test, self.y_test)

        # Calculate custom metrics and attach to attributes
        if self.T.task != 'regression':
            self.confusion_matrix = confusion_matrix(self.y_test,
                                                     self.predict_test)
            if self.T.task.startswith('binary'):
                tn, fp, fn, tp = self.confusion_matrix.ravel()

                # Get metrics (lift, true (false) positive rate and support)
                self.lift = (tp/(tp+fp))/((tp+fn)/(tp+tn+fp+fn))
                self.fpr = fp/(fp+tn)
                self.tpr = tp/(tp+fn)
                self.sup = (tp+fp)/(tp+fp+fn+tn)

                self.tn, self.fp, self.fn, self.tp = tn, fp, fn, tp

        # Calculate all pre-defined metrics on the test set
        for key in SCORERS.keys():
            try:
                m = getattr(self.T.metric, key)

                # Some metrics need probabilities and other need predict
                if type(m).__name__ == '_ThresholdScorer':
                    if self.T.task == 'regression':
                        y_pred = self.predict_test
                    elif hasattr(self, 'decision_function_test'):
                        y_pred = self.decision_function_test
                    else:
                        y_pred = self.predict_proba_test
                        if self.T.task.startswith('binary'):
                            y_pred = y_pred[:, 1]
                elif type(m).__name__ == '_ProbaScorer':
                    if hasattr(self, 'predict_proba_test'):
                        y_pred = self.predict_proba_test
                        if self.T.task.startswith('binary'):
                            y_pred = y_pred[:, 1]
                    else:
                        y_pred = self.decision_function_test
                else:
                    y_pred = self.predict_test
                scr = m._sign * m._score_func(self.y_test, y_pred, **m._kwargs)
                setattr(self, key, scr)
            except Exception:
                msg = f"This metric is unavailable for the {self.name} model!"
                setattr(self, key, msg)

        # << ================= Print stats ================= >>

        if not self._has_BO:
            self.T._log('\n', 1)  # Print 2 extra lines
            self.T._log(f"Final results for {self.longname}:{' ':9s}", 1)
        if self.name in no_BO and self._has_BO:
            self.T._log('\n', 1)  # Print 2 extra lines
            self.T._log(f"Final results for {self.longname}:{' ':9s}", 1)
        self.T._log("Fitting -----------------------------------------", 1)
        self.T._log(f"Score on the training set: {self.score_train:.4f}", 1)
        self.T._log(f"Score on the test set: {self.score_test:.4f}", 1)

        # Get duration and print to log
        duration = time_to_string(t_init)
        self.fit_time = duration
        self.T._log(f"Time elapsed: {duration}", 1)

    @composed(crash, params_to_log, typechecked)
    def bagging(self, bagging: Optional[int] = 5):
        """Peform bagging algorithm.

        Take bootstrap samples from the training set and test them on the test
        set to get a distribution of the model's results.

        Parameters
        ----------
        bagging: int or None, optional (default=5)
            Number of data sets (bootstrapped from the training set) to use in
            the bagging algorithm. If None or 0, no bagging is performed.

        """
        t_init = time()

        if bagging is None or bagging == 0:
            return None  # Do not perform bagging
        elif bagging < 0:
            raise ValueError("Invalid value for the bagging parameter." +
                             f"Value should be >=0, got {bagging}.")

        self.bagging_scores = []  # List of the scores
        for _ in range(bagging):
            # Create samples with replacement
            sample_x, sample_y = resample(self.X_train, self.y_train)

            # Fit on bootstrapped set and predict on the independent test set
            algorithm = self.best_model.fit(sample_x, sample_y)
            score = self.T.metric(algorithm, self.X_test, self.y_test)

            # Append metric result to list
            self.bagging_scores.append(score)

        # Numpy array for mean and std
        self.bagging_scores = np.array(self.bagging_scores)
        self.T._log("Bagging -----------------------------------------", 1)
        self.T._log("Mean: {:.4f}   Std: {:.4f}".format(
                    self.bagging_scores.mean(), self.bagging_scores.std()), 1)

        # Get duration and print to log
        duration = time_to_string(t_init)
        self.bs_time = duration
        self.T._log(f"Time elapsed: {duration}", 1)

    # << =================== Pipeline methods =================== >>

    def _pipeline_methods(self, X, attribute, **kwargs):
        """Apply pipeline methods on new data.

        First transform the new data and apply the attribute on the best
        model. The model has to have the provided attribute.

        Parameters
        ----------
        X: dict, sequence, np.array or pd.DataFrame
            Data containing the features, with shape=(n_samples, n_features).

        attribute: str
            Attribute of the model to be applied.

        **kwargs
            Additional parameters for the transform method.

        Returns
        -------
        np.array
            Return of the attribute.

        """
        if not hasattr(self.best_model_fit, attribute):
            raise AttributeError("The winning model doesn't have a " +
                                 f"{attribute} attribute!")

        X_transformed = self.T.transform(X, **kwargs)
        return getattr(self.best_model_fit, attribute)(X_transformed)

    @composed(crash, params_to_log, typechecked)
    def transform(self, X: X_types, **kwargs):
        """Apply all data transformations in ATOM to new data."""
        return self.T.transform(X, **kwargs)

    @composed(crash, params_to_log, typechecked)
    def predict(self, X: X_types, **kwargs):
        """Get predictions on new data."""
        return self._pipeline_methods(X, 'predict', **kwargs)

    @composed(crash, params_to_log, typechecked)
    def predict_proba(self, X: X_types, **kwargs):
        """Get probability predictions on new data."""
        return self._pipeline_methods(X, 'predict_proba', **kwargs)

    @composed(crash, params_to_log, typechecked)
    def predict_log_proba(self, X: X_types, **kwargs):
        """Get log probability predictions on new data."""
        return self._pipeline_methods(X, 'predict_log_proba', **kwargs)

    @composed(crash, params_to_log, typechecked)
    def decision_function(self, X: X_types, **kwargs):
        """Get the decision function on new data."""
        return self._pipeline_methods(X, 'decision_function', **kwargs)

    # << ==================== Plot functions ==================== >>

    @composed(crash, params_to_log, typechecked)
    def plot_bagging(self,
                     title: Optional[str] = None,
                     figsize: Optional[Tuple[int, int]] = None,
                     filename: Optional[str] = None,
                     display: bool = True):
        """Boxplot of the bagging's results."""
        plot_bagging(self.T, self.name, title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_successive_halving(self,
                                title: Optional[str] = None,
                                figsize: Tuple[int, int] = (10, 6),
                                filename: Optional[str] = None,
                                display: bool = True):
        """Plot the models' scores per iteration of the successive halving."""
        plot_successive_halving(self.T, self.name,
                                title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_learning_curve(
                    self,
                    title: Optional[str] = None,
                    figsize: Tuple[int, int] = (10, 6),
                    filename: Optional[str] = None,
                    display: bool = True):
        """Plot the model's learning curve: score vs training samples."""
        plot_learning_curve(self.T, self.name,
                            title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_ROC(self,
                 title: Optional[str] = None,
                 figsize: Tuple[int, int] = (10, 6),
                 filename: Optional[str] = None,
                 display: bool = True):
        """Plot the Receiver Operating Characteristics curve."""
        plot_ROC(self.T, self.name, title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_PRC(self,
                 title: Optional[str] = None,
                 figsize: Tuple[int, int] = (10, 6),
                 filename: Optional[str] = None,
                 display: bool = True):
        """Plot the precision-recall curve."""
        plot_PRC(self.T, self.name, title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_permutation_importance(self,
                                    show: Optional[int] = None,
                                    n_repeats: int = 10,
                                    title: Optional[str] = None,
                                    figsize: Optional[Tuple[int, int]] = None,
                                    filename: Optional[str] = None,
                                    display: bool = True):
        """Plot the feature permutation importance of models."""
        plot_permutation_importance(self.T, self.name, show, n_repeats,
                                    title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_feature_importance(self,
                                show: Optional[int] = None,
                                title: Optional[str] = None,
                                figsize: Optional[Tuple[int, int]] = None,
                                filename: Optional[str] = None,
                                display: bool = True):
        """Plot a tree-based model's normalized feature importances."""
        plot_feature_importance(self.T, self.name,
                                show, title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_confusion_matrix(self,
                              normalize: bool = False,
                              title: Optional[str] = None,
                              figsize: Tuple[int, int] = (8, 8),
                              filename: Optional[str] = None,
                              display: bool = True):
        """Plot the confusion matrix.

        For 1 model: plot it's confusion matrix in a heatmap.
        For >1 models: compare TP, FP, FN and TN in a barplot.

        """
        plot_confusion_matrix(self.T, self.name, normalize,
                              title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_threshold(self,
                       metric: Optional[Union[cal, Sequence[cal]]] = None,
                       steps: int = 100,
                       title: Optional[str] = None,
                       figsize: Tuple[int, int] = (10, 6),
                       filename: Optional[str] = None,
                       display: bool = True):
        """Plot performance metric(s) against threshold values."""
        plot_threshold(self.T, self.name, metric, steps,
                       title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_probabilities(self,
                           target: Union[int, str] = 1,
                           title: Optional[str] = None,
                           figsize: Tuple[int, int] = (10, 6),
                           filename: Optional[str] = None,
                           display: bool = True):
        """Plot the distribution of predicted probabilities."""
        plot_probabilities(self.T, self.name, target,
                           title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_calibration(self,
                         n_bins: int = 10,
                         models: Union[None, str, Sequence[str]] = None,
                         title: Optional[str] = None,
                         figsize: Tuple[int, int] = (10, 10),
                         filename: Optional[str] = None,
                         display: bool = True):
        """Plot the calibration curve for a binary classifier."""
        plot_calibration(self.T, self.name, n_bins,
                         title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_gains(self,
                   models: Union[None, str, Sequence[str]] = None,
                   title: Optional[str] = None,
                   figsize: Tuple[int, int] = (10, 6),
                   filename: Optional[str] = None,
                   display: bool = True):
        """Plot the cumulative gains curve."""
        plot_gains(self.T, self.name, title, figsize, filename, display)

    @composed(crash, params_to_log, typechecked)
    def plot_lift(self,
                  models: Union[None, str, Sequence[str]] = None,
                  title: Optional[str] = None,
                  figsize: Tuple[int, int] = (10, 6),
                  filename: Optional[str] = None,
                  display: bool = True):
        """Plot the lift curve."""
        plot_lift(self.T, self.name, title, figsize, filename, display)

    # << ============ Utility functions ============ >>

    @composed(crash, params_to_log, typechecked)
    def save_model(self, filename: Optional[str] = None):
        """Save the best found model (fitted) to a pickle file."""
        save(self.best_model_fit,
             'model_' + self.name if filename is None else filename)
        self.T._log(self.longname + " model saved successfully!", 1)

    @composed(crash, params_to_log, typechecked)
    def save(self, filename: Optional[str] = None):
        """Save the class to a pickle file."""
        save(self, 'ATOM_' + self.name if filename is None else filename)
        self.T._log("ATOM's " + self.name + " class saved successfully!", 1)
