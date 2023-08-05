# -*- coding: utf-8 -*-

import numpy as np, warnings
from .utils import _check_constructor_input, _check_beta_prior, \
            _check_smoothing, _check_fit_input, _check_X_input, _check_1d_inp, \
            _ZeroPredictor, _OnePredictor, _OneVsRest,\
            _BootstrappedClassifier_w_predict, _BootstrappedClassifier_w_predict_proba, \
            _BootstrappedClassifier_w_decision_function, _check_njobs, \
            _BayesianLogisticRegression,\
            _check_bools, _check_refit_buffer, _check_refit_inp, _check_random_state, \
            _add_method_predict_robust, _check_active_inp, \
            _check_autograd_supported, _get_logistic_grads_norms, _gen_random_grad_norms, \
            _check_bay_inp, _apply_softmax, _apply_inverse_sigmoid, \
            _LinUCB_n_TS_single, _LogisticUCB_n_TS_single
from ._cy_utils import _choice_over_rows

class _BasePolicy:
    def __init__(self):
        pass

    def _add_common_params(self, base_algorithm, beta_prior, smoothing, njobs, nchoices,
            batch_train, refit_buffer, deep_copy_buffer, assume_unique_reward,
            random_state, assign_algo=True, prior_def_ucb = False):
        
        if isinstance(base_algorithm, np.ndarray) or base_algorithm.__class__.__name__ == "Series":
            base_algorithm = list(base_algorithm)

        self._add_choices(nchoices)
        _check_constructor_input(base_algorithm, self.nchoices, batch_train)
        self.smoothing = _check_smoothing(smoothing)
        self.njobs = _check_njobs(njobs)
        self.batch_train, self.assume_unique_reward = _check_bools(batch_train, assume_unique_reward)
        self.beta_prior = _check_beta_prior(beta_prior, self.nchoices, prior_def_ucb)
        self.random_state = _check_random_state(random_state)

        if assign_algo:
            self.base_algorithm = base_algorithm
            if ("warm_start" in dir(self.base_algorithm)) and (self.base_algorithm.warm_start):
                self.has_warm_start = True
            else:
                self.has_warm_start = False
        else:
            self.has_warm_start = False

        self.refit_buffer = _check_refit_buffer(refit_buffer, self.batch_train)
        self.deep_copy_buffer = bool(deep_copy_buffer)

        ### For compatibility with the active policies
        self._force_fit = False
        self._force_counters = False

        self.is_fitted = False

    def _add_choices(self, nchoices):
        if isinstance(nchoices, int):
            self.nchoices = nchoices
            self.choice_names = None
        elif isinstance(nchoices, list) or nchoices.__class__.__name__ == "Series" or nchoices.__class__.__name__ == "DataFrame":
            self.choice_names = np.array(nchoices).reshape(-1)
            self.nchoices = self.choice_names.shape[0]
            if np.unique(self.choice_names).shape[0] != self.choice_names.shape[0]:
                raise ValueError("Arm/choice names contain duplicates.")
        elif isinstance(nchoices, np.ndarray):
            self.choice_names = nchoices.reshape(-1)
            self.nchoices = self.choice_names.shape[0]
            if np.unique(self.choice_names).shape[0] != self.choice_names.shape[0]:
                raise ValueError("Arm/choice names contain duplicates.")
        else:
            raise ValueError("'nchoices' must be an integer or list with named arms.")

    def _name_arms(self, pred):
        if self.choice_names is None:
            return pred
        else:
            return self.choice_names[pred]

    def drop_arm(self, arm_name):
        """
        Drop an arm/choice

        Drops (removes/deletes) an arm from the set of available choices to the policy.

        Note
        ----
        The available arms, if named, are stored in attribute 'choice_names'.
        
        Parameters
        ----------
        arm_name : int or object
            Arm to drop. If passing an integer, will drop at that index (starting at zero). Otherwise,
            will drop the arm matching this name (argument must be of the same type as the individual entries
            passed to 'nchoices' in the initialization).

        Returns
        -------
        self : object
            This object
        """
        drop_ix = self._get_drop_ix(arm_name)
        self._oracles._drop_arm(drop_ix)
        self._drop_ix(drop_ix)
        self.has_warm_start = False
        return self

    def _get_drop_ix(self, arm_name):
        if isinstance(arm_name, int):
            if arm_name > self.nchoices:
                raise ValueError("Object has only ", str(self.nchoices), " arms.")
            drop_ix = arm_name
        else:
            if self.choice_names is None:
                raise ValueError("If arms are not named, must pass an integer value.")
            for ch in range(self.nchoices):
                if self.choice_names[ch] == arm_name:
                    drop_ix = ch
                    break
            else:
                raise ValueError("No arm named '", str(arm_name), "' - current names are stored in attribute 'choice_names'.")
        return drop_ix

    def _drop_ix(self, drop_ix):
        if self.choice_names is None:
            self.choice_names = np.arange(self.nchoices)
        self.nchoices -= 1
        self.choice_names = np.r_[self.choice_names[:drop_ix], self.choice_names[drop_ix + 1:]]

    ## TODO: maybe add functionality to take an arm from another object of this class

    def add_arm(self, arm_name = None, fitted_classifier = None,
                n_w_rew = 0, n_wo_rew = 0,
                refit_buffer_X = None, refit_buffer_r = None):
        """
        Adds a new arm to the pool of choices

        Parameters
        ----------
        arm_name : object
            Name for this arm. Only applicable when using named arms. If None, will use the name of the last
            arm plus 1 (will only work when the names are integers).
        fitted_classifier : object
            If a classifier has already been fit to rewards coming from this arm, you can pass it here, otherwise,
            will be started from the same 'base_classifier' as the initial arms. If using bootstrapped or Bayesian methods,
            don't pass a classifier here (unless using the classes in `utils._BootstrappedClassifierBase` or `utils._BayesianLogisticRegression`)
        n_w_rew : int
            Number of trials/rounds with rewards coming from this arm (only used when using a beta prior or smoothing).
        n_wo_rew : int
            Number of trials/rounds without rewards coming from this arm (only used when using a beta prior or smoothing).
        refit_buffer_X : array(m, n) or None
            Refit buffer of 'X' data to use for the new arm. Ignored when using
            'batch_train=False' or 'refit_buffer=None'.
        refit_buffer_r : array(m,) or None
            Refit buffer of rewards data to use for the new arm. Ignored when using
            'batch_train=False' or 'refit_buffer=None'.

        Returns
        -------
        self : object
            This object
        """
        assert isinstance(n_w_rew,  int)
        assert isinstance(n_wo_rew, int)
        assert n_w_rew >= 0
        assert n_wo_rew >= 0
        refit_buffer_X, refit_buffer_r = \
            _check_refit_inp(refit_buffer_X, refit_buffer_r, self.refit_buffer)
        arm_name = self._check_new_arm_name(arm_name)
        self._oracles._spawn_arm(fitted_classifier, n_w_rew, n_wo_rew,
                                 refit_buffer_X, refit_buffer_r)
        self._append_arm(arm_name)
        return self

    def _check_new_arm_name(self, arm_name):
        if self.choice_names is None and arm_name is not None:
            raise ValueError("Cannot create a named arm when no names were passed to 'nchoices'.")
        if arm_name is None and self.choice_names is not None:
            try:
                arm_name = self.choice_names[-1] + 1
            except:
                raise ValueError("Must provide an arm name when using named arms.")
        return arm_name

    def _append_arm(self, arm_name):
        if self.choice_names is not None:
            self.choice_names = np.r_[self.choice_names, np.array(arm_name).reshape((1,))]
        self.nchoices += 1

    def fit(self, X, a, r, warm_start=False):
        """
        Fits the base algorithm (one per class [and per sample if bootstrapped]) to partially labeled data.

        Parameters
        ----------
        X : array (n_samples, n_features)
            Matrix of covariates for the available data.
        a : array (n_samples), int type
            Arms or actions that were chosen for each observations.
        r : array (n_samples), {0,1}
            Rewards that were observed for the chosen actions. Must be binary rewards 0/1.
        warm_start : bool
            Whether to use the results of previous calls to 'fit' as a start
            for fitting to the 'X' data passed here. This will only be available
            if the base classifier has a property ``warm_start`` too and that
            property is also set to 'True'. You can double-check that it's
            recognized as such by checking this object's property
            ``has_warm_start``. Passing 'True' when the classifier doesn't
            support warm start despite having the property might slow down
            things.
            Dropping arms will make this functionality unavailable.
            This options is not available for 'BootstrappedUCB',
            nor for 'BootstrappedTS'.

        Returns
        -------
        self : obj
            This object
        """
        X, a, r = _check_fit_input(X, a, r, self.choice_names)
        use_warm = warm_start and self.has_warm_start and self.is_fitted
        self._oracles = _OneVsRest(self.base_algorithm,
                                   X, a, r,
                                   self.nchoices,
                                   self.beta_prior[1], self.beta_prior[0][0], self.beta_prior[0][1],
                                   self.random_state,
                                   self.smoothing,
                                   self.assume_unique_reward,
                                   self.batch_train,
                                   refit_buffer = self.refit_buffer,
                                   deep_copy = self.deep_copy_buffer,
                                   force_fit = self._force_fit,
                                   force_counters = self._force_counters,
                                   prev_ovr = self._oracles if self.is_fitted else None,
                                   warm = use_warm,
                                   njobs = self.njobs)
        self.is_fitted = True
        return self
    
    def partial_fit(self, X, a, r):
        """
        Fits the base algorithm (one per class) to partially labeled data in batches.
        
        Note
        ----
        In order to use this method, the base classifier must have a 'partial_fit' method,
        such as 'sklearn.linear_model.SGDClassifier'. This method is not available
        for 'LogisticUCB', nor for 'LogisticTS'.

        Parameters
        ----------
        X : array (n_samples, n_features)
            Matrix of covariates for the available data.
        a : array (n_samples), int type
            Arms or actions that were chosen for each observations.
        r : array (n_samples), {0,1}
            Rewards that were observed for the chosen actions. Must be binary rewards 0/1.

        Returns
        -------
        self : obj
            This object
        """
        if not self.batch_train:
            raise ValueError("Must pass 'batch_train' = 'True' to use '.partial_fit'.")
        if '_oracles' in dir(self):
            X, a, r =_check_fit_input(X, a, r, self.choice_names)
            self._oracles.partial_fit(X, a, r)
            self.is_fitted = True
            return self
        else:
            return self.fit(X, a, r)
    
    def decision_function(self, X):
        """
        Get the scores for each arm following this policy's action-choosing criteria.

        Note
        ----
        For 'ExploreFirst', the results from this method will not actually follow the policy in
        assigning random numbers during the exploration phase.
        Same for 'AdaptiveGreedy' - it won't make random choices according to the policy.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            Data for which to obtain decision function scores for each arm.
        
        Returns
        -------
        scores : array (n_samples, n_choices)
            Scores following this policy for each arm.
        """
        X = _check_X_input(X)
        if not self.is_fitted:
            raise ValueError("Object has not been fit to data.")
        return self._oracles.decision_function(X)

    def _predict_random_if_unfit(self, X, output_score):
        warnings.warn("Model object has not been fit to data, predictions will be random.")
        X = _check_X_input(X)
        pred = self._name_arms(self.random_state.integers(self.nchoices, size = X.shape[0]))
        if not output_score:
            return pred
        else:
            return {"choice" : pred, "score" : (1.0 / self.nchoices) * np.ones(size = X.shape[0], dtype = "float64")}


