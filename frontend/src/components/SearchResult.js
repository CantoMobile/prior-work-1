import React, { useState } from 'react'


export const SearchResult = ({ link, name, description }) => {
    return (
        
        <div className="singleResult">
            {console.log(link, description)}
            <div className="siteName">
                {link}
            </div>
            <a href={link}>
                <div className="siteDescription">
                    {name}
                </div>
            </a>
            
        </div>
    )

}