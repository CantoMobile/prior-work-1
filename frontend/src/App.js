import './App.css';
import React, { useEffect, useState } from 'react';
import { SearchBar } from './components/SearchBar'
import axios from 'axios'

function App() {
  const [getMessage, setGetMessage] = useState({})
  const [x, setX] = useState(0)
  const [data, setData] = useState([{}]);

  // useEffect(()=>{
  //   axios.get('http://127.0.0.1:5000').then(response => {
  //     console.log("SUCCESS", response)
  //     setGetMessage(response)
  //   }).catch(error => {
  //     console.log(error)
  //   })
  // }, [])

  const updateX = () => {
    setX(x+1)
    console.log(x)
  }

  return (
    <div className="App">
        <h1 onClick={updateX}>CANTONICA</h1>
        <SearchBar/>
        <p>React + Flask</p>
        <p onClick={updateX}>The current time is {x}</p>
        <div>{getMessage.status === 200 ? 
          <h3>{getMessage.data.message}</h3>
          :
          <h3>LOADING</h3>}</div>
      
    </div>
  );
}

export default App;