class _BasePolicyWithExploit(_BasePolicy):
    def _add_bootstrapped_inputs(self, base_algorithm, batch_sample_method, nsamples, njobs_samples, percentile):
        assert (batch_sample_method == 'gamma') or (batch_sample_method == 'poisson')
        assert isinstance(nsamples, int)
        assert nsamples >= 2
        self.batch_sample_method = batch_sample_method
        self.nsamples = nsamples
        self.njobs_samples = _check_njobs(njobs_samples)
        if "predict_proba" in dir(base_algorithm):
            self.base_algorithm = _BootstrappedClassifier_w_predict_proba(
                base_algorithm, self.nsamples, percentile,
                self.batch_train, self.batch_sample_method,
                random_state = 1,
                njobs = self.njobs_samples
                )
        elif "decision_function" in dir(base_algorithm):
            self.base_algorithm = _BootstrappedClassifier_w_decision_function(
                base_algorithm, self.nsamples, percentile,
                self.batch_train, self.batch_sample_method,
                random_state = 1,
                njobs = self.njobs_samples
                )
        else:
            self.base_algorithm = _BootstrappedClassifier_w_predict(
                base_algorithm, self.nsamples, percentile,
                self.batch_train, self.batch_sample_method,
                random_state = 1,
                njobs = self.njobs_samples
                )

    def _exploit(self, X):
        return self._oracles.exploit(X)

    def predict(self, X, exploit = False, output_score = False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
        output_score : bool
            Whether to output the score that this method predicted, in case it is desired to use
            it with this pakckage's offpolicy and evaluation modules.
            
        Returns
        -------
        pred : array (n_samples,) or dict("choice" : array(n_samples,), "score" : array(n_samples,))
            Actions chosen by the policy. If passing output_score=True, it will be a dictionary
            with the chosen arm and the score that the arm got following this policy with the classifiers used.
        """
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, output_score)

        if exploit:
            scores = self._exploit(X)
        else:
            scores = self.decision_function(X)
        pred = self._name_arms(np.argmax(scores, axis = 1))

        if not output_score:
            return pred
        else:
            score_max = np.max(scores, axis=1).reshape((-1, 1))
            return {"choice" : pred, "score" : score_max}

class BootstrappedUCB(_BasePolicyWithExploit):
    """
    Bootstrapped Upper Confidence Bound

    Obtains an upper confidence bound by taking the percentile of the predictions from a
    set of classifiers, all fit with different bootstrapped samples (multiple samples per arm).
    
    Note
    ----
    When fitting the algorithm to data in batches (online), it's not possible to take an
    exact bootstrapped sample, as the sample is not known in advance. In theory, as the sample size
    grows to infinity, the number of times that an observation appears in a bootstrapped sample is
    distributed ~ Poisson(1). However, I've found that assigning random weights to observations
    produces a more stable effect, so it also has the option to assign weights randomly ~ Gamma(1,1).
    
    Parameters
    ----------
    base_algorithm : obj or list
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    nsamples : int
        Number of bootstrapped samples per class to take.
    percentile : int [0,100]
        Percentile of the predictions sample to take
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((5/nchoices, 4), 2)
        Note that it will only generate one random number per arm, so the 'a' parameters should be higher
        than for other methods.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to 'True',
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    batch_sample_method : str, either 'gamma' or 'poisson'
        How to simulate bootstrapped samples when training in batch mode (online).
        See Note.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs_arms : int or None
        Number of parallel jobs to run (for dividing work across arms). If passing None will set it to 1.
        If passing -1 will set it to the number of CPU cores. Note that if the base algorithm is itself
        parallelized, this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The total number of parallel jobs will be njobs_arms * njobs_samples. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.
    njobs_samples : int or None
        Number of parallel jobs to run (for dividing work across samples within one arm). If passing None
        will set it to 1. If passing -1 will set it to the number of CPU cores. The total number of parallel
        jobs will be njobs_arms * njobs_samples.
        The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, nsamples=10, percentile=80,
                 beta_prior='auto', smoothing=None, batch_train=False,
                 refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, batch_sample_method='gamma',
                 random_state=None, njobs_arms=-1, njobs_samples=1):
        assert (percentile >= 0) and (percentile <= 100)
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs_arms,
                                nchoices, batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state,
                                assign_algo = False, prior_def_ucb = True)
        self.percentile = percentile
        self._add_bootstrapped_inputs(base_algorithm, batch_sample_method, nsamples, njobs_samples, self.percentile)

