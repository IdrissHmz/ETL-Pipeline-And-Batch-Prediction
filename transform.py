from __future__ import absolute_import

import argparse
import dill as pickle
import logging
import os
import random
import tempfile

import pubchem

import apache_beam as beam
import tensorflow as tf
import tensorflow_transform.beam.impl as beam_impl

from apache_beam.io import tfrecordio
from apache_beam.options.pipeline_options import PipelineOptions
from tensorflow_transform.beam.tft_beam_io import transform_fn_io
from tensorflow_transform.coders import example_proto_coder
from tensorflow_transform.tf_metadata import dataset_metadata
from tensorflow_transform.tf_metadata import schema_utils


#


# HELPER FUNCTION:
#
#  from google.protobuf.json_format import MessageToDict

# # Define a helper function to get individual examples
# def get_records(dataset, num_records):
#     '''Extracts records from the given dataset.
#     Args:
#         dataset (TFRecordDataset): dataset saved in the preprocessing step
#         num_records (int): number of records to preview
#     '''

#     # initialize an empty list
#     records = []

#     # Use the `take()` method to specify how many records to get
#     for tfrecord in dataset.take(num_records):

#         # Get the numpy property of the tensor
#         serialized_example = tfrecord.numpy()

#         # Initialize a `tf.train.Example()` to read the serialized data
#         example = tf.train.Example()

#         # Read the example data (output is a protocol buffer message)
#         example.ParseFromString(serialized_example)

#         # convert the protocol bufffer message to a Python dictionary
#         example_dict = (MessageToDict(example))

#         # append to the records list
#         records.append(example_dict)

#    return records
