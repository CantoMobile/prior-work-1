import React, { useState, useEffect } from 'react'
import SearchIcon from '@mui/icons-material/Search';
import '../App.css';
import { SearchResult } from './SearchResult'
import { SendQuery } from './APIService'

export const SearchBar = () => {
    const [searchInput, setSearchInput] = useState("");
    const [data, setData] = useState("");
    const [filteredResults, setFilteredResults] = useState([]);

    

    //   const response = await fetch("http://localhost:5000/Search", {
    //         method: "POST",
    //         headers: {
    //             'Content-Type':'application/json'
    //         },
    //         body: JSON.stringify({query: input})
    //     })

    //   useEffect(() => {
    //     fetch("http://localhost:5000/Search", {
    //         method: "GET",
    //         headers: {
    //             'Content-Type':'application/json'
    //         },
    //         body: JSON.stringify({query: input})
    //     }).then(
    //         res => res.json()
    //     ).then(
    //         data => {
    //             setData(data)
    //             console.log("data")
    //             console.log(data)
    //         }
    //     )
    //   }, [searchInput])

      const handleChange = async (e) => {
        e.preventDefault();
        setSearchInput(e.target.value);
        const input = e.target.value
        // const response = await fetch("http://localhost:5000/Search", {
        //     method: "POST",
        //     headers: {
        //         'Content-Type':'application/json'
        //     },
        //     body: JSON.stringify({query: input})
        // }).then(response => response.json())
        // .catch(error => {console.log(error); console.log(JSON.stringify({query: input}))})

        const searchResults = ['https://www.microsoft.com/en-ca', 'https://www.disney.com/', 'https://www.starbucks.com',
        'https://www.sony.com/en/', 'https://www.dotdashmeredith.com/', 'https://dribbble.com/',
        'https://github.com/', 'https://www.shopify.com/ca', 'https://www.paypal.com/us/home', "https://www.amazon.com"]//await fetch("http://localhost:5000/Search", {
        //     method: "GET",
        //     headers: {
        //         'Content-Type':'application/json'
        //     }
        // }).then(response => response.json())
        // .catch(error => console.log(error))
        console.log(`Search results: ${typeof searchResults}`)
        console.log(searchResults)

        // const newResults = countries.filter((country) => {
        //     return country.name.toLowerCase().includes(input.toLowerCase()) || country.continent.toLowerCase().includes(input.toLowerCase())
        // })

        if (input === "") {
            setFilteredResults([])
        } else {
            setFilteredResults(searchResults)
        }
        
      };

     

      return (
        <div>
            <div className="searchBar">
                <input
                type="search"
                placeholder="Search here"
                onChange={handleChange}
                value={searchInput} />
                <div className="searchIcon">
                </div>
            </div>
            {filteredResults.length != 0 && (
            <div>
                <table className="searchResults">
                    <tbody>
                        <tr>
                            <th>Results</th>
                        </tr>
                        {filteredResults.slice(0, 6).map((result) => {
                            return (<SearchResult /*key={result.id}*/ link={result} /*name={result.name} description={result.description}*/ />
                        )})}
                    </tbody>
                </table>
            </div>
            )}

        </div>
      )

}