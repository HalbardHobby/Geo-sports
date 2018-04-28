import React, { Component } from 'react';

class FilterForm extends Component {
  constructor(props) {
    super(props);
    this.state = {
      sex: '',
      year: '',
      results: {}
    };

    this.handleChange = this.handleChange.bind(this);
    this.requestPlayers = this.requestPlayers.bind(this);
  }

  handleChange(event) {
    const value = event.target.value;
    const name = event.target.name;
    this.setState({[name]: value})
    this.requestPlayers();
  }

  componentDidMount() {
    this.requestPlayers();
  }

  requestPlayers() {
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
     .then( r => console.log(r));
  }

  render() {
    const years = [...Array(69).keys()].map( i => i + 1950 );
    return (
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
    );
  }
}

export default FilterForm;
