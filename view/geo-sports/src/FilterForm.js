import React, { Component } from 'react';
import Plot from 'react-plotly.js';

class FilterForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sex: '',
      year: '',
      results: {}
    };
  }

  componentDidMount() {
    this.requestPlayers();
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({[name]: value}, this.requestPlayers);
  }

  requestPlayers = () => {
    fetch('https://us-central1-geo-sports.cloudfunctions.net/countAthletesByCountry', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
              "sex": this.state.sex,
              "year": this.state.year
            })
    }).then( r => r.json())
     .then( r => this.setState({results: r}));
  }

  render() {
    console.log(this.state);
    console.log(Object.keys(this.state.results));
    console.log(Object.values(this.state.results));
    const years = [...Array(69).keys()].map( i => i + 1950 );
    return (
      <div>
        <form>
          <label>
            Gender:
            <select value={this.state.sex} onChange={this.handleChange} name="sex">
              <option value=''>Both</option>
              <option value='female'>Female</option>
              <option value='male'>Male</option>
            </select>
          </label>
          <label>
            Birth Year:
            <select value={this.state.year} onChange={this.handleChange} name="year">
              <option value=''>All years</option>
              {years.map( i => <option value={i}>{i}</option> )}
            </select>
          </label>
        </form>
        <Plot
          data={[{
                  type: 'choropleth',
                  locations: Object.keys(this.state.results),
                  z: Object.values(this.state.results),
                }]}
          layout={{title: 'Players by Country',
                   width: window.innerWidth - 20,
                   height: window.innerWidth * 0.45
                 }}
        />
      </div>
    );
  }
}

export default FilterForm;
