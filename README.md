# Geo Sports

Pequeña aplicación desarrollada en cloud con diferentes tecnologías y
herramientas. disponible en [Geo Sports](https://geo-sports.firebaseapp.com/).

## Estructura del proyecto

- `etl/`: Esta carpeta contiene la definición y ejecución del workflow
    utilizado para la ingesta de dstos hacia Cloud Datastore.
- `api/`: Aqui se encuentra la definición del servicio para la consulta de la
    información almacenada.
- `view/`: Proyecto desarrollado en React para el acceso al servicio REST.

## Tecnologías utilizadas

- **Servicios cloud**
  - [Google Cloud Dataflow](https://cloud.google.com/dataflow/):
      Servicio de transferencia y transformación de datos.
  - [Google Cloud Storage](https://cloud.google.com/storage/):
      Servicio de almacenamiento de información no estructurada.
  - [Google Cloud Datastore](https://cloud.google.com/datastore/):
      Servicio de base de datos NoSQL altamente escalable.
  - [Google Cloud Functions (beta)](https://cloud.google.com/functions/):
      PLataforma de computo _serverless_ manejado por eventos.
  - [Firebase static hosting](https://firebase.google.com/products/hosting/):
      Hosting con grado de producción para aplicaciones web y contenido estático.
- **Librerias de desarrollo**
  - [Apache Beam](https://beam.apache.org/):
      Modelo unificado para la definición y ejecución de workflows de procesamiento
      de datos.
  - [React](https://reactjs.org/):
      Libreria Javascript para la creación de interfaces de usuario.
  - [Plotly](https://plot.ly/):
      Herramientas open source para la creación y edición de visualizaciones de
      información vía web.
  - [react-plotly](https://github.com/plotly/react-plotly.js/):
      Integración de plotly como componente de React.
- **Herramientas adicionales**
  - [create-react-app](https://github.com/facebook/create-react-app):
      Herramienta open source para la creación de aplicaciones React sin
      configuraciones iniciales.
  - [Google Cloud SDK](https://cloud.google.com/sdk/**):
      Interfaz de linea de comandos para los productos y servicios de GCP .
  - [Firebase Tools](https://github.com/firebase/firebase-tools):
      Interfaz de linea de comandos para los productos y servicios de Firebase.

## Descripción Arquitectural

Para el desarrollo del proyecto se recurrió a una arquitectura de tres capas,
implementadas siguiendo una aproximación de microservicios haciendo una
descomposición de funcionallidad como es descrita por
[_Martin Fowler_](https://martinfowler.com/articles/microservices.html) teniendo
servicios independientes para cada una de los componentes requeridos. A
continuación se presenta un diagrama de la solución desplegada en Google Cloud
Platform.

![Referencia Arquitectural](images\Referencia Arquitectural.png)

### ETL y base de datos
La primera capa de la solución es la ingesta de información (normalmente
referida como ETL) y el almacenamiento en base de datos. Para lograr esto se
utilizó el servicio de Dataflow para crear el pipeline de ingesta de la
información a partir de un bucket creado en Google Cloud Storage.

![Pipeline de ingesta](images\Dataflow Pipeline.PNG)

Pensando en el tipo de consultas que se equieren de la solución se dividió el
pipeline en dos partes; una encargada de mapear los jugadores a entidades de
Datastore y la otra encargada de generar agregados para disminuir el número de
registros para revisar durante la consulta (se logró reducir de más de 11.000
entidades hasta apróximadamente 3.600). A Continuación se presenta una imagen de
las diferentes entidades generadas a partir del pipeline.

#### Entidades de jugador
![Entidades de jugador](images\Datastore Athlete.PNG)

#### Entidades de agregados
![Entidades de Agregado](images\Datastore Aggregate.PNG)

### API

Para la creación del API se recurrió a una solución _serverless_ dada la
funcionalidad tan sencilla a implementar. Para este caso específico se decidió
utilizar Google Cloud Functions, pemitiendo una implementación en extremo
sencilla del servicio. Aún así debido a la naturaleza de descomposición de
servicios y la estructuración de proyectos en GCP, es necesario agregar el
manejo para peticiones de tipo `OPTIONS` para permitir el uso de CORS en la
vista.

Finalmente una implementación severless reduce el overhead operativo de
aprovisionamiento y escalamiento de infraestructura. A cambio se puede
experimentar una baja de desempeño las primeras veces que se ejecuta el servicio
despues de un tiempo, ya que debe ser aprovisionado y escalado por el proveedor
de forma dinámica.

### Vista
Finalmente paa el componente de vista de la aplicación se recurrió a un
desarrollo en React, haciendo un scaffold de la misma a través de la herramienta
create-react-app, reduciendo el tiempo de desarrollo debido a la configuración
de todas las dependencias. Para la creación del mapa se recurrió a la libreria
plotly que facilita la creación de visualizaciones de datos vía web.

![Geo Sports](images\Geo Sports.PNG)

En cuanto al despliegue de la vista se recurrió a una solución similar que el
API haciendo miras a una aplicación _serverless_. Para lograr esto se utilizó el
servicio de aprovisionamiento estático de Firebase.

## Despliegue
A continuación se describe de forma breve como desplegar cada componente de la
solución para poder ofrecer el servicio diseñado a través de internet. Se asume
la configuración previa de las herramientas de comando y variables de entorno
para las mismas.

### ETL y base de datos

Para ejecutar el etl y generar las entidades en la base de datos es
prerrequisito tener los .csv bien formados para procesar en un bucket de Cloud
Storage y las autorizaciones de servicio necesarias tanto en consola como en la
maquina local.

```
python2 etl.py\
  --project [ID del proyecto]\
  --runner DataflowRunner\
  --staging_location [Url del bucket]/staging \
  --temp_location [Url del bucket]/temp \
  --output [Url del bucket]/output
```

Este comando corre el pipeline diseñado con Apache Beam de forma remota sobre el
runner de Dataflow en el proyecto y bucket seleccionado.

### Servicio REST

El despliegue del sevicio REST consiste unicamente en la ejecución del siguiente
comando.

```
gcloud beta functions deploy countAthletesByCountry\
  --trigger-http\
  --stage-bucket [Url del bucket]
```

Este comando despliega la función con un trigger http, permitiendo su acceso vía
web y con las configuraciones predeterminadas para la ejecución de la función.

### Vista para usuario final

Finalmente para el despliegue de la vista se requiere la edición del archivo
`.firebaserc` para señalar al proyecto correcto y ejecutar los siguientes comandos.

```
npm run build
firebase deploy
```

Con la ejecución de estos comandos se crea la versión de despliegue de la vista
y a su vez es desplegada en el servidor de contenido estático de Firebase.

## Autor

- __Alejandro Espinosa__
