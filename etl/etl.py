from __future__ import absolute_import

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.io import WriteToText
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

class csvLoadDoFn(beam.DoFn):
    """Parsea cada linea del csv como una entidad de datastore."""

    def init(self):
        """Inicializa el proceso según los lineamientos de apache beam."""
        super(csvLoadDoFn, self).init()

    def process(self, element):
        """ """
        pass

def run(argv=None):
    """Punto de acceso principal que corre el pipeline."""

if __name__=='__main__':
    Logging.getLogger().setLevel(Logging.INFO)
    run()
