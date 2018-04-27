from __future__ import absolute_import

import argparse
import logging
from datetime import datetime

# dependencias necesarias para el ETL
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# Dependencias para metricas
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter

# dependencias para escritura en base de datos.
from google.cloud.proto.datastore.v1 import entity_pb2
from apache_beam.io.gcp.datastore.v1.datastoreio import WriteToDatastore

from googledatastore import helper as datastore_helper
from googledatastore import PropertyFilter

class AthleteEntityWrapper(object):
    """Crea una entidad de Cloud Datastore dada una string."""

    def __init__(self, kind):
        """Inicializa la entidad con un kind predeterminado."""
        self._kind = kind

    def make_entity(self, content):
        """Parsea el contenido del string para crear una entidad de Datastore."""
        props = content.split(',')
        entity = entity_pb2.Entity()

        # Crear la llave de la entidad
        datastore_helper.add_key_path(entity.key, self._kind, props[0])

        # Se anhaden las propiedades
        properties = {"name": props[1],
                      "country": props[2],
                      "sex": props[3],
                      "date_of_birth": datetime.strptime(props[4], "%Y-%m-%d"),
                      "height": props[5],
                      "weight": props[6],
                      "gold": props[7],
                      "silver": props[8],
                      "bronze": props[9],
                      "info": props[10]}
        datastore_helper.add_properties(entity, properties)
        return entity

class AggregateEntityWrapper(object):
    """Crea una entidad del agregado en Datastore dada una tupla."""

    def make_entity(self, content):
        """Con una tupla dada genera una entrada en datastore de los agregados."""
        entity = entity_pb2.Entity()
        datastore_helper.add_key_path(entity.key, 'Aggregate')

        properties = {"country": content[0][0],
                      "sex": content[0][1],
                      "year": content[0][2],
                      "total": content[1]}
        datastore_helper.add_properties(entity, properties)
        return entity


class StripProperties(beam.DoFn):
    """Parsea cada linea del csv como un diccionario eliminando campos
    innecesarios para el conteo."""

    def process(self, element):
        """Retorna un string de cada atleta en el cual solo se tiene en
        cuenta el pais de origen, el sexo y el anho de nacimiento.
        Args:
          element: el elemento de entrada para procesar.
        Returns:
          la tupla descrita.
        """
        props = element.split(',')
        dicc = (props[2],
                props[3],
                datetime.strptime(props[4], "%Y-%m-%d").year)
        logging.info(dicc)
        yield dicc

def write_to_datastore(user_options, pipeline_options):
    """Crea un pipeline que escribe entidades a Cloud Datastore."""
    def count_athletes(athletes):
        athletes, ones = athletes;
        tuple = (athletes, sum(ones))
        logging.info(tuple)
        return tuple

    with beam.Pipeline(options=pipeline_options) as p:
        p0 = (p | 'leer archivo' >> ReadFromText(user_options.input))

        p1 = (p0 | 'Crear entidad de atleta' >> beam.Map(
                        AthleteEntityWrapper(user_options.kind).make_entity))

        p2 = (p0 | 'Eliminar propiedades' >> beam.ParDo(StripProperties())
                 | 'Generar agregados' >> beam.combiners.Count.PerElement()
                 | 'Crear entidad de agregados' >>  beam.Map(
                        AggregateEntityWrapper().make_entity))

        p3 = ((p1, p2) | 'Unir colecciones' >> beam.Flatten()
                       | 'escribir en Datastore' >> WriteToDatastore(user_options.dataset))

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
    parser.add_argument('--dataset',
                        dest='dataset',
                        default='geo-sports',
                        help='Id del dataset de datastore')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Se obtienen las opciones del pipeline a traves de los argumentos.
    # Se guarda la sesion principal ya que hay operaciones que dependen del
    # contexto global
    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True

    # Escribir a datastore
    write_to_datastore(known_args, pipeline_options)

if __name__=='__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()

# Comando completo para ejecutar el etl. requiere certificados de acceso.
# python2 etl.py\
#  --project geo-sports\
#  --runner DataflowRunner\
#  --staging_location gs://geo-sports-database-input/staging \
#  --temp_location gs://geo-sports-database-input/temp \
#  --output gs://geo-sports-database-input/output
