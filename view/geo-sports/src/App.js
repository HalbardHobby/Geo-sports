import React, { Component } from 'react';
import FilterForm from './FilterForm';
import CloroMap from './CloroplethMap';
import logo from './logo.svg';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Geo Sports</h1>
        </header>
        <FilterForm/>
        <CloroMap/>
      </div>
    );
  }
}

export default App;
