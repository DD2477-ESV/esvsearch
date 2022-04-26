import React, {useState, useEffect} from 'react'
import "./../styles/ResultPageStyles.css"

const ResultPage = (props) => {
        const [docToView, setDocToView] = useState("");

        useEffect(() => {
                console.log(props);
        }, []);

        const documentClicked = (e) => {
                //e.preventDefault();
                setDocToView(e.target.value);
                console.log(e.target.value);
        };

        // https://github.com/wojtekmaj/react-pdf
        return (
                <div>
                        <div>
                                {props.documents.map((doc) => {
                                        return (
                                                <div key={doc.url}>
                                                        <h3>{doc.title}</h3>
                                                        <button value={doc.url} onClick={documentClicked}>
                                                                Öppna
                                                        </button>
                                                </div>
                                        );
                                })}
                        </div>

                        <div>
                                {/* <ViewDocument docURL={docToView} /> */}
                                <iframe
                    src={ docToView }
                    frameBorder="0"
                    className="pdf-in-browser"
                                ></iframe>
                        </div>
                </div>
        );
};

export default ResultPage;
