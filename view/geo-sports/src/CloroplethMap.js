import React, { Component } from 'react';
import Plot from 'react-plotly.js';


class CloroMap extends Component {
  render() {
    return (
      <Plot
        data={[
          {
            type: 'choropleth',
            locationmode: 'country names',
          },
        ]}
        layout={{title: 'Players by Country'}}
      />
    );
  }
}

export default CloroMap;