class BootstrappedTS(_BasePolicyWithExploit):
    """
    Bootstrapped Thompson Sampling
    
    Performs Thompson Sampling by fitting several models per class on bootstrapped samples,
    then makes predictions by taking one of them at random for each class.
    
    Note
    ----
    When fitting the algorithm to data in batches (online), it's not possible to take an
    exact bootstrapped sample, as the sample is not known in advance. In theory, as the sample size
    grows to infinity, the number of times that an observation appears in a bootstrapped sample is
    distributed ~ Poisson(1). However, I've found that assigning random weights to observations
    produces a more stable effect, so it also has the option to assign weights randomly ~ Gamma(1,1).

    Note
    ----
    Unlike the other Thompson sampling classes, this class, due to using bootstrapped
    samples, does not offer the option 'sample_unique' - it's equivalent to
    always having `False` for that parameter in the other methods.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    nsamples : int
        Number of bootstrapped samples per class to take.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    batch_sample_method : str, either 'gamma' or 'poisson'
        How to simulate bootstrapped samples when training in batch mode (online).
        See Note.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs_arms : int or None
        Number of parallel jobs to run (for dividing work across arms). If passing None will set it to 1.
        If passing -1 will set it to the number of CPU cores. Note that if the base algorithm is itself
        parallelized, this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The total number of parallel jobs will be njobs_arms * njobs_samples.
        The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.
    njobs_samples : int or None
        Number of parallel jobs to run (for dividing work across samples within one arm). If passing None
        will set it to 1. If passing -1 will set it to the number of CPU cores. The total number of parallel
        jobs will be njobs_arms * njobs_samples.
        The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.
    
    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    .. [2] Chapelle, Olivier, and Lihong Li. "An empirical evaluation of thompson sampling."
           Advances in neural information processing systems. 2011.
    """
    def __init__(self, base_algorithm, nchoices, nsamples=10, beta_prior='auto', smoothing=None,
                 batch_train=False, refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, batch_sample_method='gamma',
                 random_state=None, njobs_arms=-1, njobs_samples=1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs_arms,
                                nchoices, batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state, assign_algo=False)
        self._add_bootstrapped_inputs(base_algorithm, batch_sample_method, nsamples, njobs_samples, None)

class LogisticUCB(_BasePolicyWithExploit):
    """
    Logistic Regression with Confidence Interval

    Logistic regression classifier which constructs an upper bound on the
    predicted probabilities through a confidence interval calculated from
    the variance-covariance matrix of the predictors.

    Note
    ----
    This strategy is implemented for comparison purposes only and it's not
    recommended to rely on it, particularly not for large datasets.

    Note
    ----
    This strategy does not support fitting the data in batches ('partial_fit'
    will not be available), nor does it support using any other classifier.
    See 'BootstrappedUCB' for a more generalizable version.

    Note
    ----
    This strategy requires each fitted classifier to store a square matrix with
    dimension equal to the number of features. Thus, memory consumption can grow
    very high with this method.

    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    percentile : int [0,100]
        Percentile of the confidence interval to take.
    fit_intercept : bool
        Whether to add an intercept term to the models.
    lambda_ : float
        Strenght of the L2 regularization. Must be greater than zero.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((5/nchoices, 4), 2)
        Note that it will only generate one random number per arm, so the 'a' parameters should be higher
        than for other methods.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, nchoices, percentile=80, fit_intercept=True, lambda_=1.0,
                 beta_prior='auto', smoothing=None,
                 assume_unique_reward=False,
                 random_state=None, njobs=-1):
        assert (percentile >= 0) and (percentile <= 100)
        assert lambda_ > 0.
        base = _LogisticUCB_n_TS_single(lambda_=float(lambda_),
                                        fit_intercept=fit_intercept,
                                        alpha=float(percentile) / 100.,
                                        ts=False)
        self._add_common_params(base, beta_prior, smoothing, njobs, nchoices,
                                False, None, False, assume_unique_reward,
                                random_state, assign_algo=True, prior_def_ucb=True)
        self.percentile = percentile

class LogisticTS(_BasePolicyWithExploit):
    """
    Logistic Regression with Thompson Sampling

    Logistic regression classifier which samples its coefficients using
    the the variance-covariance matrix of the predictors.

    Note
    ----
    This strategy is implemented for comparison purposes only and it's not
    recommended to rely on it, particularly not for large datasets.

    Note
    ----
    This strategy does not support fitting the data in batches ('partial_fit'
    will not be available), nor does it support using any other classifier.
    See 'BootstrappedTS' for a more generalizable version.

    Note
    ----
    This strategy requires each fitted model to store a square matrix with
    dimension equal to the number of features. Thus, memory consumption can grow
    very high with this method.

    Note
    ----
    Be aware that sampling coefficients is an operation that scales poorly with
    the number of columns/features/variables. For wide datasets, it might be
    slower than a bootstrapped approach, especially when using ``sample_unique=True``.

    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    multiplier : float
        Multiplier for the covariance matrix. Pass 1 to take it as-is.
    fit_intercept : bool
        Whether to add an intercept term to the models.
    lambda_ : float
        Strenght of the L2 regularization. Must be greater than zero.
    sample_unique : bool
        Whether to sample different coefficients each time a prediction is to
        be made. If passing 'False', when calling 'predict', it will sample
        the same coefficients for all the observations in the same call to
        'predict', whereas if passing 'True', will use a different set of
        coefficients for each observations. Passing 'False' leads to an
        approach which is theoretically wrong, but as sampling coefficients
        can be very slow, using 'False' can provide a reasonable speed up
        without much of a performance penalty.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((5/nchoices, 4), 2)
        Note that it will only generate one random number per arm, so the 'a' parameters should be higher
        than for other methods.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, nchoices, multiplier=1.0, fit_intercept=True,
                 lambda_=1.0, sample_unique = False,
                 beta_prior='auto', smoothing=None,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        warnings.warn("This class is experimental. Not recommended to rely on it.")
        assert lambda_ > 0.
        assert multiplier > 0.
        base = _LogisticUCB_n_TS_single(lambda_=lambda_,
                                        fit_intercept=fit_intercept,
                                        alpha=0.,
                                        m=multiplier,
                                        ts=True,
                                        sample_unique=sample_unique)
        self._add_common_params(base, beta_prior, smoothing, njobs, nchoices,
                                False, None, False, assume_unique_reward,
                                random_state, assign_algo=True, prior_def_ucb=False)

