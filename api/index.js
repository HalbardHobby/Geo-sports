'use strict'

// dependencia a la libreria de datastore
const Datastore = require('@google-cloud/datastore');
//instancia un cliente
const datastore = Datastore();

/**
 * Responds to any HTTP request that can provide a "message" field in the body.
 *
 * @param {!Object} req Cloud Function request context.
 * @param {!Object} res Cloud Function response context.
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
     *  "bornBefore": 2012-04-23T18:25:43.511Z,
     *  "bornAfter": 1990-04-23T18:25:43.511Z}
     */
    sex = req.body.sex;
    bornBefore = req.body.bornBefore;
    bornAfter = req.body.bornAfter;
  }
};
