import React, { Component } from 'react';

class FilterForm extends Component {
  constructor() {
    super();
    this.state = {
      sex: '',
      year: '',
      results: {}
    };

    this.handleChange = this.handleChange.bind(this);
  }

  handleChange(event) {
    const value = event.target.value;
    const name = event.target.name;
  }

  componentDidMount() {
    fetch('https://us-central1-geo-sports.cloudfunctions.net/countAthletesByCountry', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'http://localhost:3000',
      },
      body: JSON.stringify({
        sex: this.state.sex,
        year: this.state.year,
      })
    }).then(result => result.json)
    .then(items => {
      items.forEach(i=>console.log(i));
    })
  }

  render() {
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
          <input value={this.state.year} onChange={this.handleChange}
              type="number" name="year" min="1950" max="2018"/>
        </label>
      </form>
    );
  }
}

export default FilterForm;