class SeparateClassifiers(_BasePolicy):
    """
    Separate Clasifiers per arm
    
    Fits one classifier per arm using only the data on which that arm was chosen.
    Predicts as One-Vs-Rest, plus the usual metaheuristics from ``beta_prior``
    and ``smoothing``.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, beta_prior=None, smoothing=None,
                 batch_train=False, refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state)
    
    def decision_function_std(self, X):
        """
        Get the predicted "probabilities" from each arm from the classifier that predicts it,
        standardized to sum up to 1 (note that these are no longer probabilities).
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            Data for which to obtain decision function scores for each arm.
        
        Returns
        -------
        scores : array (n_samples, n_choices)
            Scores following this policy for each arm.
        """
        X = _check_X_input(X)
        if not self.is_fitted:
            raise ValueError("Object has not been fit to data.")
        return self._oracles.predict_proba(X)
    
    def predict_proba_separate(self, X):
        """
        Get the predicted probabilities from each arm from the classifier that predicts it.
        
        Note
        ----
        Classifiers are all fit on different data, so the probabilities will not add up to 1.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            Data for which to obtain decision function scores for each arm.
        
        Returns
        -------
        scores : array (n_samples, n_choices)
            Scores following this policy for each arm.
        """
        X = _check_X_input(X)
        if not self.is_fitted:
            raise ValueError("Object has not been fit to data.")
        return self._oracles.predict_proba_raw(X)
    
    def predict(self, X, output_score = False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        output_score : bool
            Whether to output the score that this method predicted, in case it is desired to use
            it with this pakckage's offpolicy and evaluation modules.
            
        Returns
        -------
        pred : array (n_samples,) or dict("choice" : array(n_samples,), "score" : array(n_samples,))
            Actions chosen by the policy. If passing output_score=True, it will be a dictionary
            with the chosen arm and the score that the arm got following this policy with the classifiers used.
        """
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, output_score)

        scores = self.decision_function(X)
        pred = self._name_arms(np.argmax(scores, axis = 1))

        if not output_score:
            return pred
        else:
            score_max = np.max(scores, axis=1).reshape((-1, 1))
            return {"choice" : pred, "score" : score_max}

