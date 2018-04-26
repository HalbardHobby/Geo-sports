from __future__ import absolute_import

import argparse
import logging
from datetime import datetime

# dependencias necesarias para el ETL
import apache_beam as beam
from apache_beam.io import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

# dependencias para escritura en base de datos.
from google.cloud.proto.datastore.v1 import entity_pb2
from apache_beam.io.gcp.datastore.v1.datastoreio import WriteToDatastore

from googledatastore import helper as datastore_helper
from googledatastore import PropertyFilter

class csvLoadDoFn(beam.DoFn):
    """Parsea cada linea del csv como una entidad de datastore."""

    def __init__(self):
        """Inicializa el proceso segun los lineamientos de apache beam."""
        super(csvLoadDoFn, self).init()

class EntityWrapper(object):
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

        birth = datetime(1, 1, 1)
        try:
            birth = datetime.strptime(props[4], "%Y-%m-%d")
        except _:
            # En caso de no poder formatear correctamente la fecha de nacimiento
            # se da un valor por defecto.
            birth = datetime(1, 1, 1)
        finally:
            # Se anhaden las propiedades
            properties = {"name": props[1],
                          "country": props[2],
                          "sex": props[3],
                          "date_of_birth": birth,
                          "height": props[5],
                          "weight": props[6],
                          "gold": props[7],
                          "silver": props[8],
                          "bronze": props[9],
                          "info": props[10]}
            datastore_helper.add_properties(entity, properties)
            return entity

def write_to_datastore(user_options, pipeline_options):
    """Crea un pipeline que escribe entidades a Cloud Datastore."""
    with beam.Pipeline(options=pipeline_options) as p:
        (p
         | 'leer archivo' >> ReadFromText(user_options.input)
         | 'crear entidad' >> beam.Map(
             EntityWrapper(user_options.kind).make_entity)
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
