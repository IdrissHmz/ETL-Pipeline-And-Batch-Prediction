from __future__ import absolute_import

import json
import logging
import pprint

import apache_beam as beam
import tensorflow as tf
from tensorflow.python.ops.variables import model_variables
import tensorflow_transform as tft

from apache_beam.io import filebasedsource

from pubchem import sdf


FEATURE_SPEC = {
    # Features (inputs)
    'TotalC': tf.io.FixedLenFeature([], tf.int64),
    'TotalH': tf.io.FixedLenFeature([], tf.int64),
    'TotalO': tf.io.FixedLenFeature([], tf.int64),
    'TotalN': tf.io.FixedLenFeature([], tf.int64),

    # Labels (outputs/predictions)
    'Energy': tf.io.FixedLenFeature([], tf.float32),
}

LABELS = ['Energy']