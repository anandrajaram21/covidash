from math import sqrt
from scipy.special import xlogy
from scipy.stats import gmean
from scipy import stats
import numpy as np
import warnings
import json
import datetime

import matplotlib.pyplot as plt


EPS = 1e-10  # epsilon


class FindErrors(object):
    """
    Presents about 100 performance metrics related to sequence data at one place.

     actual: ture/observed values, 1D array or list
     predicted: simulated values, 1D array or list

     The following attributes are dynamic i.e. they can be changed from outside the class. This means the user can
     change their value after creating the class. This will be useful if we want to calculate an error once by ignoring
     NaN and then by not ignoring the NaNs. However, the user has to run the method `treat_arrays` in order to have the
     changed values impact on true and predicted arrays.

     replace_nan: float/int, default None, if not None, then NaNs in true and predicted will be replaced by this value.
     replace_inf: float/int, default None, if not None, then inf vlaues in true and predicted will be replaced by this
                  value.
     remove_zero: bool, default False, if True, the zero values in true or predicted arrays will be removed. If a zero
                  is found in one array, the corresponding value in the other array will also be removed.
     remove_neg: bool, default False, if True, the negative values in true or predicted arrays will be removed.
    """

    def __init__(
        self,
        actual,
        predicted,
        replace_nan=None,
        replace_inf=None,
        remove_zero=False,
        remove_neg=False,
    ):

        self.true, self.predicted = self._pre_process(actual, predicted)
        self.replace_nan = replace_nan
        self.replace_inf = replace_inf
        self.remove_zero = remove_zero
        self.remove_neg = remove_neg
        self.all_methods = [
            method
            for method in dir(self)
            if callable(getattr(self, method))
            if not method.startswith("_")
            if method not in ["calculate_all", "stats", "plot1d", "treat_arrays"]
        ]

        # if arrays contain negative values, following three errors can not be computed
        for array in [self.true, self.predicted]:

            assert len(array) > 0, "Input arrays should not be empty"

            if len(array[array < 0.0]) > 0:
                self.all_methods = [
                    m
                    for m in self.all_methods
                    if m
                    not in (
                        "mean_gamma_deviance",
                        "mean_poisson_deviance",
                        "mean_square_log_error",
                    )
                ]
            if (array <= 0).any():  # mean tweedie error is not computable
                self.all_methods = [
                    m
                    for m in self.all_methods
                    if m not in ("mean_gamma_deviance", "mean_poisson_deviance")
                ]

    @property
    def replace_nan(self):
        return self._replace_nan

    @replace_nan.setter
    def replace_nan(self, x):
        self._replace_nan = x

    @property
    def replace_inf(self):
        return self._replace_inf

    @replace_inf.setter
    def replace_inf(self, x):
        self._replace_inf = x

    @property
    def remove_zero(self):
        return self._remove_zero

    @remove_zero.setter
    def remove_zero(self, x):
        self._remove_zero = x

    @property
    def remove_neg(self):
        return self._remove_neg

    @remove_neg.setter
    def remove_neg(self, x):
        self._remove_neg = x

    def _pre_process(self, true, predicted):

        predicted = self._assert_1darray(predicted)
        true = self._assert_1darray(true)
        assert len(predicted) == len(
            true
        ), "lengths of provided arrays mismatch, predicted array: {}, true array: {}".format(
            len(predicted), len(true)
        )

        return true, predicted

    def _assert_1darray(self, array_like) -> np.ndarray:
        """Makes sure that the provided `array_like` is 1D numpy array"""
        if not isinstance(array_like, np.ndarray):
            if not isinstance(array_like, list):
                # it can be pandas series or datafrmae
                if array_like.__class__.__name__ in ["Series", "DataFrame"]:
                    if (
                        len(array_like.shape) > 1
                    ):  # 1d series has shape (x,) while 1d dataframe has shape (x,1)
                        if array_like.shape[1] > 1:  # it is a 2d datafrmae
                            raise TypeError(
                                "only 1d pandas Series or dataframe are allowed"
                            )
                    np_array = np.array(array_like).reshape(
                        -1,
                    )
                else:
                    raise TypeError(
                        f"all inputs must be numpy array or list but one is of type {type(array_like)}"
                    )
            else:
                np_array = np.array(array_like).reshape(
                    -1,
                )
        else:
            # maybe the dimension is >1 so make sure it is more
            np_array = array_like.reshape(
                -1,
            )

        assert len(np_array.shape) == 1
        return np_array

    def calculate_all(self, statistics=False, verbose=False, write=False, name=None):
        """calculates errors using all available methods except brier_score..
        write: bool, if True, will write the calculated errors in file.
        name: str, if not None, then must be path of the file in which to write."""
        errors = {}
        for m in self.all_methods:
            if m not in ["brier_score"]:
                try:
                    error = float(getattr(self, m)())
                except TypeError:  # some errors might not have been computed and returned a non float-convertible value e.g. None
                    error = getattr(self, m)()
                errors[m] = error
                if verbose:
                    if error is None:
                        print("{0:25} :  {1}".format(m, error))
                    else:
                        print("{0:25} :  {1:<12.3f}".format(m, error))

        if statistics:
            errors["stats"] = self.stats(verbose=verbose)

        if write:
            if name is not None:
                assert isinstance(name, str)
                fname = name
            else:
                fname = str(datetime.now())

            with open(fname + ".json", "w") as fp:
                json.dump(errors, fp, sort_keys=True, indent=4)

        return errors

    def _error(self, true=None, predicted=None):
        """ simple difference """
        if true is None:
            true = self.true
        if predicted is None:
            predicted = self.predicted
        return true - predicted

    def _percentage_error(self):
        """
        Percentage error
        """
        return self._error() / (self.true + EPS) * 100

    def _naive_prognose(self, seasonality: int = 1):
        """ Naive forecasting method which just repeats previous samples """
        return self.true[:-seasonality]

    def _relative_error(self, benchmark: np.ndarray = None):
        """ Relative Error """
        if benchmark is None or isinstance(benchmark, int):
            # If no benchmark prediction provided - use naive forecasting
            if not isinstance(benchmark, int):
                seasonality = 1
            else:
                seasonality = benchmark
            return self._error(
                self.true[seasonality:], self.predicted[seasonality:]
            ) / (
                self._error(self.true[seasonality:], self._naive_prognose(seasonality))
                + EPS
            )

        return self._error() / (self._error(self.true, benchmark) + EPS)

    def _bounded_relative_error(self, benchmark: np.ndarray = None):
        """ Bounded Relative Error """
        if benchmark is None or isinstance(benchmark, int):
            # If no benchmark prediction provided - use naive forecasting
            if not isinstance(benchmark, int):
                seasonality = 1
            else:
                seasonality = benchmark

            abs_err = np.abs(
                self._error(self.true[seasonality:], self.predicted[seasonality:])
            )
            abs_err_bench = np.abs(
                self._error(self.true[seasonality:], self._naive_prognose(seasonality))
            )
        else:
            abs_err = np.abs(self._error())
            abs_err_bench = np.abs(self._error())

        return abs_err / (abs_err + abs_err_bench + EPS)

    def _ae(self):
        """Absolute error """
        return np.abs(self.true - self.predicted)

    def acc(self):
        """Anomaly correction coefficient.
        Reference: Langland et al., 2012. Miyakoda et al., 1972. Murphy et al., 1989."""
        a = self.predicted - np.mean(self.predicted)
        b = self.true - np.mean(self.true)
        c = (
            np.std(self.true, ddof=1)
            * np.std(self.predicted, ddof=1)
            * self.predicted.size
        )
        return np.dot(a, b / c)

    def mapd(self):
        """Mean absolute percentage deviation."""
        a = np.sum(np.abs(self.predicted - self.true))
        b = np.sum(np.abs(self.true))
        return a / b

    def me(self):
        """Mean error """
        return np.mean(self._error())

    def mle(self):
        """Mean log error"""
        return np.mean(np.log1p(self.predicted) - np.log1p(self.true))

    def sse(self):
        """Sum of squared errors (model vs actual).
        measure of how far off our model's predictions are from the observed values. A value of 0 indicates that all
         predications are spot on. A non-zero value indicates errors.
        https://dziganto.github.io/data%20science/linear%20regression/machine%20learning/python/Linear-Regression-101-Metrics/
        This is also called residual sum of squares (RSS) or sum of squared residuals as per
        https://www.tutorialspoint.com/statistics/residual_sum_of_squares.htm
        """
        squared_errors = (self.true - self.predicted) ** 2
        return np.sum(squared_errors)

    def mase(self, seasonality: int = 1):
        """
        Mean Absolute Scaled Error
        Baseline (benchmark) is computed with naive forecasting (shifted by @seasonality)
        modified after https://gist.github.com/bshishov/5dc237f59f019b26145648e2124ca1c9
        """
        return self.mae() / self.mae(
            self.true[seasonality:], self._naive_prognose(seasonality)
        )

    def rmsse(self, seasonality: int = 1):
        """ Root Mean Squared Scaled Error """
        q = np.abs(self._error()) / self.mae(
            self.true[seasonality:], self._naive_prognose(seasonality)
        )
        return np.sqrt(np.mean(np.square(q)))

    def mde(self):
        """Median Error"""
        return np.median(self.predicted - self.true)

    def med_seq_error(self):
        """Median Squared Error
        Same as mse but it takes median which reduces the impact of outliers.
        """
        return np.median((self.predicted - self.true) ** 2)

    def euclid_distance(self):
        """Euclidian distance

        Referneces: Kennard et al., 2010
        """
        return np.linalg.norm(self.true - self.predicted)

    def norm_euclid_distance(self):
        """Normalized Euclidian distance"""

        a = self.true / np.mean(self.true)
        b = self.predicted / np.mean(self.predicted)
        return np.linalg.norm(a - b)

    def rmsle(self):
        """Root mean square log error"""
        return np.sqrt(
            np.mean(np.power(np.log1p(self.predicted) - np.log1p(self.true), 2))
        )

    def nrmse_range(self):
        """Range Normalized Root Mean Squared Error.
        RMSE normalized by true values. This allows comparison between data sets with different scales. It is more
        sensitive to outliers.

        Reference: Pontius et al., 2008
        """

        return self.rmse() / (np.max(self.true) - np.min(self.true))

    def nrmse_ipercentile(self, q1=25, q2=75):
        """
        RMSE normalized by inter percentile range of true. This is least sensitive to outliers.
        q1: any interger between 1 and 99
        q2: any integer between 2 and 100. Should be greater than q1.
        Reference: Pontius et al., 2008.
        """

        q1 = np.percentile(self.true, q1)
        q3 = np.percentile(self.true, q2)
        iqr = q3 - q1

        return self.rmse() / iqr

    def nrmse_mean(self):
        """Mean Normalized RMSE
        RMSE normalized by mean of true values.This allows comparison between datasets with different scales.

        Reference: Pontius et al., 2008
        """
        return self.rmse() / np.mean(self.true)

    def irmse(self):
        """Inertial RMSE. RMSE divided by standard deviation of the gradient of true."""
        # Getting the gradient of the observed data
        obs_len = self.true.size
        obs_grad = self.true[1:obs_len] - self.true[0 : obs_len - 1]

        # Standard deviation of the gradient
        obs_grad_std = np.std(obs_grad, ddof=1)

        # Divide RMSE by the standard deviation of the gradient of the observed data
        return self.rmse() / obs_grad_std

    def rmdspe(self):
        """
        Root Median Squared Percentage Error
        """
        return np.sqrt(np.median(np.square(self._percentage_error()))) * 100.0

    def inrse(self):
        """ Integral Normalized Root Squared Error """
        return np.sqrt(
            np.sum(np.square(self._error()))
            / np.sum(np.square(self.true - np.mean(self.true)))
        )

    def rrse(self):
        """ Root Relative Squared Error """
        return np.sqrt(
            np.sum(np.square(self.true - self.predicted))
            / np.sum(np.square(self.true - np.mean(self.true)))
        )

    def mda(self):
        """Mean Directional Accuracy
        modified after https://gist.github.com/bshishov/5dc237f59f019b26145648e2124ca1c9
        """
        dict_acc = np.sign(self.true[1:] - self.true[:-1]) == np.sign(
            self.predicted[1:] - self.predicted[:-1]
        )
        return np.mean(dict_acc)

    def gmae(self):
        """ Geometric Mean Absolute Error """
        return _geometric_mean(np.abs(self._error()))

    def mpe(self):
        """ Mean Percentage Error """
        return np.mean(self._percentage_error())

    def mdape(self):
        """
        Median Absolute Percentage Error
        """
        return np.median(np.abs(self._percentage_error())) * 100

    def smdape(self):
        """
        Symmetric Median Absolute Percentage Error
        Note: result is NOT multiplied by 100
        """
        return np.median(
            2.0 * self._ae() / ((np.abs(self.true) + np.abs(self.predicted)) + EPS)
        )

    def maape(self):
        """
        Mean Arctangent Absolute Percentage Error
        Note: result is NOT multiplied by 100
        """
        return np.mean(
            np.arctan(np.abs((self.true - self.predicted) / (self.true + EPS)))
        )

    def norm_ae(self):
        """ Normalized Absolute Error """
        return np.sqrt(
            np.sum(np.square(self._error() - self.mae())) / (len(self.true) - 1)
        )

    def norm_ape(self):
        """ Normalized Absolute Percentage Error """
        return np.sqrt(
            np.sum(np.square(self._percentage_error() - self.mape()))
            / (len(self.true) - 1)
        )

    def rae(self):
        """ Relative Absolute Error (aka Approximation Error) """
        return np.sum(self._ae()) / (
            np.sum(np.abs(self.true - np.mean(self.true))) + EPS
        )

    def mrae(self, benchmark: np.ndarray = None):
        """ Mean Relative Absolute Error """
        return np.mean(np.abs(self._relative_error(benchmark)))

    def mdrae(self, benchmark: np.ndarray = None):
        """ Median Relative Absolute Error """
        return np.median(np.abs(self._relative_error(benchmark)))

    def gmrae(self, benchmark: np.ndarray = None):
        """ Geometric Mean Relative Absolute Error """
        return _geometric_mean(np.abs(self._relative_error(benchmark)))

    def mbrae(self, benchmark: np.ndarray = None):
        """ Mean Bounded Relative Absolute Error """
        return np.mean(self._bounded_relative_error(benchmark))

    def umbrae(self, benchmark: np.ndarray = None):
        """ Unscaled Mean Bounded Relative Absolute Error """
        return self.mbrae(benchmark) / (1 - self.mbrae(benchmark))

    def rmse(self, weights=None) -> float:
        """ root mean square error"""
        return sqrt(
            np.average((self.true - self.predicted) ** 2, axis=0, weights=weights)
        )

    def mse(self, weights=None) -> float:
        """ mean square error """
        return np.average((self.true - self.predicted) ** 2, axis=0, weights=weights)

    def r2(self) -> float:
        """coefficient of determination. Square of pearson correlation coefficient. More heavily affected by outliers
        than pearson correlatin r."""
        zx = (self.true - np.mean(self.true)) / np.std(self.true, ddof=1)
        zy = (self.predicted - np.mean(self.predicted)) / np.std(self.predicted, ddof=1)
        r = np.sum(zx * zy) / (len(self.true) - 1)
        return r ** 2

    def r2_mod(self, weights=None) -> float:
        """
        This is not a symmetric function.
        Unlike most other scores, R^2 score may be negative (it need not actually
        be the square of a quantity R).
        This metric is not well-defined for single samples and will return a NaN
        value if n_samples is less than two.
        """

        if len(self.predicted) < 2:
            msg = "R^2 score is not well-defined with less than two samples."
            warnings.warn(msg)
            return float("nan")

        if weights is None:
            weight = 1.0
        else:
            weight = weights[:, np.newaxis]

        numerator = (weight * (self.true - self.predicted) ** 2).sum(
            axis=0, dtype=np.float64
        )
        denominator = (
            weight * (self.true - np.average(self.true, axis=0, weights=weights)) ** 2
        ).sum(axis=0, dtype=np.float64)

        output_scores = _foo(denominator, numerator)

        return np.average(output_scores, weights=weights)

    def rsr(self) -> float:
        return self.rmse() / np.std(self.true)

    def nse(self) -> float:
        _nse = 1 - sum((self.predicted - self.true) ** 2) / sum(
            (self.true - np.mean(self.true)) ** 2
        )
        return _nse

    def abs_pbias(self) -> float:
        """ Absolute Percent bias"""
        _apb = (
            100.0 * sum(abs(self.predicted - self.true)) / sum(self.true)
        )  # Absolute percent bias
        return _apb

    def pbias(self) -> float:
        """ Percent Bias"""
        return 100.0 * sum(self.predicted - self.true) / sum(self.true)  # percent bias

    def nrmse(self) -> float:
        """ Normalized Root Mean Squared Error """
        return self.rmse() / (self.true.max() - self.true.min())

    def mae(self, true=None, predicted=None):
        """ Mean Absolute Error """
        if true is None:
            true = self.true
        if predicted is None:
            predicted = self.predicted
        return np.mean(np.abs(true - predicted))

    def mape(self) -> float:
        """ Mean Absolute Percentage Error"""
        return np.mean(np.abs((self.true - self.predicted) / self.true)) * 100

    def smape(self) -> float:
        """
        Symmetric Mean Absolute Percentage Error
        https://en.wikipedia.org/wiki/Symmetric_mean_absolute_percentage_error
        https://stackoverflow.com/a/51440114/5982232
        """
        _temp = np.sum(
            2
            * np.abs(self.predicted - self.true)
            / (np.abs(self.true) + np.abs(self.predicted))
        )
        return 100 / len(self.true) * _temp

    def wmape(self):
        """
        Weighted Mean Absolute Percent Error
        https://stackoverflow.com/a/54833202/5982232
        """
        # Take a series (actual) and a dataframe (forecast) and calculate wmape
        # for each forecast. Output shape is (1, num_forecasts)

        # Make an array of mape (same shape as forecast)
        se_mape = abs(self.true - self.predicted) / self.true

        # Calculate sum of actual values
        ft_actual_sum = self.true.sum(axis=0)

        # Multiply the actual values by the mape
        se_actual_prod_mape = self.true * se_mape

        # Take the sum of the product of actual values and mape
        # Make sure to sum down the rows (1 for each column)
        ft_actual_prod_mape_sum = se_actual_prod_mape.sum(axis=0)

        # Calculate the wmape for each forecast and return as a dictionary
        ft_wmape_forecast = ft_actual_prod_mape_sum / ft_actual_sum
        return ft_wmape_forecast

    def wape(self) -> float:
        """
        weighted absolute percentage error
        https://mattdyor.wordpress.com/2018/05/23/calculating-wape/
        """
        return float(np.sum(self._ae() / np.sum(self.true)))

    def mean_abs_rel_error(self) -> float:
        """ Mean Absolute Relative Error """
        return np.sum(self._ae(), axis=0, dtype=np.float64) / np.sum(self.true)

    def mean_bias_error(self) -> float:
        """
            It represents overall bias error or systematic error. It shows average interpolation bias; i.e. average over-
            or underestimation. [1][2]

        [2] Willmott, C. J., & Matsuura, K. (2006). On the use of dimensioned measures of error to evaluate the performance
            of spatial interpolators. International Journal of Geographical Information Science, 20(1), 89-102.
             https://doi.org/10.1080/1365881050028697
        [1] Valipour, M. (2015). Retracted: Comparative Evaluation of Radiation-Based Methods for Estimation of Potential
            Evapotranspiration. Journal of Hydrologic Engineering, 20(5), 04014068.
             http://dx.doi.org/10.1061/(ASCE)HE.1943-5584.0001066
        """
        return np.sum(self.true - self.predicted) / len(self.true)

    def bias(self) -> float:
        """
        Bias as shown in Gupta in Sorooshian (1998), Toward improved calibration of hydrologic models:
        Multiple  and noncommensurable measures of information, Water Resources Research
            .. math::
            Bias=\\frac{1}{N}\\sum_{i=1}^{N}(e_{i}-s_{i})
        """
        bias = np.nansum(self.true - self.predicted) / len(self.true)
        return float(bias)

    def log_nse(self, epsilon=0.0) -> float:
        """
        log Nash-Sutcliffe model efficiency
            .. math::
            NSE = 1-\\frac{\\sum_{i=1}^{N}(log(e_{i})-log(s_{i}))^2}{\\sum_{i=1}^{N}(log(e_{i})-log(\\bar{e})^2}-1)*-1
        """
        s, o = self.predicted + epsilon, self.true + epsilon
        return float(
            1
            - sum((np.log(o) - np.log(o)) ** 2)
            / sum((np.log(o) - np.mean(np.log(o))) ** 2)
        )

    def log_prob(self) -> float:
        """
        Logarithmic probability distribution
        """
        scale = np.mean(self.true) / 10
        if scale < 0.01:
            scale = 0.01
        y = (self.true - self.predicted) / scale
        normpdf = -(y ** 2) / 2 - np.log(np.sqrt(2 * np.pi))
        return float(np.mean(normpdf))

    def corr_coeff(self) -> float:
        """
        Correlation Coefficient
            .. math::
            r = \\frac{\\sum ^n _{i=1}(e_i - \\bar{e})(s_i - \\bar{s})}{\\sqrt{\\sum ^n _{i=1}(e_i - \\bar{e})^2}
             \\sqrt{\\sum ^n _{i=1}(s_i - \\bar{s})^2}}
        """
        correlation_coefficient = np.corrcoef(self.true, self.predicted)[0, 1]
        return correlation_coefficient

    def relative_rmse(self) -> float:
        """
        Relative Root Mean Squared Error
            .. math::
            RRMSE=\\frac{\\sqrt{\\frac{1}{N}\\sum_{i=1}^{N}(e_{i}-s_{i})^2}}{\\bar{e}}
        """
        rrmse = self.rmse() / np.mean(self.true)
        return rrmse

    def rmspe(self) -> float:
        """
        Root Mean Square Percentage Error
        https://stackoverflow.com/a/53166790/5982232
        """
        return np.sqrt(
            np.mean(np.square(((self.true - self.predicted) / self.true)), axis=0)
        )

    def agreement_index(self) -> float:
        """
        Agreement Index (d) developed by Willmott (1981)
            .. math::
            d = 1 - \\frac{\\sum_{i=1}^{N}(e_{i} - s_{i})^2}{\\sum_{i=1}^{N}(\\left | s_{i} - \\bar{e}
             \\right | + \\left | e_{i} - \\bar{e} \\right |)^2}
        """
        agreement_index = 1 - (np.sum((self.true - self.predicted) ** 2)) / (
            np.sum(
                (
                    np.abs(self.predicted - np.mean(self.true))
                    + np.abs(self.true - np.mean(self.true))
                )
                ** 2
            )
        )
        return agreement_index

    def ref_agreement_index(self):
        """Refined Index of Agreement. From -1 to 1. Larger the better.
        Refrence: Willmott et al., 2012"""
        a = np.sum(np.abs(self.predicted - self.true))
        b = 2 * np.sum(np.abs(self.true - self.true.mean()))
        if a <= b:
            return 1 - (a / b)
        else:
            return (b / a) - 1

    def rel_agreement_index(self):
        """Relative index of agreement. from 0 to 1. larger the better."""
        a = ((self.predicted - self.true) / self.true) ** 2
        b = np.abs(self.predicted - np.mean(self.true))
        c = np.abs(self.true - np.mean(self.true))
        e = ((b + c) / np.mean(self.true)) ** 2
        return 1 - (np.sum(a) / np.sum(e))

    def mod_agreement_index(self, j=1):
        """Modified agreement of index.
        j: int, when j==1, this is same as agreement_index. Higher j means more impact of outliers."""
        a = (np.abs(self.predicted - self.true)) ** j
        b = np.abs(self.predicted - np.mean(self.true))
        c = np.abs(self.true - np.mean(self.true))
        e = (b + c) ** j
        return 1 - (np.sum(a) / np.sum(e))

    def covariance(self) -> float:
        """
        Covariance
            .. math::
            Covariance = \\frac{1}{N} \\sum_{i=1}^{N}((e_{i} - \\bar{e}) * (s_{i} - \\bar{s}))
        """
        obs_mean = np.mean(self.true)
        sim_mean = np.mean(self.predicted)
        covariance = np.mean((self.true - obs_mean) * (self.predicted - sim_mean))
        return float(covariance)

    def decomposed_mse(self) -> float:
        """
        Decomposed MSE developed by Kobayashi and Salam (2000)
            .. math ::
            dMSE = (\\frac{1}{N}\\sum_{i=1}^{N}(e_{i}-s_{i}))^2 + SDSD + LCS
            SDSD = (\\sigma(e) - \\sigma(s))^2
            LCS = 2 \\sigma(e) \\sigma(s) * (1 - \\frac{\\sum ^n _{i=1}(e_i - \\bar{e})(s_i - \\bar{s})}
            {\\sqrt{\\sum ^n _{i=1}(e_i - \\bar{e})^2} \\sqrt{\\sum ^n _{i=1}(s_i - \\bar{s})^2}})
        """
        e_std = np.std(self.true)
        s_std = np.std(self.predicted)

        bias_squared = self.bias() ** 2
        sdsd = (e_std - s_std) ** 2
        lcs = 2 * e_std * s_std * (1 - self.corr_coeff())

        decomposed_mse = bias_squared + sdsd + lcs

        return decomposed_mse

    def kge(self, return_all=False):
        """
        Kling-Gupta Efficiency
        Gupta, Kling, Yilmaz, Martinez, 2009, Decomposition of the mean squared error and NSE performance
         criteria: Implications for improving hydrological modelling
        output:
            kge: Kling-Gupta Efficiency
            cc: correlation
            alpha: ratio of the standard deviation
            beta: ratio of the mean
        """
        cc = np.corrcoef(self.true, self.predicted)[0, 1]
        alpha = np.std(self.predicted) / np.std(self.true)
        beta = np.sum(self.predicted) / np.sum(self.true)
        kge = 1 - np.sqrt((cc - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        if return_all:
            return np.vstack((kge, cc, alpha, beta))
        else:
            return kge

    def kge_np(self, return_all=False):
        """
        Non parametric Kling-Gupta Efficiency
        Corresponding paper:
        Pool, Vis, and Seibert, 2018 Evaluating model performance: towards a non-parametric variant of the
         Kling-Gupta efficiency, Hydrological Sciences Journal.
        https://doi.org/10.1080/02626667.2018.1552002
        output:
            kge: Kling-Gupta Efficiency
            cc: correlation
            alpha: ratio of the standard deviation
            beta: ratio of the mean
        """
        # # self-made formula
        cc = self.spearmann_corr()

        fdc_sim = np.sort(
            self.predicted / (np.nanmean(self.predicted) * len(self.predicted))
        )
        fdc_obs = np.sort(self.true / (np.nanmean(self.true) * len(self.true)))
        alpha = 1 - 0.5 * np.nanmean(np.abs(fdc_sim - fdc_obs))

        beta = np.mean(self.predicted) / np.mean(self.true)
        kge = 1 - np.sqrt((cc - 1) ** 2 + (alpha - 1) ** 2 + (beta - 1) ** 2)
        if return_all:
            return np.vstack((kge, cc, alpha, beta))
        else:
            return kge

    def pearson_r(self):
        """Pearson correlation coefficient.
        Measures linear correlatin. Sensitive to outliers.
        Reference: Pearson, K 1895.
        """
        sim_mean = np.mean(self.predicted)
        obs_mean = np.mean(self.true)

        top = np.sum((self.true - obs_mean) * (self.predicted - sim_mean))
        bot1 = np.sqrt(np.sum((self.true - obs_mean) ** 2))
        bot2 = np.sqrt(np.sum((self.predicted - sim_mean) ** 2))

        return top / (bot1 * bot2)

    def kge_mod(self, return_all=False):
        """
        Modified Kling-Gupta Efficiency (Kling et al. 2012 - https://doi.org/10.1016/j.jhydrol.2012.01.011)
        """
        # calculate error in timing and dynamics r (Pearson's correlation coefficient)
        sim_mean = np.mean(self.predicted, axis=0, dtype=np.float64)
        obs_mean = np.mean(self.true, dtype=np.float64)
        r = np.sum(
            (self.predicted - sim_mean) * (self.true - obs_mean),
            axis=0,
            dtype=np.float64,
        ) / np.sqrt(
            np.sum((self.predicted - sim_mean) ** 2, axis=0, dtype=np.float64)
            * np.sum((self.true - obs_mean) ** 2, dtype=np.float64)
        )
        # calculate error in spread of flow gamma (avoiding cross correlation with bias by dividing by the mean)
        gamma = (np.std(self.predicted, axis=0, dtype=np.float64) / sim_mean) / (
            np.std(self.true, dtype=np.float64) / obs_mean
        )
        # calculate error in volume beta (bias of mean discharge)
        beta = np.mean(self.predicted, axis=0, dtype=np.float64) / np.mean(
            self.true, axis=0, dtype=np.float64
        )
        # calculate the modified Kling-Gupta Efficiency KGE'
        kgeprime_ = 1 - np.sqrt((r - 1) ** 2 + (gamma - 1) ** 2 + (beta - 1) ** 2)

        if return_all:
            return np.vstack((kgeprime_, r, gamma, beta))
        else:
            return kgeprime_

    def volume_error(self) -> float:
        """
        Returns the Volume Error (Ve).
        It is an indicator of the agreement between the averages of the simulated
        and observed runoff (i.e. long-term water balance).
        used in this paper:
        Reynolds, J.E., S. Halldin, C.Y. Xu, J. Seibert, and A. Kauffeldt. 2017.
        "Sub-Daily Runoff Predictions Using Parameters Calibrated on the Basis of Data with a
        Daily Temporal Resolution."  Journal of Hydrology 550 (July):399?411.
        https://doi.org/10.1016/j.jhydrol.2017.05.012.
            .. math::
            Sum(self.predicted- true)/sum(self.predicted)
        """
        # TODO written formula and executed formula are different.
        ve = np.sum(self.predicted - self.true) / np.sum(self.true)
        return float(ve)

    def mean_poisson_deviance(self, weights=None) -> float:
        """
        mean poisson deviance
        """
        return _mean_tweedie_deviance(
            self.true, self.predicted, weights=weights, power=1
        )

    def mean_gamma_deviance(self, weights=None):
        """
        mean gamma deviance
        """
        return _mean_tweedie_deviance(
            self.true, self.predicted, weights=weights, power=2
        )

    def median_abs_error(self) -> float:
        """
        median absolute error
        """
        return float(np.median(np.abs(self.predicted - self.true), axis=0))

    def mean_square_log_error(self, weights=None) -> float:
        """
        mean square logrithmic error
        """
        return np.average(
            (np.log1p(self.true) - np.log1p(self.predicted)) ** 2,
            axis=0,
            weights=weights,
        )

    def max_error(self) -> float:
        """
        maximum error
        """
        return np.max(self._ae())

    def exp_var_score(self, weights=None) -> float:
        """
        Explained variance score
        https://stackoverflow.com/questions/24378176/python-sci-kit-learn-metrics-difference-between-r2-score-and-explained-varian
        best value is 1, lower values are less accurate.
        """
        y_diff_avg = np.average(self.true - self.predicted, weights=weights, axis=0)
        numerator = np.average(
            (self.true - self.predicted - y_diff_avg) ** 2, weights=weights, axis=0
        )

        y_true_avg = np.average(self.true, weights=weights, axis=0)
        denominator = np.average((self.true - y_true_avg) ** 2, weights=weights, axis=0)

        output_scores = _foo(denominator, numerator)

        return np.average(output_scores, weights=weights)

    def fdc_fhv(self, h: float = 0.02) -> float:
        """
        modified after: https://github.com/kratzert/ealstm_regional_modeling/blob/64a446e9012ecd601e0a9680246d3bbf3f002f6d/papercode/metrics.py#L190
        Peak flow bias of the flow duration curve (Yilmaz 2018).
        used in kratzert et al., 2018
        Returns
        -------
        float
            Bias of the peak flows

        Raises
        ------

        RuntimeError
            If `h` is not in range(0,1)
        """
        if (h <= 0) or (h >= 1):
            raise RuntimeError("h has to be in the range (0,1)")

        # sort both in descending order
        obs = -np.sort(-self.true)
        sim = -np.sort(-self.predicted)

        # subset data to only top h flow values
        obs = obs[: np.round(h * len(obs)).astype(int)]
        sim = sim[: np.round(h * len(sim)).astype(int)]

        fhv = np.sum(sim - obs) / (np.sum(obs) + 1e-6)

        return fhv * 100

    def nse_alpha(self) -> float:
        """
        Alpha decomposition of the NSE, see Gupta et al. 2009
        used in kratzert et al., 2018
        Returns
        -------
        float
            Alpha decomposition of the NSE

        """
        return np.std(self.predicted) / np.std(self.true)

    def nse_beta(self) -> float:
        """
        Beta decomposition of NSE. See Gupta et. al 2009
        used in kratzert et al., 2018
        Returns
        -------
        float
            Beta decomposition of the NSE
        """
        return (np.mean(self.predicted) - np.mean(self.true)) / np.std(self.true)

    def nse_mod(self, j=1):
        """
        Gives less weightage of outliers if j=1 and if j>1, gives more weightage to outliers.
        Reference: Krause et al., 2005
        """
        a = (np.abs(self.predicted - self.true)) ** j
        b = (np.abs(self.true - np.mean(self.true))) ** j
        return 1 - (np.sum(a) / np.sum(b))

    def nse_rel(self):
        """
        Relative NSE.
        """

        a = (np.abs((self.predicted - self.true) / self.true)) ** 2
        b = (np.abs((self.true - np.mean(self.true)) / np.mean(self.true))) ** 2
        return 1 - (np.sum(a) / np.sum(b))

    def fdc_flv(self, low_flow: float = 0.3) -> float:
        """
        bias of the bottom 30 % low flows
        modified after: https://github.com/kratzert/ealstm_regional_modeling/blob/64a446e9012ecd601e0a9680246d3bbf3f002f6d/papercode/metrics.py#L237
        used in kratzert et al., 2018
        Parameters
        ----------
        low_flow : float, optional
            Upper limit of the flow duration curve. E.g. 0.3 means the bottom 30% of the flows are
            considered as low flows, by default 0.3

        Returns
        -------
        float
            Bias of the low flows.

        Raises
        ------
        RuntimeError
            If `low_flow` is not in the range(0,1)
        """

        low_flow = 1.0 - low_flow
        # make sure that metric is calculated over the same dimension
        obs = self.true.flatten()
        sim = self.predicted.flatten()

        if (low_flow <= 0) or (low_flow >= 1):
            raise RuntimeError("l has to be in the range (0,1)")

        # for numerical reasons change 0s to 1e-6
        sim[sim == 0] = 1e-6
        obs[obs == 0] = 1e-6

        # sort both in descending order
        obs = -np.sort(-obs)
        sim = -np.sort(-sim)

        # subset data to only top h flow values
        obs = obs[np.round(low_flow * len(obs)).astype(int) :]
        sim = sim[np.round(low_flow * len(sim)).astype(int) :]

        # transform values to log scale
        obs = np.log(obs + 1e-6)
        sim = np.log(sim + 1e-6)

        # calculate flv part by part
        qsl = np.sum(sim - sim.min())
        qol = np.sum(obs - obs.min())

        flv = -1 * (qsl - qol) / (qol + 1e-6)

        return flv * 100

    def nse_bound(self):
        """
        Bounded Version of the Nash-Sutcliffe Efficiency
        https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf
        """
        nse_ = self.nse()
        nse_c2m_ = nse_ / (2 - nse_)

        return nse_c2m_

    def kge_bound(self):
        """
        Bounded Version of the Original Kling-Gupta Efficiency
        https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf
        """
        kge_ = self.kge(return_all=True)[0, :]
        kge_c2m_ = kge_ / (2 - kge_)

        return kge_c2m_

    def kgeprime_c2m(self):
        """
        https://iahs.info/uploads/dms/13614.21--211-219-41-MATHEVET.pdf
         Bounded Version of the Modified Kling-Gupta Efficiency
        """
        kgeprime_ = self.kge_mod(return_all=True)[0, :]
        kgeprime_c2m_ = kgeprime_ / (2 - kgeprime_)

        return kgeprime_c2m_

    def kgenp_bound(self):
        """
        Bounded Version of the Non-Parametric Kling-Gupta Efficiency
        """
        kgenp_ = self.kge_np(return_all=True)[0, :]
        kgenp_c2m_ = kgenp_ / (2 - kgenp_)

        return kgenp_c2m_

    def mb_r(self):
        """Mielke-Berry R value.
        Mielke and Berry., 2007.
        Berry and Mielke, 1988.
        """
        # Calculate metric
        n = self.predicted.size
        tot = 0.0
        for i in range(n):
            tot = tot + np.sum(np.abs(self.predicted - self.true[i]))
        mae_val = np.sum(np.abs(self.predicted - self.true)) / n
        mb = 1 - ((n ** 2) * mae_val / tot)

        return mb

    def lm_index(self, obs_bar_p=None):
        """Legate-McCabe Efficiency Index.

        obs_bar_p: float, Seasonal or other selected average. If None, the mean of the observed array will be used.
        """
        mean_obs = np.mean(self.true)

        if obs_bar_p is not None:
            a = np.abs(self.predicted - self.true)
            b = np.abs(self.true - obs_bar_p)
            return 1 - (np.sum(a) / np.sum(b))
        else:
            a = np.abs(self.predicted - self.true)
            b = np.abs(self.true - mean_obs)
            return 1 - (np.sum(a) / np.sum(b))

    def watt_m(self):
        """Watterson's M.
        Refrence: Watterson., 1996"""
        a = 2 / np.pi
        c = np.std(self.true, ddof=1) ** 2 + np.std(self.predicted, ddof=1) ** 2
        e = (np.mean(self.predicted) - np.mean(self.true)) ** 2
        f = c + e
        return a * np.arcsin(1 - (self.mse() / f))

    def stats(self, verbose: bool = False) -> dict:
        """ returns some important stats about true and predicted values."""
        _stats = dict()
        _stats["true"] = stats(self.true)
        _stats["predicted"] = stats(self.predicted)

        if verbose:
            print("\nName            True         Predicted  ")
            print("----------------------------------------")
            for k in _stats["true"].keys():
                print(
                    "{:<25},  {:<10},  {:<10}".format(
                        k, round(_stats["true"][k], 4), round(_stats["predicted"][k])
                    )
                )

        return _stats

    def spearmann_corr(self):
        """Separmann correlation coefficient
        https://hess.copernicus.org/articles/24/2505/2020/hess-24-2505-2020.pdf
        """
        col = [list(a) for a in zip(self.true, self.predicted)]
        xy = sorted(col, key=lambda _x: _x[0], reverse=False)
        # rang of x-value
        for i, row in enumerate(xy):
            row.append(i + 1)

        a = sorted(xy, key=lambda _x: _x[1], reverse=False)
        # rang of y-value
        for i, row in enumerate(a):
            row.append(i + 1)

        mw_rank_x = np.nanmean(np.array(a)[:, 2])
        mw_rank_y = np.nanmean(np.array(a)[:, 3])

        numerator = np.nansum(
            [
                float((a[j][2] - mw_rank_x) * (a[j][3] - mw_rank_y))
                for j in range(len(a))
            ]
        )
        denominator1 = np.sqrt(
            np.nansum([(a[j][2] - mw_rank_x) ** 2.0 for j in range(len(a))])
        )
        denominator2 = np.sqrt(
            np.nansum([(a[j][3] - mw_rank_x) ** 2.0 for j in range(len(a))])
        )
        return float(numerator / (denominator1 * denominator2))

    def ve(self):
        """
        Volumetric efficiency. from 0 to 1. Smaller the better.
        Reference: Criss and Winston 2008.
        """
        a = np.sum(np.abs(self.predicted - self.true))
        b = np.sum(self.true)
        return 1 - (a / b)

    def sa(self):
        """Spectral angle. From -pi/2 to pi/2. Closer to 0 is better.
        It measures angle between two vectors in hyperspace indicating how well the shape of two arrays match instead
        of their magnitude.
        Reference: Robila and Gershman, 2005."""
        a = np.dot(self.predicted, self.true)
        b = np.linalg.norm(self.predicted) * np.linalg.norm(self.true)
        return np.arccos(a / b)

    def sc(self):
        """Spectral correlation.
        From -pi/2 to pi/2. Closer to 0 is better.
        """
        a = np.dot(
            self.true - np.mean(self.true), self.predicted - np.mean(self.predicted)
        )
        b = np.linalg.norm(self.true - np.mean(self.true))
        c = np.linalg.norm(self.predicted - np.mean(self.predicted))
        e = b * c
        return np.arccos(a / e)

    def sid(self):
        """Spectral Information Divergence.
        From -pi/2 to pi/2. Closer to 0 is better."""
        first = (self.true / np.mean(self.true)) - (
            self.predicted / np.mean(self.predicted)
        )
        second1 = np.log10(self.true) - np.log10(np.mean(self.true))
        second2 = np.log10(self.predicted) - np.log10(np.mean(self.predicted))
        return np.dot(first, second1 - second2)

    def sga(self):
        """Spectral gradient angle.
        From -pi/2 to pi/2. Closer to 0 is better.
        """
        sgx = self.true[1:] - self.true[: self.true.size - 1]
        sgy = self.predicted[1:] - self.predicted[: self.predicted.size - 1]
        a = np.dot(sgx, sgy)
        b = np.linalg.norm(sgx) * np.linalg.norm(sgy)
        return np.arccos(a / b)

    def gmean_diff(self):
        """Geometric mean difference. First geometric mean is calculated for each of two samples and their difference
        is calculated."""
        sim_log = np.log1p(self.predicted)
        obs_log = np.log1p(self.true)
        return np.exp(gmean(sim_log) - gmean(obs_log))

    def KLsym(self):
        """Symmetric kullback-leibler divergence"""
        if not all((self.true == 0) == (self.predicted == 0)):
            return (
                None  # ('KL divergence not defined when only one distribution is 0.')
            )
        x, y = self.true, self.predicted
        # set values where both distributions are 0 to the same (positive) value.
        # This will not contribute to the final distance.
        x[x == 0] = 1
        y[y == 0] = 1
        d = 0.5 * np.sum((x - y) * (np.log2(x) - np.log2(y)))
        return d

    def aitchison(self, center="mean"):
        """ Aitchison distance. used in https://hess.copernicus.org/articles/24/2505/2020/hess-24-2505-2020.pdf"""
        lx = np.log(self.true)
        ly = np.log(self.predicted)
        if center.upper() == "MEAN":
            m = np.mean
        elif center.upper() == "MEDIAN":
            m = np.median
        else:
            raise ValueError

        clr_x = lx - m(lx)
        clr_y = ly - m(ly)
        d = (sum((clr_x - clr_y) ** 2)) ** 0.5
        return float(d)

    def JS(self):
        """Jensen-shannon divergence"""
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        d1 = self.true * np.log2(2 * self.true / (self.true + self.predicted))
        d2 = self.predicted * np.log2(2 * self.predicted / (self.true + self.predicted))
        d1[np.isnan(d1)] = 0
        d2[np.isnan(d2)] = 0
        d = 0.5 * sum(d1 + d2)
        return d

    def centered_rms_dev(self):
        """
        Modified after https://github.com/PeterRochford/SkillMetrics/blob/master/skill_metrics/centered_rms_dev.py
        Calculates the centered root-mean-square (RMS) difference between true and predicted
        using the formula:
        (E')^2 = sum_(n=1)^N [(p_n - mean(p))(r_n - mean(r))]^2/N
        where p is the predicted values, r is the true values, and
        N is the total number of values in p & r.

        Output:
        CRMSDIFF : centered root-mean-square (RMS) difference (E')^2
        """
        # Calculate means
        pmean = np.mean(self.predicted)
        rmean = np.mean(self.true)

        # Calculate (E')^2
        crmsd = np.square((self.predicted - pmean) - (self.true - rmean))
        crmsd = np.sum(crmsd) / self.predicted.size
        crmsd = np.sqrt(crmsd)

        return crmsd

    def skill_score_murphy(self):
        """
        Adopted from https://github.com/PeterRochford/SkillMetrics/blob/278b2f58c7d73566f25f10c9c16a15dc204f5869/skill_metrics/skill_score_murphy.py
        Calculate non-dimensional skill score (SS) between two variables using
        definition of Murphy (1988) using the formula:

        SS = 1 - RMSE^2/SDEV^2

        SDEV is the standard deviation of the true values

        SDEV^2 = sum_(n=1)^N [r_n - mean(r)]^2/(N-1)

        where p is the predicted values, r is the reference values, and
        N is the total number of values in p & r. Note that p & r must
        have the same number of values.

        Output:
        SS : skill score
        Reference:
        Allan H. Murphy, 1988: Skill Scores Based on the Mean Square Error
        and Their Relationships to the Correlation Coefficient. Mon. Wea.
        Rev., 116, 2417-2424.
        doi: http//dx.doi.org/10.1175/1520-0493(1988)<2417:SSBOTM>2.0.CO;2
        """
        # Calculate RMSE
        rmse2 = self.rmse() ** 2

        # Calculate standard deviation
        sdev2 = np.std(self.true, ddof=1) ** 2

        # % Calculate skill score
        ss = 1 - rmse2 / sdev2

        return ss

    def brier_score(self):
        """
        Adopted from https://github.com/PeterRochford/SkillMetrics/blob/master/skill_metrics/brier_score.py
        Calculates the Brier score (BS), a measure of the mean-square error of
        probability forecasts for a dichotomous (two-category) event, such as
        the occurrence/non-occurrence of precipitation. The score is calculated
        using the formula:
        BS = sum_(n=1)^N (f_n - o_n)^2/N

        where f is the forecast probabilities, o is the observed probabilities
        (0 or 1), and N is the total number of values in f & o. Note that f & o
        must have the same number of values, and those values must be in the
        range [0,1].

        Output:
        BS : Brier score

        Reference:
        Glenn W. Brier, 1950: Verification of forecasts expressed in terms
        of probabilities. Mon. We. Rev., 78, 1-23.
        D. S. Wilks, 1995: Statistical Methods in the Atmospheric Sciences.
        Cambridge Press. 547 pp.

        """
        # Check for valid values
        index = np.where(np.logical_or(self.predicted < 0, self.predicted > 1))
        if np.sum(index) > 0:
            msg = "Forecast has values outside interval [0,1]."
            raise ValueError(msg)

        index = np.where(np.logical_and(self.true != 0, self.true != 1))
        if np.sum(index) > 0:
            msg = "Observed has values not equal to 0 or 1."
            raise ValueError(msg)

        # Calculate score
        bs = np.sum(np.square(self.predicted - self.true)) / len(self.predicted)

        return bs

    def plot(self, save=True, name="plot", show=False):
        fig, axis = plt.subplots()

        axis.plot(np.arange(len(self.true)), self.true, label="True")
        axis.plot(np.arange(len(self.predicted)), self.predicted, label="Predicted")
        axis.legend(loc="best")

        if save:
            plt.savefig(name, dpi=300, bbox_inches="tight")
        if show:
            plt.show()

        plt.close("all")
        return

    def mean_var(self):
        """Mean variance"""
        return np.var(np.log1p(self.true) - np.log1p(self.predicted))

    def treat_values(self):
        """
        This function is applied by default at the start/at the time of initiating the class. However, it can used any
        time after that. This can be handy if we want to calculate error first by ignoring nan and then by no ignoring
        nan.
        Adopting from https://github.com/BYU-Hydroinformatics/HydroErr/blob/master/HydroErr/HydroErr.py#L6210
        Removes the nan, negative, and inf values in two numpy arrays"""
        sim_copy = np.copy(self.predicted)
        obs_copy = np.copy(self.true)

        # Treat missing data in observed_array and simulated_array, rows in simulated_array or
        # observed_array that contain nan values
        all_treatment_array = np.ones(obs_copy.size, dtype=bool)

        if np.any(np.isnan(obs_copy)) or np.any(np.isnan(sim_copy)):
            if self.replace_nan is not None:
                # Finding the NaNs
                sim_nan = np.isnan(sim_copy)
                obs_nan = np.isnan(obs_copy)
                # Replacing the NaNs with the input
                sim_copy[sim_nan] = self.replace_nan
                obs_copy[obs_nan] = self.replace_nan

                warnings.warn(
                    "Elements(s) {} contained NaN values in the simulated array and "
                    "elements(s) {} contained NaN values in the observed array and have been "
                    "replaced (Elements are zero indexed).".format(
                        np.where(sim_nan)[0], np.where(obs_nan)[0]
                    ),
                    UserWarning,
                )
            else:
                # Getting the indices of the nan values, combining them, and informing user.
                nan_indices_fcst = ~np.isnan(sim_copy)
                nan_indices_obs = ~np.isnan(obs_copy)
                all_nan_indices = np.logical_and(nan_indices_fcst, nan_indices_obs)
                all_treatment_array = np.logical_and(
                    all_treatment_array, all_nan_indices
                )

                warnings.warn(
                    "Row(s) {} contained NaN values and the row(s) have been "
                    "removed (Rows are zero indexed).".format(
                        np.where(~all_nan_indices)[0]
                    ),
                    UserWarning,
                )

        if np.any(np.isinf(obs_copy)) or np.any(np.isinf(sim_copy)):
            if self.replace_nan is not None:
                # Finding the NaNs
                sim_inf = np.isinf(sim_copy)
                obs_inf = np.isinf(obs_copy)
                # Replacing the NaNs with the input
                sim_copy[sim_inf] = self.replace_inf
                obs_copy[obs_inf] = self.replace_inf

                warnings.warn(
                    "Elements(s) {} contained Inf values in the simulated array and "
                    "elements(s) {} contained Inf values in the observed array and have been "
                    "replaced (Elements are zero indexed).".format(
                        np.where(sim_inf)[0], np.where(obs_inf)[0]
                    ),
                    UserWarning,
                )
            else:
                inf_indices_fcst = ~(np.isinf(sim_copy))
                inf_indices_obs = ~np.isinf(obs_copy)
                all_inf_indices = np.logical_and(inf_indices_fcst, inf_indices_obs)
                all_treatment_array = np.logical_and(
                    all_treatment_array, all_inf_indices
                )

                warnings.warn(
                    "Row(s) {} contained Inf or -Inf values and the row(s) have been removed (Rows "
                    "are zero indexed).".format(np.where(~all_inf_indices)[0]),
                    UserWarning,
                )

        # Treat zero data in observed_array and simulated_array, rows in simulated_array or
        # observed_array that contain zero values
        if self.remove_zero:
            if (obs_copy == 0).any() or (sim_copy == 0).any():
                zero_indices_fcst = ~(sim_copy == 0)
                zero_indices_obs = ~(obs_copy == 0)
                all_zero_indices = np.logical_and(zero_indices_fcst, zero_indices_obs)
                all_treatment_array = np.logical_and(
                    all_treatment_array, all_zero_indices
                )

                warnings.warn(
                    "Row(s) {} contained zero values and the row(s) have been removed (Rows are "
                    "zero indexed).".format(np.where(~all_zero_indices)[0]),
                    UserWarning,
                )

        # Treat negative data in observed_array and simulated_array, rows in simulated_array or
        # observed_array that contain negative values

        # Ignore runtime warnings from comparing
        if self.remove_neg:
            with np.errstate(invalid="ignore"):
                obs_copy_bool = obs_copy < 0
                sim_copy_bool = sim_copy < 0

            if obs_copy_bool.any() or sim_copy_bool.any():
                neg_indices_fcst = ~sim_copy_bool
                neg_indices_obs = ~obs_copy_bool
                all_neg_indices = np.logical_and(neg_indices_fcst, neg_indices_obs)
                all_treatment_array = np.logical_and(
                    all_treatment_array, all_neg_indices
                )

                warnings.warn(
                    "Row(s) {} contained negative values and the row(s) have been "
                    "removed (Rows are zero indexed).".format(
                        np.where(~all_neg_indices)[0]
                    ),
                    UserWarning,
                )

        self.true = obs_copy[all_treatment_array]
        self.predicted = sim_copy[all_treatment_array]

        return


def _foo(denominator, numerator):
    nonzero_numerator = numerator != 0
    nonzero_denominator = denominator != 0
    valid_score = nonzero_numerator & nonzero_denominator
    output_scores = np.ones(1)

    output_scores[valid_score] = 1 - (numerator[valid_score] / denominator[valid_score])
    output_scores[nonzero_numerator & ~nonzero_denominator] = 0.0
    return output_scores


def _mean_tweedie_deviance(y_true, y_pred, power=0, weights=None):
    # copying from https://github.com/scikit-learn/scikit-learn/blob/95d4f0841d57e8b5f6b2a570312e9d832e69debc/sklearn/metrics/_regression.py#L659

    message = "Mean Tweedie deviance error with power={} can only be used on ".format(
        power
    )
    if power < 0:
        # 'Extreme stable', y_true any real number, y_pred > 0
        if (y_pred <= 0).any():
            raise ValueError(message + "strictly positive y_pred.")
        dev = 2 * (
            np.power(np.maximum(y_true, 0), 2 - power) / ((1 - power) * (2 - power))
            - y_true * np.power(y_pred, 1 - power) / (1 - power)
            + np.power(y_pred, 2 - power) / (2 - power)
        )
    elif power == 0:
        # Normal distribution, y_true and y_pred any real number
        dev = (y_true - y_pred) ** 2
    elif power < 1:
        raise ValueError(
            "Tweedie deviance is only defined for power<=0 and " "power>=1."
        )
    elif power == 1:
        # Poisson distribution, y_true >= 0, y_pred > 0
        if (y_true < 0).any() or (y_pred <= 0).any():
            raise ValueError(
                message + "non-negative y_true and strictly " "positive y_pred."
            )
        dev = 2 * (xlogy(y_true, y_true / y_pred) - y_true + y_pred)
    elif power == 2:
        # Gamma distribution, y_true and y_pred > 0
        if (y_true <= 0).any() or (y_pred <= 0).any():
            raise ValueError(message + "strictly positive y_true and y_pred.")
        dev = 2 * (np.log(y_pred / y_true) + y_true / y_pred - 1)
    else:
        if power < 2:
            # 1 < p < 2 is Compound Poisson, y_true >= 0, y_pred > 0
            if (y_true < 0).any() or (y_pred <= 0).any():
                raise ValueError(
                    message + "non-negative y_true and strictly " "positive y_pred."
                )
        else:
            if (y_true <= 0).any() or (y_pred <= 0).any():
                raise ValueError(message + "strictly positive y_true and " "y_pred.")

        dev = 2 * (
            np.power(y_true, 2 - power) / ((1 - power) * (2 - power))
            - y_true * np.power(y_pred, 1 - power) / (1 - power)
            + np.power(y_pred, 2 - power) / (2 - power)
        )

    return np.average(dev, weights=weights)


def _geometric_mean(a, axis=0, dtype=None):
    """ Geometric mean """
    if not isinstance(a, np.ndarray):  # if not an ndarray object attempt to convert it
        log_a = np.log(np.array(a, dtype=dtype))
    elif dtype:  # Must change the default dtype allowing array type
        if isinstance(a, np.ma.MaskedArray):
            log_a = np.log(np.ma.asarray(a, dtype=dtype))
        else:
            log_a = np.log(np.asarray(a, dtype=dtype))
    else:
        log_a = np.log(a)
    return np.exp(log_a.mean(axis=axis))


if __name__ == "__main__":
    t = np.random.random((20, 1))
    p = np.random.random((20, 1))

    er = FindErrors(t, p)

    all_errors = er.calculate_all(True, True, True)

    er.plot(show=True)
    t = np.random.randint(0, 2, 20).reshape(20, 1)
    er = FindErrors(t, p)
    print("brier score: ", er.brier_score())
    s = er.stats()