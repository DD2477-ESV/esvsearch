import React, { useState } from "react";
import ResultPage from "./ResultPage";
import "./../styles/HomePageStyles.css";
import "./../styles/CheckBoxesStyles.css";

const HomePage = () => {
        const [results, setResult] = useState([]); // Sätter

        /*
    Funktion för att hantera responsen som kommer i json
    Sätter result-statet till 
    */
        const handleResponse = (res) => {
                let pdfsToView = [];

                // För exemplet på en sökning
                //console.log(res._source)
                // Det här får väl typ göras i en for-loop sen gissar jag
        /*
                let title = res._source.titel;
                let organ = res._source.organ;
                let url = res._source.dok_url;
                let docInfo = { title, organ, url };
                console.log(docInfo);
                pdfsToView.push(docInfo);
        */
        const hits = res.hits.hits;
        for (let i = 0; i < hits.length; i++) {
            const resHit = hits[i];
            //console.log(resHit);
            let title = resHit.fields.title[0];
            let url = resHit.fields.download_url[0];
            let preview = resHit.highlight;
            let docInfo = { title, preview, url };
            console.log(docInfo)
            pdfsToView.push(docInfo);
        }
                // Set state to found documents
                setResult(pdfsToView);
        };

        const searchButtonClicked = (e) => {
                e.preventDefault();
                alert("Sökt");

                // Skicka iväg en request med sökningen
                // vänta på response...
                // ta emot response....
                fetch("Example_result.json")
                        .then(function (response) {
                                console.log(response);
                                return response.json();
                        })
            .then(function (myJson) {
                console.log(myJson)
                                handleResponse(myJson);
                        });
        };

        return (
                <div>
            {
                results.length !== 0 ? (
                                <ResultPage documents={results} />
                        ) : (
                                <div className="topnav">
                                        <a className="active" href="#home">
                                                Home
                                        </a>
                                        <input type="text" placeholder="Sök.." />
                                        <link
                                                rel="stylesheet"
                                                href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
                                        ></link>
                                        <button
                                                onClick={searchButtonClicked}
                                                className="homepage-search-button"
                                                type="submit"
                                        >
                                                <i className="fa fa-search"></i>
                                        </button>
                                        <h3 className="h3_checkboxes">Myndigheter</h3>
                                        <div className="container">
                                                <input type="checkbox" /> Arbetsförmedlingen <br />
                                                <input type="checkbox" /> Prepositioner <br />
                                                <input type="checkbox" /> Annat <br />
                                                <input type="checkbox" /> Annat <br />
                                                <input type="checkbox" /> Annat <br />
                                                <input type="checkbox" /> Annat <br />
                                        </div>
                                </div>
                        )}
                </div>
        );
};

export default HomePage;