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

    if(req.body.sex !== undefined)
      query.filter('sex', '=', req.body.sex)
    if(req.body.year !== undefined)
      query.filter('year', '=', req.body.year)

    datastore.runQuery(query).then( results => {
      console.log(results[0].length);
      res.status(200).send({'result': results[0].length});
    })
  }
};
