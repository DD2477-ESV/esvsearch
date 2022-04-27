import React, { useState, useEffect } from "react";

import "./../styles/ResultPageStyles.css";

const ResultPage = (props) => {
	const [docToView, setDocToView] = useState("");
	const [documentsToView, setDocumentsToView] = useState([]);

	useEffect(() => {
		props.documents.length < 20
			? setDocumentsToView(props.documents)
			: setDocumentsToView(props.documents.slice(0, 20));
		// Det här kollar hur många dokument vi har i resultatet och hur många dokument vi vill visa
	}, []);

	const documentClicked = (e) => {
		//e.preventDefault();
		docToView === e.target.value
			? setDocToView("")
			: setDocToView(e.target.value);
		console.log(e.target.value);
	};

	const viewMoreClicked = (e) => {
		if (documentsToView.length + 10 < props.documents.length) {
			const currentNumberOfDocuments = documentsToView.length;
			setDocumentsToView(
				documentsToView.concat(
					props.documents.slice(
						currentNumberOfDocuments,
						currentNumberOfDocuments + 10
					)
				)
			);
		} else {
			setDocumentsToView(props.documents);
		}
	};

	// https://github.com/wojtekmaj/react-pdf
	return (
		<div className="result-page-container">
			<div className="all-results-container">
				<h3>{"Visar " + documentsToView.length + " dokument"}</h3>
				{documentsToView.map((doc) => {
					return (
						<div key={doc.url} className="single-result-container">
							<h3>{doc.title}</h3>
							<button
								value={doc.url}
								onClick={documentClicked}
								className="single-result-container-open-button open-button-specific"
							>
								{docToView === doc.url ? "Stäng" : "Öppna här"}
							</button>
							<a href={doc.url} target="_blank">
								<button
									value={doc.url}
									className="single-result-container-open-button"
								>
									{"Ladda ner"}
								</button>
							</a>
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
			{documentsToView.length === props.documents.length ? (
				<p>Inga fler dokument att visa...</p>
			) : (
				<button onClick={viewMoreClicked} className="single-result-container-open-button">Visa fler dokument</button>
			)}
		</div>
	);
};

/*
{props.documents.map((doc) => {
					return (
						<div key={doc.url} className="single-result-container">
							<h3>{doc.title}</h3>
							<button
								value={doc.url}
								onClick={documentClicked}
								className="single-result-container-open-button open-button-specific"
							>
								{docToView === doc.url ? "Stäng" : "Öppna här"}
							</button>
							<a href={doc.url} target="_blank">
								<button
									value={doc.url}
									className="single-result-container-open-button"
								>
									{"Ladda ner"}
								</button>
							</a>
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
*/
export default ResultPage;