class EpsilonGreedy(_BasePolicy):
    """
    Epsilon Greedy
    
    Takes a random action with probability p, or the action with highest
    estimated reward with probability 1-p.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    explore_prob : float (0,1)
        Probability of taking a random action at each round.
    decay : float (0,1)
        After each prediction, the explore probability reduces to
        p = p*decay
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.
    
    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    .. [2] Yue, Yisong, et al. "The k-armed dueling bandits problem."
           Journal of Computer and System Sciences 78.5 (2012): 1538-1556.
    """
    def __init__(self, base_algorithm, nchoices, explore_prob=0.2, decay=0.9999,
                 beta_prior='auto', smoothing=None, batch_train=False,
                 refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state)
        assert (explore_prob>0) and (explore_prob<1)
        if decay is not None:
            assert (decay>0) and (decay<1)
            if decay <= .99:
                warnings.warn("Warning: 'EpsilonGreedy' has a very high decay rate.")
        self.explore_prob = explore_prob
        self.decay = decay
    
    def predict(self, X, exploit = False, output_score = False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
        output_score : bool
            Whether to output the score that this method predicted, in case it is desired to use
            it with this pakckage's offpolicy and evaluation modules.
            
        Returns
        -------
        pred : array (n_samples,) or dict("choice" : array(n_samples,), "score" : array(n_samples,))
            Actions chosen by the policy. If passing output_score=True, it will be a dictionary
            with the chosen arm and the score that the arm got following this policy with the classifiers used.
        """
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, output_score)
        scores = self.decision_function(X)
        pred = np.argmax(scores, axis = 1)
        if not exploit:
            ix_change_rnd = (self.random_state.random(size =  X.shape[0]) <= self.explore_prob)
            pred[ix_change_rnd] = self.random_state.integers(self.nchoices, size = ix_change_rnd.sum())
        pred = self._name_arms(pred)

        if self.decay is not None:
            self.explore_prob *= self.decay ** X.shape[0]
        
        if not output_score:
            return pred
        else:
            score_max = np.max(scores, axis = 1).reshape((-1, 1))
            score_max[ix_change_rnd] = 1 / self.nchoices
            return {"choice" : pred, "score" : score_max}

class _ActivePolicy(_BasePolicy):
    ### TODO: parallelize this in cython for the default case
    def _crit_active(self, X, pred, grad_crit):
        for choice in range(self.nchoices):
            if self._oracles.should_calculate_grad(choice) or self._force_fit:
                if (self._get_grad_norms == _get_logistic_grads_norms) and ("coef_" not in dir(self._oracles.algos[choice])):
                    grad_norms = \
                        self._rand_grad_norms(X,
                                              self._oracles.get_n_pos(choice),
                                              self._oracles.get_n_neg(choice),
                                              self._oracles.rng_arm[choice])
                else:
                    grad_norms = self._get_grad_norms(self._oracles.algos[choice], X, pred[:, choice])
            else:
                grad_norms = self._rand_grad_norms(X,
                                                   self._oracles.get_n_pos(choice),
                                                   self._oracles.get_n_neg(choice),
                                                   self._oracles.rng_arm[choice])

            if grad_crit == 'min':
                pred[:, choice] = grad_norms.min(axis = 1)
            elif grad_crit == 'max':
                pred[:, choice] = grad_norms.max(axis = 1)
            elif grad_crit == 'weighted':
                pred[:, choice] = np.einsum("i,ij->i", pred[:, choice], grad_norms)
            else:
                raise ValueError("Something went wrong. Please open an issue in GitHub indicating what you were doing.")
        return pred


class AdaptiveGreedy(_ActivePolicy):
    """
    Adaptive Greedy
    
    Takes the action with highest estimated reward, unless that estimation falls below a certain
    threshold, in which case it takes a an action either at random or according to an active learning
    heuristic (same way as `ActiveExplorer`).

    Note
    ----
    The hyperparameters here can make a large impact on the quality of the choices. Be sure
    to tune the threshold (or percentile), decay, and prior (or smoothing parameters).
    
    Note
    ----
    The threshold for the reward probabilities can be set to a hard-coded number, or
    to be calculated dynamically by keeping track of the predictions it makes, and taking
    a fixed percentile of that distribution to be the threshold.
    In the second case, these are calculated in separate batches rather than in a sliding window.
    
    The original idea was taken from the paper in the references and adapted to the
    contextual bandits setting like this. Can also be set to make choices in the same way as
    'ActiveExplorer' rather than random (see 'greedy_choice' parameter) when using logistic regression.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array, or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    window_size : int
        Number of predictions after which the threshold will be updated to the desired percentile.
    percentile : int in [0,100] or None
        Percentile of the predictions sample to set as threshold, below which actions are random.
        If None, will not take percentiles, will instead use the intial threshold and apply decay to it.
    decay : float (0,1) or None
        After each prediction, either the threshold or the percentile gets adjusted to:
            val_t+1 = val_t*decay
    decay_type : str, either 'percentile' or 'threshold'
        Whether to decay the threshold itself or the percentile of the predictions to take after
        each prediction. Ignored when using 'decay=None'. If passing 'percentile=None' and 'decay_type=percentile',
        will be forced to 'threshold'.
    initial_thr : str 'autho' or float (0,1)
        Initial threshold for the prediction below which a random action is taken.
        If set to 'auto', will be calculated as initial_thr = 1.5/nchoices.
        Note that if 'base_algorithm' has a 'decision_function' method, it will first apply a sigmoid function to the
        output, and then compare it to the threshold, so the threshold should lie between zero and one.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    active_choice : None or str in {'min', 'max', 'weighted'}
        How to select arms when predictions are below the threshold. If passing None, selects them at random (default).
        If passing 'min', 'max' or 'weighted', selects them in the same way as 'ActiveExplorer'.
        Non-random active selection requires being able to calculate gradients (gradients for logistic regression and linear regression (from this package)
        are already defined with an option 'auto' below).
    f_grad_norm : str 'auto' or function(base_algorithm, X, pred) -> array (n_samples, 2)
        Function that calculates the row-wise norm of the gradient from observations in X if their class were
        negative (first column) or positive (second column).
        The option 'auto' will only work with scikit-learn's 'LogisticRegression', 'SGDClassifier', and 'RidgeClassifier';
        with stochQN's 'StochasticLogisticRegression';
        and with this package's 'LinearRegression'.
    case_one_class : str 'auto', 'zero', None, or function(X, n_pos, n_neg, rng) -> array(n_samples, 2)
        If some arm/choice/class has only rewards of one type, many models will fail to fit, and consequently the gradients
        will be undefined. Likewise, if the model has not been fit, the gradient might also be undefined, and this requires a workaround.
        If passing None, will assume that 'base_algorithm' can be fit to data of only-positive or only-negative class without
        problems, and that it can calculate gradients and predictions with a 'base_algorithm' object that has not been fitted.
        If passing a function, will take the output of it as the row-wise gradient norms when it compares them against other
        arms/classes, with the first column having the values if the observations were of negative class, and the second column if they
        were positive class. The other inputs to this function are the number of positive and negative examples that have been observed, and a ``Generator``
        object from NumPy to use for generating random numbers.
        If passing 'auto', will generate random numbers:

            negative: ~ Gamma(log10(n_features) / (n_pos+1)/(n_pos+n_neg+2), log10(n_features)).

            positive: ~ Gamma(log10(n_features) * (n_pos+1)/(n_pos+n_neg+2), log10(n_features)).

        If passing 'zero', it will output zero whenever models have not been fitted.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.
    
    References
    ----------
    .. [1] Chakrabarti, Deepayan, et al. "Mortal multi-armed bandits."
           Advances in neural information processing systems. 2009.
    .. [2] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, window_size=500, percentile=35, decay=0.9998,
                 decay_type='percentile', initial_thr='auto', beta_prior='auto', smoothing=None,
                 batch_train=False, refit_buffer=None,  deep_copy_buffer=True,
                 assume_unique_reward=False, active_choice=None, f_grad_norm='auto',
                 case_one_class='auto', random_state=None, njobs=-1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state)
        
        assert isinstance(window_size, int)
        if percentile is not None:
            assert isinstance(percentile, int)
            assert (percentile > 0) and (percentile < 100)
        if initial_thr == 'auto':
            initial_thr = 1.0 / (np.sqrt(nchoices) * 2.0)
        assert isinstance(initial_thr, float)
        assert window_size > 0
        self.window_size = window_size
        self.percentile = percentile
        self.thr = initial_thr
        self.window_cnt = 0
        self.window = np.array([])
        assert (decay_type == 'threshold') or (decay_type == 'percentile')
        if (decay_type == 'percentile') and (percentile is None):
            decay_type = 'threshold'
        self.decay_type = decay_type
        if decay is not None:
            assert (decay >= 0.0) and (decay <= 1.0)
        if (decay_type == 'percentile') and (percentile is None):
            decay = 1
        self.decay = decay

        if active_choice is not None:
            assert active_choice in ['min', 'max', 'weighted']
            _check_active_inp(self, base_algorithm, f_grad_norm, case_one_class)
        self.active_choice = active_choice
        self._force_counters = self.active_choice is not None

    def predict(self, X, exploit = False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
            
        Returns
        -------
        pred : array (n_samples,)
            Actions chosen by the policy.
        """
        # TODO: add option to output scores
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, False)
        return self._name_arms(self._predict(X, exploit))
    
    def _predict(self, X, exploit = False):
        X = _check_X_input(X)
        
        if X.shape[0] == 0:
            return np.array([])
        
        if exploit:
            return self._oracles.predict(X)
        
        # fixed threshold, anything below is always random
        if (self.decay == 1) or (self.decay is None):
            pred, pred_max = self._calc_preds(X)

        # variable threshold that needs to be updated
        else:
            remainder_window = self.window_size - self.window_cnt
            
            # case 1: number of predictions to make would still fit within current window
            if remainder_window > X.shape[0]:
                pred, pred_max = self._calc_preds(X)
                self.window_cnt += X.shape[0]
                self.window = np.r_[self.window, pred_max]
                
                # apply decay for all observations
                self._apply_decay(X.shape[0])

            # case 2: number of predictions to make would span more than current window
            else:
                # predict for the remainder of this window
                pred, pred_max = self._calc_preds(X[:remainder_window, :])
                
                # allocate the rest that don't fit in this window
                pred_all = np.zeros(X.shape[0])
                pred_all[:remainder_window] = pred
                
                # complete window, update percentile if needed
                self.window = np.r_[self.window, pred_max]
                if self.decay_type == 'percentile':
                    self.thr = np.percentile(self.window, self.percentile)

                # reset window
                self.window = np.array([])
                self.window_cnt = 0
                
                # decay threshold only for these observations
                self._apply_decay(remainder_window)
                
                # predict the rest recursively
                pred_all[remainder_window:] = self.predict(X[remainder_window:, :])
                return pred_all
                
        return pred

    def _apply_decay(self, nobs):
        if (self.decay is not None) and (self.decay != 1):
            if self.decay_type == 'threshold':
                self.thr *= self.decay ** nobs
            elif self.decay_type == 'percentile':
                self.percentile *= self.decay ** nobs
            else:
                raise ValueError("'decay_type' must be one of 'threshold' or 'percentile'")

    def _calc_preds(self, X):
        pred_proba = self._oracles.decision_function(X)
        pred_max = pred_proba.max(axis = 1)
        pred = np.argmax(pred_proba, axis = 1)
        set_greedy = pred_max <= self.thr
        if np.any(set_greedy):
            self._choose_greedy(set_greedy, X, pred, pred_proba)
        return pred, pred_max

    def _choose_greedy(self, set_greedy, X, pred, pred_all):
        if self.active_choice is None:
            pred[set_greedy] = self.random_state.integers(self.nchoices, size = set_greedy.sum())
        else:
            pred[set_greedy] = np.argmax(
                self._crit_active(
                    X[set_greedy],
                    pred_all[set_greedy],
                    self.active_choice),
                axis = 1)

class ExploreFirst(_BasePolicy):
    """
    Explore First, a.k.a. Explore-Then-Exploit
    
    Selects random actions for the first N predictions, after which it selects the
    best arm only, according to its estimates.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    explore_rounds : int
        Number of rounds to wait before exploitation mode.
        Will switch after making N predictions.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, explore_rounds=2500,
                 beta_prior=None, smoothing=None, batch_train=False,
                 refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state)
        
        assert explore_rounds>0
        assert isinstance(explore_rounds, int)
        self.explore_rounds = explore_rounds
        self.explore_cnt = 0

    def predict(self, X, exploit = False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
            
        Returns
        -------
        pred : array (n_samples,)
            Actions chosen by the policy.
        """
        # TODO: add option to output scores
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, False)
        return self._name_arms(self._predict(X, exploit))
    
    def _predict(self, X, exploit = False):
        X = _check_X_input(X)
        
        if X.shape[0] == 0:
            return np.array([])
        
        if exploit:
            return self._oracles.predict(X)
        
        if self.explore_cnt < self.explore_rounds:
            self.explore_cnt += X.shape[0]
            
            # case 1: all predictions are within allowance
            if self.explore_cnt <= self.explore_rounds:
                return self.random_state.integers(self.nchoices, size = X.shape[0])
            
            # case 2: some predictions are within allowance, others are not
            else:
                n_explore = self.explore_rounds - self.explore_cnt + X.shape[0]
                pred = np.empty(X.shape[0], type = np.float64)
                pred[:n_explore] = self.random_state.integers(self.nchoices, n_explore)
                pred[n_explore:] = self._oracles.predict(X[n_explore:])
                return pred
        else:
            return self._oracles.predict(X)

class ActiveExplorer(_ActivePolicy):
    """
    Active Explorer
    
    Selects a proportion of actions according to an active learning heuristic based on gradient.
    Works only for differentiable and preferably smooth functions.
    
    Note
    ----
    Here, for the predictions that are made according to an active learning heuristic
    (these are selected at random, just like in Epsilon-Greedy), the guiding heuristic
    is the gradient that the observation, having either label (either weighted by the estimted
    probability, or taking the maximum or minimum), would produce on each model that
    predicts a class, given the current coefficients for that model. This of course requires
    being able to calculate gradients - package comes with pre-defined gradient functions for
    linear and logistic regression, and allows passing custom functions for others.
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1
            2) A 'decision_function' method with unbounded outputs (n_samples,) to which it will apply a sigmoid function.
            3) A 'predict' method with outputs (n_samples,) with values in [0,1].
        Can also pass a list with a different (or already-fit) classifier for each arm.
    f_grad_norm : str 'auto' or function(base_algorithm, X, pred) -> array (n_samples, 2)
        Function that calculates the row-wise norm of the gradient from observations in X if their class were
        negative (first column) or positive (second column).
        The option 'auto' will only work with scikit-learn's 'LogisticRegression', 'SGDClassifier' (log-loss only), and 'RidgeClassifier';
        with stochQN's 'StochasticLogisticRegression';
        and with this package's 'LinearRegression'.
    case_one_class : str 'auto', 'zero', None, or function(X, n_pos, n_neg, rng) -> array(n_samples, 2)
        If some arm/choice/class has only rewards of one type, many models will fail to fit, and consequently the gradients
        will be undefined. Likewise, if the model has not been fit, the gradient might also be undefined, and this requires a workaround.
        If passing None, will assume that 'base_algorithm' can be fit to data of only-positive or only-negative class without
        problems, and that it can calculate gradients and predictions with a 'base_algorithm' object that has not been fitted.
        If passing a function, will take the output of it as the row-wise gradient norms when it compares them against other
        arms/classes, with the first column having the values if the observations were of negative class, and the second column if they
        were positive class. The other inputs to this function are the number of positive and negative examples that have been observed, and a ``Generator``
        object from NumPy to use for generating random numbers.
        If passing 'auto', will generate random numbers:

            negative: ~ Gamma(log10(n_features) / (n_pos+1)/(n_pos+n_neg+2), log10(n_features)).

            positive: ~ Gamma(log10(n_features) * (n_pos+1)/(n_pos+n_neg+2), log10(n_features)).

        If passing 'zero', it will output zero whenever models have not been fitted.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    explore_prob : float (0,1)
        Probability of selecting an action according to active learning criteria.
    decay : float (0,1)
        After each prediction, the probability of selecting an arm according to active
        learning criteria is set to p = p*decay
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, f_grad_norm='auto', case_one_class='auto',
                 explore_prob=.15, decay=0.9997, beta_prior='auto', smoothing=None,
                 batch_train=False, refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        _check_active_inp(self, base_algorithm, f_grad_norm, case_one_class)
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state, assign_algo=False)

        if self.batch_train:
            base_algorithm = _add_method_predict_robust(base_algorithm)
        self.base_algorithm = base_algorithm
        
        assert isinstance(explore_prob, float)
        assert (explore_prob > 0) and (explore_prob < 1)
        self.explore_prob = explore_prob
        self.decay = decay
        self._force_counters = True
    
    def predict(self, X, exploit=False, gradient_calc='weighted'):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
        gradient_calc : str, one of 'weighted', 'max' or 'min'
            How to calculate the gradient that an observation would have on the loss
            function for each classifier, given that it could be either class (positive or negative)
            for the classifier that predicts each arm. If weighted, they are weighted by the same
            probability estimates from the base algorithm.
            
        Returns
        -------
        pred : array (n_samples,)
            Actions chosen by the policy.
        """
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, False)
        X = _check_X_input(X)
        
        pred = self._oracles.decision_function(X)
        if not exploit:
            change_greedy = self.random_state.random(size=X.shape[0]) <= self.explore_prob
            if np.any(change_greedy):
                pred[change_greedy, :] = self._crit_active(X[change_greedy, :], pred[change_greedy, :], gradient_calc)
            
            if self.decay is not None:
                self.explore_prob *= self.decay ** X.shape[0]
        
        return self._name_arms(np.argmax(pred, axis = 1))

class SoftmaxExplorer(_BasePolicy):
    """
    SoftMax Explorer
    
    Selects an action according to probabilites determined by a softmax transformation
    on the scores from the decision function that predicts each class.

    Note
    ----
    Will apply an inverse sigmoid transformations to the probabilities that come from the base algorithm
    before applying the softmax function.
    
    
    Parameters
    ----------
    base_algorithm : obj
        Base binary classifier for which each sample for each class will be fit.
        Will look for, in this order:
            1) A 'predict_proba' method with outputs (n_samples, 2), values in [0,1], rows suming to 1, to which it
               will apply an inverse sigmoid function.
            2) A 'decision_function' method with unbounded outputs (n_samples,).
            3) A 'predict' method outputting (n_samples,), values in [0,1], to which it will apply an inverse sigmoid function.
        Can also pass a list with a different (or already-fit) classifier for each arm.
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    multiplier : float or None
        Number by which to multiply the outputs from the base algorithm before applying the softmax function
        (i.e. will take softmax(yhat * multiplier)).
    inflation_rate : float or None
        Number by which to multiply the multipier rate after every prediction, i.e. after making
        't' predictions, the multiplier will be 'multiplier_t = multiplier * inflation_rate^t'.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    batch_train : bool
        Whether the base algorithm will be fit to the data in batches as it comes (online),
        or to the whole dataset each time it is refit. Requires a classifier with a
        'partial_fit' method.
    refit_buffer : int or None
        Number of observations per arm to keep as a reserve for passing to
        'partial_fit'. If passing it, up until the moment there are at least this
        number of observations for a given arm, that arm will keep the observations
        when calling 'fit' and 'partial_fit', and will translate calls to
        'partial_fit' to calls to 'fit' with the new plus stored observations.
        After the reserve number is reached, calls to 'partial_fit' will enlarge
        the data batch with the stored observations, and old stored observations
        will be gradually replaced with the new ones (at random, not on a FIFO
        basis). This technique can greatly enchance the performance when fitting
        the data in batches, but memory consumption can grow quite large.
        Calls to 'fit' will override this reserve.
        Ignored when passing 'batch_train=False'.
    deep_copy_buffer : bool
        Whether to make deep copies of the data that is stored in the
        reserve for ``refit_buffer``. If passing 'False', when the reserve is
        not yet full, these will only store shallow copies of the data, which
        is faster but will not let Python's garbage collector free memory
        after deleting the data, and if the orinal data is overwritten, so will
        this buffer.
        Ignored when not using ``refit_buffer``.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Note that if the base algorithm is itself parallelized,
        this might result in a slowdown as both compete for available threads, so don't set
        parallelization in both. The parallelization uses shared memory, thus you will only
        see a speed up if your base classifier releases the Python GIL, and will
        otherwise result in slower runs.

    References
    ----------
    .. [1] Cortes, David. "Adapting multi-armed bandits policies to contextual bandits scenarios."
           arXiv preprint arXiv:1811.04383 (2018).
    """
    def __init__(self, base_algorithm, nchoices, multiplier=1.0, inflation_rate=1.0004,
                 beta_prior='auto', smoothing=None, batch_train=False,
                 refit_buffer=None, deep_copy_buffer=True,
                 assume_unique_reward=False, random_state=None, njobs=-1):
        self._add_common_params(base_algorithm, beta_prior, smoothing, njobs, nchoices,
                                batch_train, refit_buffer, deep_copy_buffer,
                                assume_unique_reward, random_state)

        if multiplier is not None:
            if isinstance(multiplier, int):
                multiplier = float(multiplier)
            assert multiplier > 0
        else:
            multiplier = None
        if inflation_rate is not None:
            if isinstance(inflation_rate, int):
                inflation_rate = float(inflation_rate)
            assert inflation_rate > 0
        self.multiplier = multiplier
        self.inflation_rate = inflation_rate
    
    def decision_function(self, X, output_score=False, apply_sigmoid_score=True):
        """
        Get the scores for each arm following this policy's action-choosing criteria.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            Data for which to obtain decision function scores for each arm.
        
        Returns
        -------
        scores : array (n_samples, n_choices)
            Scores following this policy for each arm.
        """
        X = _check_X_input(X)
        if not self.is_fitted:
            raise ValueError("Object has not been fit to data.")
        return self._oracles.predict_proba(X)
    
    def predict(self, X, exploit=False, output_score=False):
        """
        Selects actions according to this policy for new data.
        
        Parameters
        ----------
        X : array (n_samples, n_features)
            New observations for which to choose an action according to this policy.
        exploit : bool
            Whether to make a prediction according to the policy, or to just choose the
            arm with the highest expected reward according to current models.
        output_score : bool
            Whether to output the score that this method predicted, in case it is desired to use
            it with this pakckage's offpolicy and evaluation modules.
            
        Returns
        -------
        pred : array (n_samples,) or dict("choice" : array(n_samples,), "score" : array(n_samples,))
            Actions chosen by the policy. If passing output_score=True, it will be a dictionary
            with the chosen arm and the score that the arm got following this policy with the classifiers used.
        """
        if not self.is_fitted:
            return self._predict_random_if_unfit(X, output_score)
        if exploit:
            X = _check_X_input(X)
            return np.argmax(self._oracles.decision_function(X), axis=1)
        pred = self.decision_function(X)
        _apply_inverse_sigmoid(pred)
        if self.multiplier is not None:
            pred *= self.multiplier
            if self.inflation_rate is not None:
                self.multiplier *= self.inflation_rate ** pred.shape[0]
        _apply_softmax(pred)
        chosen =  _choice_over_rows(pred, self.random_state, self.njobs)

        if output_score:
            score_chosen = pred[np.arange(pred.shape[0]), chosen]
        chosen = self._name_arms(chosen)

        if not output_score:
            return chosen
        else:
            return {"choice" : chosen, "score" : score_chosen}


class LinUCB(_BasePolicyWithExploit):
    """
    LinUCB

    Note
    ----
    This strategy requires each fitted model to store a square matrix with
    dimension equal to the number of features. Thus, memory consumption can grow
    very high with this method.

    Note
    ----
    The 'X' data (covariates) should ideally be centered before passing them
    to 'fit', 'partial_fit', 'predict'.
    
    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    alpha : float
        Parameter to control the upper confidence bound (more is higher).
    lambda_ : float > 0
        Regularization parameter. References assumed this would always be equal to 1, but this
        implementation allows to change it.
    fit_intercept : bool
        Whether to add an intercept term to the coefficients.
    use_float : bool
        Whether to use C 'float' type for the required matrices. If passing 'False',
        will use C 'double'. Be aware that memory usage for this model can grow
        very large.
    method : str, one of 'chol' or 'sm'
        Method used to fit the model. Options are:

        ``'chol'``:
            Uses the Cholesky decomposition to solve the linear system from the
            least-squares closed-form each time 'fit' or 'partial_fit' is called.
            This is likely to be faster when fitting the model to a large number
            of observations at once, and is able to better exploit multi-threading.
        ``'sm'``:
            Starts with an inverse diagonal matrix and updates it as each
            new observation comes using the Sherman-Morrison formula, thus
            never explicitly solving the linear system, nor needing to calculate
            a matrix inverse. This is likely to be faster when fitting the model
            to small batches of observations. Be aware that with this method, it
            will add regularization to the intercept if passing 'fit_intercept=True'.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((5/nchoices, 4), 2)
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
        Note that it is technically incorrect to apply smoothing like this (because
        the predictions from models are not bounded between zero and one), but
        if neither ``beta_prior``, nor ``smoothing`` are passed, the policy can get
        stuck in situations in which it will only choose actions from the first batch
        of observations to which it is fit.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.
    
    References
    ----------
    .. [1] Chu, Wei, et al. "Contextual bandits with linear payoff functions."
           Proceedings of the Fourteenth International Conference on Artificial Intelligence and Statistics. 2011.
    .. [2] Li, Lihong, et al. "A contextual-bandit approach to personalized news article recommendation."
           Proceedings of the 19th international conference on World wide web. ACM, 2010.
    """
    def __init__(self, nchoices, alpha=1.0, lambda_=1.0, fit_intercept=True,
                 use_float=True, method="sm",
                 beta_prior=None, smoothing=None, assume_unique_reward=False,
                 random_state=None, njobs=1):
        self._ts = False
        self._add_common_lin(alpha, lambda_, fit_intercept, use_float, method, nchoices, njobs)
        base = _LinUCB_n_TS_single(alpha=self.alpha, lambda_=self.lambda_,
                                   fit_intercept=self.fit_intercept,
                                   use_float=self.use_float, method=self.method,
                                   ts=False)
        self._add_common_params(base, beta_prior, smoothing, njobs, nchoices,
                                True, None, False, assume_unique_reward,
                                random_state, assign_algo=True, prior_def_ucb=True)

    def _add_common_lin(self, alpha, lambda_, fit_intercept, use_float, method, nchoices, njobs):
        if isinstance(alpha, int):
            alpha = float(alpha)
        assert isinstance(alpha, float)
        if isinstance(lambda_, int):
            lambda_ = float(lambda_)
        assert lambda_ >= 0.
        assert method in ["chol", "sm"]

        self.alpha = alpha
        self.lambda_ = lambda_
        self.fit_intercept = bool(fit_intercept)
        self.use_float = bool(use_float)
        self.method = method
        if self._ts:
            self.v_sq = self.alpha
            del self.alpha

class LinTS(LinUCB):
    """
    LinUCB

    Note
    ----
    This strategy requires each fitted model to store a square matrix with
    dimension equal to the number of features. Thus, memory consumption can grow
    very high with this method.

    Note
    ----
    The 'X' data (covariates) should ideally be centered before passing them
    to 'fit', 'partial_fit', 'predict'.

    Note
    ----
    Be aware that sampling coefficients is an operation that scales poorly with
    the number of columns/features/variables. For wide datasets, it might be
    slower than a bootstrapped approach, especially when using ``sample_unique=True``.
    
    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    v_sq : float
        Parameter by which to multiply the covariance matrix (more means higher variance).
    lambda_ : float > 0
        Regularization parameter. References assumed this would always be equal to 1, but this
        implementation allows to change it.
    fit_intercept : bool
        Whether to add an intercept term to the coefficients.
    sample_unique : bool
        Whether to sample different coefficients each time a prediction is to
        be made. If passing 'False', when calling 'predict', it will sample
        the same coefficients for all the observations in the same call to
        'predict', whereas if passing 'True', will use a different set of
        coefficients for each observations. Passing 'False' leads to an
        approach which is theoretically wrong, but as sampling coefficients
        can be very slow, using 'False' can provide a reasonable speed up
        without much of a performance penalty.
    use_float : bool
        Whether to use C 'float' type for the required matrices. If passing 'False',
        will use C 'double'. Be aware that memory usage for this model can grow
        very large.
    method : str, one of 'chol' or 'sm'
        Method used to fit the model. Options are:

        ``'chol'``:
            Uses the Cholesky decomposition to solve the linear system from the
            least-squares closed-form each time 'fit' or 'partial_fit' is called.
            This is likely to be faster when fitting the model to a large number
            of observations at once, and is able to better exploit multi-threading.
        ``'sm'``:
            Starts with an inverse diagonal matrix and updates it as each
            new observation comes using the Sherman-Morrison formula, thus
            never explicitly solving the linear system, nor needing to calculate
            a matrix inverse. This is likely to be faster when fitting the model
            to small batches of observations. Be aware that with this method, it
            will add regularization to the intercept if passing 'fit_intercept=True'.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
        Note that it is technically incorrect to apply smoothing like this (because
        the predictions from models are not bounded between zero and one), but
        if neither ``beta_prior``, nor ``smoothing`` are passed, the policy can get
        stuck in situations in which it will only choose actions from the first batch
        of observations to which it is fit.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.
    
    References
    ----------
    .. [1] Agrawal, Shipra, and Navin Goyal.
           "Thompson sampling for contextual bandits with linear payoffs."
           International Conference on Machine Learning. 2013.
    """
    def __init__(self, nchoices, v_sq=1.0, lambda_=1.0, fit_intercept=True,
                 sample_unique=False, use_float=True, method="sm",
                 beta_prior=None, smoothing=None, assume_unique_reward=False,
                 random_state=None, njobs = 1):
        self._ts = True
        self._add_common_lin(v_sq, lambda_, fit_intercept, use_float, method, nchoices, njobs)
        base = _LinUCB_n_TS_single(alpha=self.v_sq, lambda_=self.lambda_,
                                   fit_intercept=self.fit_intercept,
                                   use_float=self.use_float, method=self.method,
                                   ts=True, sample_unique=sample_unique)
        self._add_common_params(base, beta_prior, smoothing, njobs, nchoices,
                                True, None, False, assume_unique_reward,
                                random_state, assign_algo=True, prior_def_ucb=False)

class BayesianUCB(_BasePolicyWithExploit):
    """
    Bayesian Upper Confidence Bound
    
    Gets an upper confidence bound by Bayesian Logistic Regression estimates.
    
    Note
    ----
    The implementation here uses PyMC3's GLM formula with either MCMC sampling
    or ADVI. This is a very, very slow implementation, and will probably take at
    least two or three orders or magnitude more to fit compared to other methods. It's not advised to use it unless having a very good GPU that PyMC3 could use.
    
    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    percentile : int [0,100]
        Percentile of the predictions sample to take.
    method : str, either 'advi', 'nuts', or 'metropolis'
        Method used to sample coefficients (see PyMC3's documentation for details).
    n_samples : int
        Number of samples to take when making predictions.
    n_iter : int or str 'auto'
        Number of iterations when using ADVI, or number of draws when using NUTS. Note that, when using NUTS,
        will still first draw a burn-out or tuning 500 samples before 'niter' more have been produced.
        If passing 'auto', will use 5000 for ADVI, 10000 for NUTS, and 25000 for
        Metropolis, but this might me insufficient, especially for large datasets.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((5/nchoices, 4), 2)
        Note that it will only generate one random number per arm, so the 'a' parameters should be higher
        than for other methods.
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.
    """
    def __init__(self, nchoices, percentile=80, method='advi', n_samples=50, n_iter='auto',
                 beta_prior='auto', smoothing=None,
                 assume_unique_reward=False, random_state=None, njobs=1):
        warnings.warn("This strategy is experimental and will be extremely slow. Do not rely on it.")
        ## NOTE: this is a really slow and poorly thought implementation
        ## TODO: rewrite using some faster framework such as Edward,
        ##       or with a hard-coded coordinate ascent procedure instead. 
        ## TODO: add a 'partial_fit' with stochastic variational inference.
        self._add_common_params(_ZeroPredictor(), beta_prior, smoothing, njobs, nchoices,
                                False, None, False, assume_unique_reward,
                                random_state, assign_algo=False, prior_def_ucb=True)
        assert (percentile >= 0) and (percentile <= 100)
        self.percentile = percentile
        self.n_iter, self.n_samples = _check_bay_inp(method, n_iter, n_samples)
        self.method = method
        self.base_algorithm = _BayesianLogisticRegression(
                    method = self.method, niter = self.n_iter,
                    nsamples = self.n_samples, mode = 'ucb', perc = self.percentile)
        self.batch_train = False


class BayesianTS(_BasePolicyWithExploit):
    """
    Bayesian Thompson Sampling
    
    Performs Thompson Sampling by sampling a set of Logistic Regression coefficients
    from each class, then predicting the class with highest estimate.

    Note
    ----
    The implementation here uses PyMC3's GLM formula with either MCMC sampling
    or ADVI. This is a very, very slow implementation, and will probably take at
    least two or three orders or magnitude more to fit compared to other methods. It's not advised to use it unless having a very good GPU that PyMC3 could use.

    Note
    ----
    Unlike the other Thompson sampling classes, this class
    does not offer the option 'sample_unique' - it's equivalent to
    always having `False` for that parameter in the other methods.
    
    Parameters
    ----------
    nchoices : int or list-like
        Number of arms/labels to choose from. Can also pass a list, array or series with arm names, in which case
        the outputs from predict will follow these names and arms can be dropped by name, and new ones added with a
        custom name.
    method : str, either 'advi', 'nuts', or 'metropolis'
        Method used to sample coefficients (see PyMC3's documentation for details).
    n_samples : int
        Number of samples to take when making predictions.
    n_iter : int or str 'auto'
        Number of iterations when using ADVI, or number of draws when using NUTS. Note that, when using NUTS,
        will still first draw a burn-out or tuning 500 samples before 'niter' more have been produced.
        If passing 'auto', will use 5000 for ADVI, 10000 for NUTS, and 25000 for
        Metropolis, but this might me insufficient, especially for large datasets.
    beta_prior : str 'auto', None, or tuple ((a,b), n)
        If not None, when there are less than 'n' positive samples from a class
        (actions from that arm that resulted in a reward), it will predict the score
        for that class as a random number drawn from a beta distribution with the prior
        specified by 'a' and 'b'. If set to auto, will be calculated as:
        beta_prior = ((3/nchoices, 4), 2)
    smoothing : None or tuple (a,b)
        If not None, predictions will be smoothed as yhat_smooth = (yhat*n + a)/(n + b),
        where 'n' is the number of times each arm was chosen in the training data.
        This will not work well with non-probabilistic classifiers such as SVM, in which case you might
        want to define a class that embeds it with some recalibration built-in.
        Recommended to use only one of 'beta_prior' or 'smoothing'.
    assume_unique_reward : bool
        Whether to assume that only one arm has a reward per observation. If set to True,
        whenever an arm receives a reward, the classifiers for all other arms will be
        fit to that observation too, having negative label.
    random_state : int, None, RandomState, or Generator
        Either an integer which will be used as seed for initializing a
        ``RandomState`` object for random number generation, a ``RandomState``
        object (from NumPy) from which to draw an integer, or a ``Generator``
        object (from NumPy), which will be used directly.
        Passing 'None' will make the resulting object fail to pickle,
        but alternatives such as dill can still serialize them.
        While this controls random number generation for this meteheuristic,
        there can still be other sources of variations upon re-runs, such as
        data aggregations in parallel (e.g. from OpenMP or BLAS functions).
    njobs : int or None
        Number of parallel jobs to run. If passing None will set it to 1. If passing -1 will
        set it to the number of CPU cores. Be aware that the algorithm will use BLAS function calls,
        and if these have multi-threading enabled, it might result in a slow-down
        as both functions compete for available threads.
    """
    def __init__(self, nchoices, method='advi', n_samples=50, n_iter='auto',
                 beta_prior='auto', smoothing=None,
                 assume_unique_reward=False, random_state=None, njobs=1):
        warnings.warn("This strategy is experimental and will be extremely slow. Do not rely on it.")

        ## NOTE: this is a really slow and poorly thought implementation
        ## TODO: rewrite using some faster framework such as Edward,
        ##       or with a hard-coded coordinate ascent procedure instead. 
        ## TODO: add a 'partial_fit' with stochastic variational inference.
        self._add_common_params(_ZeroPredictor(), beta_prior, smoothing, njobs, nchoices,
                                False, None, False, assume_unique_reward,
                                random_state, assign_algo=False)
        self.nchoices = nchoices
        self.n_iter, self.n_samples = _check_bay_inp(method, n_iter, n_samples)
        self.method = method
        self.base_algorithm = _BayesianLogisticRegression(
                    method = self.method, niter = self.n_iter,
                    nsamples = self.n_samples, mode = 'ts')
        self.batch_train = False
