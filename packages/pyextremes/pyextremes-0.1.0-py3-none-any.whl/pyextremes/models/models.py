# pyextremes, Extreme Value Analysis in Python
# Copyright (C), 2020 Georgii Bocharov
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import logging
import typing

import pandas as pd

from pyextremes.models.emcee import Emcee
from pyextremes.models.mle import MLE

logger = logging.getLogger(__name__)

models = {
    'MLE': MLE,
    'Emcee': Emcee
}


def get_model(
        model: str,
        extremes: pd.Series,
        distribution: str,
        **kwargs
) -> typing.Union[MLE, Emcee]:
    """
    Get an extreme value model.

    Parameters
    ----------
    model : str
        Name of an extreme value distribution fitting model.
        Supported names:
            MLE - Maximum Likelihood Estimate model (based on scipy)
            Emcee - Markov Chain Monte Carlo model based on the emcee package by Daniel Foreman-Mackey
    extremes : pandas.Series
        Time series of transformed extreme events.
    distribution : str
        Name of scipy.stats distribution.
    kwargs
        Keyword arguments passed to a model ._fit method.
        MLE model:
            MLE model takes no additional arguments.
        Emcee model:
            n_walkers : int
                The number of walkers in the ensemble.
            n_samples : int
                The number of steps to run.

    Returns
    -------
    fitting_model : class
        An extreme value model.
    """

    logger.info(f'calling get_fitting_model with {model} model')
    try:
        return models[model](extremes=extremes, distribution=distribution, **kwargs)
    except KeyError:
        raise ValueError(
            f'\'{model}\' is not a valid \'model\' value\n'
            f'Available models: {", ".join(models.keys())}'
        )
