import React from 'react'
import "./../styles/HomePageStyles.css"

const HomePage = () => {

    const searchButtonClicked = (e) => {
        alert("sök");
    }

    return (
        <div className="container-homepage">
            <div className='container-search-form'>
                <h2 id="homepage-header">Sök bland dokument</h2>
                {/* Här kan vi då lägga in olika search-options */}
                <input type="text" placeholder='Nyckelord...'></input>
                <button onClick={searchButtonClicked} className="homepage-search-button">Sök</button>
            </div>
        </div>
    )
}

export default HomePage;