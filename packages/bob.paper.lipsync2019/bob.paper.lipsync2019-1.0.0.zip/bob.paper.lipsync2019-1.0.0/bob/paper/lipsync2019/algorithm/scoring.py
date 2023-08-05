#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# @author: Pavel Korshunov <pavel.korshunov@idiap.ch>
# @date: Wed 19 Oct 23:43:22 2016

from bob.pad.base.algorithm import Algorithm
from bob.bio.base.algorithm import Algorithm as BioAlgorithm
import numpy

import logging
logger = logging.getLogger("bob.pad.voice")


class Scoring(Algorithm, BioAlgorithm):
    """This class is for evaluating data stored in tensorflow tfrecord format using a pre-trained LSTM model."""

    def __init__(self, **kwargs):
        """Generates a test value that is read and written"""

        # call base class constructor registering that this tool performs everything.
        Algorithm.__init__(
            self,
            performs_projection=True,
            requires_projector_training=False,
            **kwargs
        )
        BioAlgorithm.__init__(
            self,
            performs_projection=True,
            requires_projector_training=False,
            split_training_features_by_client=False,
            use_projected_features_for_enrollment=False,
            **kwargs
        )

    def score_for_multiple_projections(self, toscore):
        """scorescore_for_multiple_projections(toscore) -> score

        **Returns:**

        score : float
          A score value for the object ``toscore``.
        """
        scores = numpy.asarray(toscore, dtype=numpy.float32)
        real_scores = scores[:, 1]
        logger.debug("Mean score %f", numpy.mean(real_scores))
        return [numpy.mean(real_scores)]

    def score(self, toscore):
        """Returns the evarage value of the probe"""
        logger.debug("score() score %f", toscore)
        # return only real score
        return [toscore[0]]

algorithm = Scoring()
