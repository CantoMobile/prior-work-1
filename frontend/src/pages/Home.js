import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { SearchBar } from '../components/SearchBar'
import axios from 'axios'

export default function Home() {
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
        <SearchBar/>
        <p>React + Flask</p>
        <p onClick={updateX}>The current time is {x}</p>
          <Link to="/addsite" >Add a Site to Index</Link>
            
      
    </div>
  );
}