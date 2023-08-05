#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Nov, 2019
@author: Nathan de Lara <ndelara@enst.fr>
"""
from abc import ABC

import numpy as np

from sknetwork.utils.base import Algorithm


class BaseRanking(Algorithm, ABC):
    """Base class for ranking algorithms."""

    def __init__(self):
        self.scores_ = None

    def fit_transform(self, *args, **kwargs) -> np.ndarray:
        """Fit algorithm to data and return the scores. Same parameters as the ``fit`` method.

        Returns
        -------
        scores : np.ndarray
            Scores.
        """
        self.fit(*args, **kwargs)
        return self.scores_
