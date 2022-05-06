import React, { useState, useEffect } from "react";

import "./../styles/ResultPageStyles.css";

const ResultPage = (props) => {
	const [docToView, setDocToView] = useState("");
	const [allDocuments, setAllDocuments] = useState([]);
	const [documentsToView, setDocumentsToView] = useState([]);
	const [chosenSorting, setChosenSorting] = useState("relevance");

	useEffect(() => {
		setAllDocuments(props.documents); // So we can access the original documents later
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
					allDocuments.slice(
						currentNumberOfDocuments,
						currentNumberOfDocuments + 10
					)
				)
			);
		} else {
			setDocumentsToView(allDocuments);
		}
	};

	/* Functions for handling the sorting of results */

	let chosenValue = ""

	const compare = (a, b) => {
		switch (chosenValue) {
			case "relevance":
				console.log("TODO");
				break;
			case "date":
				console.log("TODO");
			case "title":
				if (a.title < b.title) {
					return -1;
				}
				if (a.title > b.title) {
					return 1;
				}
				return 0;
				break;
			default:
				return 0;
		}
	};

	const sortButtonClicked = (e) => {
		chosenValue = e.target.value;
		setChosenSorting(e.target.value)
		if (e.target.value === "relevance") {
			setAllDocuments(props.documents)
		} else {
			setAllDocuments(allDocuments.sort(compare));
		}
	};

	// https://github.com/wojtekmaj/react-pdf
	return (
		<div className="result-page-container">
			{/* <div className="container-sort-results">
				{" "}
				<h3>Sortera resultat efter</h3>
				<div className="sort-results-alternatives-box">
					<button
						value="relevance"
						className={
							chosenSorting === "relevance"
								? "active-sorting single-result-container-open-button"
								: "single-result-container-open-button"
						}
						onClick={sortButtonClicked}
					>
						Relevans
					</button>
					<button
						value="date"
						className={
							chosenSorting === "date"
								? "active-sorting single-result-container-open-button"
								: "single-result-container-open-button"
						}
						onClick={sortButtonClicked}
					>
						Datum
					</button>
					<button
						value="title"
						className={
							chosenSorting === "title"
								? "active-sorting single-result-container-open-button"
								: "single-result-container-open-button"
						}
						onClick={sortButtonClicked}
					>
						Titel
					</button>
				</div>
			</div> */}

			<div className="all-results-container">
				<h3>{"Visar " + documentsToView.length + " dokument"}</h3>
				{documentsToView.map((doc) => {
					return (
						<div key={doc.url} className="single-result-container">
							<h3>{doc.title}</h3>
							<h5>{doc.index}</h5>
							{/* <div>
								{
									doc.preview.text.map((elem) => {
										return elem;
									})
								}
							</div> */}
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
							{docToView === doc.url && doc.url !== '' ? (
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
				<button
					onClick={viewMoreClicked}
					className="single-result-container-open-button"
				>
					Visa fler dokument
				</button>
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
