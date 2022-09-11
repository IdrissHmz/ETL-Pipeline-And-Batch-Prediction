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
