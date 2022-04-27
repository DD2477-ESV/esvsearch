import React, { useState, useEffect } from "react";

import "./../styles/ResultPageStyles.css";

const ResultPage = (props) => {
	const [docToView, setDocToView] = useState("");

	useEffect(() => {
		console.log(props);
	}, []);

	const documentClicked = (e) => {
		//e.preventDefault();
		docToView === e.target.value
			? setDocToView("")
			: setDocToView(e.target.value);
		console.log(e.target.value);
	};

	// https://github.com/wojtekmaj/react-pdf
	return (
		<div className="result-page-container">
			<div className="all-results-container">
				{props.documents.map((doc) => {
					return (
						<div key={doc.url} className="single-result-container">
							<h3>{doc.title}</h3>
							<button
								value={doc.url}
								onClick={documentClicked}
								className="single-result-container-open-button"
							>
								{docToView === doc.url ? "Stäng" : "Öppna"}
							</button>
							{docToView === doc.url ? (
								<div className={"pdf-to-view"}>
									<iframe
										src={docToView}
										frameBorder="0"
										className="pdf-in-browser"
									></iframe>
								</div>
							) : (
								<p></p>
							)}
						</div>
					);
				})}
			</div>
		</div>
	);
};

export default ResultPage;
