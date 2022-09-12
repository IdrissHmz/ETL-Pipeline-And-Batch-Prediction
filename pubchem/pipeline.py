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
    "TotalC": tf.io.FixedLenFeature([], tf.int64),
    "TotalH": tf.io.FixedLenFeature([], tf.int64),
    "TotalO": tf.io.FixedLenFeature([], tf.int64),
    "TotalN": tf.io.FixedLenFeature([], tf.int64),
    # Labels (outputs/predictions)
    "Energy": tf.io.FixedLenFeature([], tf.float32),
}

LABELS = ["Energy"]


class ParseSDF(beam.PTransform):
    def __init__(self, file_patterns):
        super(ParseSDF, self).__init__()
        if isinstance(file_patterns, str):
            file_patterns = [file_patterns]
        self.file_patterns = file_patterns

    def expand(self, pcollection):
        def parse_molecules(filename):
            with tf.io.gfile.GFile(filename) as f:
                for json_molecule in sdf.parse_molecules(f):
                    yield json_molecule

        return (
            pcollection
            | "Create file patterns" >> beam.Create(self.file_patterns)
            | "Expand file patterns" >> beam.FlatMap(tf.io.gfile.glob)
            | "Parse molecules" >> beam.ParDo(parse_molecules)
        )


# [START dataflow_molecules_simple_feature_extraction]
class SimpleFeatureExtraction(beam.PTransform):
    def __init__(self, source):
        super(SimpleFeatureExtraction, self).__init__()
        self.source = source

    def expand(self, p):
        # Return the preprocessing pipeline. In this case we're reading the PubChem
        # files, but the source could be any Apache Beam source.
        return (
            p
            | "Read raw molecules" >> self.source
            | "Format molecule" >> beam.ParDo(FormatMolecule())
            | "Count atoms" >> beam.ParDo(CountAtoms())
        )


# [END dataflow_molecules_simple_feature_extraction]


# [START dataflow_molecules_normalize_inputs]
def normalize_inputs(inputs):

    return {
        "NormalizedC": tft.scale_to_0_1(inputs["TotalC"]),
        "NormalizedH": tft.scale_to_0_1(inputs["TotalH"]),
        "NormalizedO": tft.scale_to_0_1(inputs["TotalO"]),
        "NormalizedN": tft.scale_to_0_1(inputs["TotalN"]),
        "Energy": inputs["Energy"],
    }


# [END dataflow_molecules_normalize_inputs]
