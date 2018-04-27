'use strict'

// dependencia a la libreria de datastore
const Datastore = require('@google-cloud/datastore');
//instancia un cliente
const datastore = Datastore();

/**
 * Provee una lista de la cantidad de atletas registrados por pais según
 * los filtros parametros solicitados por el usuario.
 *
 * @param {!Object} req Objeto Json de contexto cloud conteniendo el request
 *                      del usuario.
 * @param {!Object} res Objeto Json con .una lista de los paises y la cantidad
 *                      de atletas registrados
 */
exports.countAthletesByCountry = (req, res) => {

  // Verificar tipo de contenido
  if (req.get('content-type') !== 'application/json'){
    // En caso de no ser una petición json, es rechazada.
    res.status(400).send('JSON required.').end();
  }
  else {
    /**
     * Entrada de ejemplo:
     * {"sex": "male",
     *  "year": 1980}
     */

    // se crea una query solo con los elementos a filtrar.
    const query = datastore.createQuery('Aggregate')

    // Verificar si hay campos adicionales y no son vacíos. En caso de no ser
    // vacíos se aplican los filtros apropiados.
    if(req.body.sex !== undefined && req.body.sex !== '')
      query.filter('sex', '=', req.body.sex);
    if(req.body.year !== undefined && req.body.year !== '')
      query.filter('year', '=', req.body.year);

    // Se corre la query y se procesa el resultado.
    datastore.runQuery(query).then( results => {
      // Se crea un objeto vacío que sirve como buffer para los resultados.
      const countries = {};
      const agg = results[0]

      agg.forEach( r => {
        // Si el campo es nulo se crea un contador en 0.
        if (countries[r.country] === undefined){
          countries[r.country] = 0;
        }
        countries[r.country] = countries[r.country] + r.total;
      })
      res.status(200).send(countries);
    })
  }
};
