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

from google.cloud import datastore

class csvLoadDoFn(beam.DoFn):
    """Parsea cada linea del csv como una entidad de datastore."""

    def __init__(self):
        """Inicializa el proceso segun los lineamientos de apache beam."""
        super(csvLoadDoFn, self).init()

    def process(self, element):
        """Procesa cada linea del csv como una entidad de datastore."""
        pass

class EntityWrapper(object):
    """Crea una entidad de Cloud Datastore dada una string."""

    def __init__(self, namespace, kind):
        self._namespace = namespace
        self._kind = kind

    def make_entity(self, content):
        pass

def write_to_datastore(user_options, pipeline_options):
    """Crea un pipeline que escribe entidades a Cloud Datastore."""
    with beam.Pipeline(options=pipeline_options) as p:
        #(p
        # | 'leer archivo' >>
        # | 'crear entidad' >>
        # | 'escribir en Datastore' >>)
         pass

def run(argv=None):
    """Punto de acceso principal que corre el pipeline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--input',
                        dest='input',
                        default='gs://geo-sports-database-input/athletes.csv',
                        help='Archivo de entrada para procesar.')
    parser.add_argument('--kind',
                        dest='kind',
                        default='Athlete',
                        help='Clase de Datastore')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Se obtienen las opciones del pipeline a traves de los argumentos.
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    # Escribir a datastore
    write_to_datastore(known_args, pipeline_options)

if __name__=='__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
