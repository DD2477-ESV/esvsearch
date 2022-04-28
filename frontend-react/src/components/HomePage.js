import React, { useState, useEffect } from "react";
import axios from "axios";

import ResultPage from "./ResultPage";
import "./../styles/HomePageStyles.css";
import "./../styles/CheckBoxesStyles.css";

const HomePage = () => {
	const [results, setResult] = useState([]);
	// All input states here
	const [termsToMatch, setTermsToMatch] = useState("");
	const [phrase, setPhrase] = useState("");
	const [termsNotToMatch, setTermsNotToMatch] = useState("");
	const [dateFrom, setDateFrom] = useState("");
	const [dateTo, setDateTo] = useState("");

	const handleResponse = (res) => {
		let pdfsToView = [];
		const hits = res.hits.hits;
		for (let i = 0; i < hits.length; i++) {
			const resHit = hits[i];
			//console.log(resHit);
			let title = resHit.fields.title[0];
			let url = resHit.fields.download_url[0];
			let preview = resHit.highlight;
			let docInfo = { title, preview, url };
			console.log(docInfo);
			pdfsToView.push(docInfo);
		}
		// Set state to found documents
		//setResult(pdfsToView);
	};

	const newSearchClicked = (e) => {
		setResult([]);
	};

	const makeRequest = (req) => {
		console.log(req);
		const headers = {
			"Content-Type": "application/json",
		};
		axios.post("http://localhost:9200/_all/_search", JSON.stringify(req), { headers }).then(
			(response) => {
				console.log(response);
			},
			(error) => {
				console.log(error);
			}
		);
	};

	const searchButtonClicked = (e) => {
		console.log(termsToMatch);

		let jsonObject = {
			query: {
				bool: {
					must: [
						{
							match: {
								text: {
									query: termsToMatch,
									operator: "and",
								},
							},
						},
					],
				},
			},
			fields: ["url", "download_url", "date", "title"],
			sort: [
				{
					date: {
						order: "desc",
					},
				},
			],
			highlight: {
				fields: {
					text: {},
				},
			},
			_source: false,
		};

		console.log(jsonObject);
		makeRequest(jsonObject);
	};

	return (
		<div className="homepage-main-container">
			{results.length !== 0 ? (
				<div className="result-page-container">
					<h2>{"Din sökning gav " + results.length + " resultat"}</h2>
					<ResultPage documents={results} />
					<button onClick={newSearchClicked} className="new-search-button">
						Ny sökning
					</button>
				</div>
			) : (
				<div className="topnav">
					{/* <a className="active" href="#home">
						Home
					</a> */}
					<h1>Ny sökning</h1>
					<h3>Hitta rapporter</h3>
					<div className="search-fields">
						<input
							type="text"
							placeholder="Innehållandes dessa ord..."
							value={termsToMatch}
							onChange={(e) => setTermsToMatch(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Innehållandes denna fras..."
							value={phrase}
							onChange={(e) => setPhrase(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Utan dessa ord..."
							value={termsNotToMatch}
							onChange={(e) => setTermsNotToMatch(e.target.value)}
						/>
						<p>Mellan följande år</p>
						<input
							type="text"
							placeholder="Från"
							value={dateFrom}
							onChange={(e) => setDateFrom(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Till"
							value={dateTo}
							onChange={(e) => setDateTo(e.target.value)}
						/>
					</div>
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
						<input type="checkbox" /> Finansinspektionen <br />
						<input type="checkbox" /> Annat <br />
						<input type="checkbox" /> Annat <br />
						<input type="checkbox" /> Annat <br />
					</div>
				</div>
			)}
			<link
				rel="stylesheet"
				href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
			></link>
		</div>
	);
};

export default HomePage;
