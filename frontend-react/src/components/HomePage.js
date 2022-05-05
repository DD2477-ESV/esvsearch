import React, { useState, useEffect } from "react";
import axios from "axios";

import ResultPage from "./ResultPage";
import "./../styles/HomePageStyles.css";
import "./../styles/CheckBoxesStyles.css";

const HomePage = () => {
	const [results, setResult] = useState([]);
	// All input states here
	const [termsToMatch, setTermsToMatch] = useState("");
	const [phraseToMatch, setPhraseToMatch] = useState("");
	const [phraseNotToMatch, setPhraseNotToMatch] = useState("");

	const [termsNotToMatch, setTermsNotToMatch] = useState("");
	const [dateFrom, setDateFrom] = useState("");
	const [dateTo, setDateTo] = useState("");
	const [finalQuery, setFinalQuery] = useState({});
	const [myndigheter, setMyndigheter] = useState([])
	const [reqAddr, setReqAddr] = useState("http://localhost:9200/_all/_search")

	useEffect(() => {
		let jsonObject = {
			query: {
				bool: {},
				fields: ["url", "download_url", "date", "title"],
				highlight: {
					fields: {
						text: {},
					},
				},
				_source: false,
			},
		};

		setFinalQuery(jsonObject);
	}, []);

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
		setResult(pdfsToView);
	};

	const newSearchClicked = (e) => {
		setResult([]);
	};

	const makeRequest = (req) => {
		console.log(req);
		console.log(reqAddr)

		const headers = {
			"Content-Type": "application/json",
		};
		axios
			.post(reqAddr, JSON.stringify(req), {
				headers,
			})
			.then(
				(response) => {
					console.log(response);
					handleResponse(response.data);
				},
				(error) => {
					console.log(error);
				}
			);
	};

	const handleMust = () => {
		/*const [termsToMatch, setTermsToMatch] = useState("");
		const [phrase, setPhrase] = useState("");*/
		let must = [];
		let matchObject = {};
		let changed = false;
		console.log(finalQuery);
		if (termsToMatch !== "") {
			matchObject["query"] = termsToMatch;
			matchObject["operator"] = "and";
			changed = true;
		}
		if (phraseToMatch !== "") {
			matchObject["match_phrase"] = phraseToMatch;
			changed = true;
		}

		if (changed === true) {
			must.push(matchObject);
			let query = finalQuery;
			query.query.bool["must"] = must;
			setFinalQuery(query);

			console.log("Final Query: ");
			console.log(finalQuery);
		}
	};

	const handleMustNot = () => {
		let must_not = [];

		let matchNotObject = {};

		let changed = false;

		if (termsNotToMatch !== "") {
			matchNotObject["query"] = termsNotToMatch;
			matchNotObject["operator"] = "and";
			changed = true;
		}

		if (phraseNotToMatch !== "") {
			matchNotObject["match_phrase"] = phraseNotToMatch;
			changed = true;
		}

		if (changed === true) {
			must_not.push(matchNotObject);
			let query = finalQuery;
			query.query.bool["must_not"] = must_not;
			setFinalQuery(query);
		}
	};

	const handleDates = () => {
		let filter = {
			range: {
				date: {},
			},
		};
		let changed = false;
		if (dateFrom !== "") {
			changed = true;
			filter.range.date["gte"] = dateFrom + "-01-01";
			if (dateTo !== "") {
				filter.range.date["lte"] = dateTo + "-01-01";
			}
		} else if (dateTo !== "") {
			// TODO, osäker på om man kan söka enbart på slutddatum, annars fixa detta
			filter.range.date["lte"] = dateTo + "-01-01";
			changed = true;
		}
		if (changed === true) {
			let query = finalQuery;
			query.query.bool["filter"] = filter;
			setFinalQuery(query);
		}
	};

	const handleCheckbox = (e) => {
		let current = myndigheter;
		let add = true;
		if (current.length !== 0) {
			for (let i = 0; i < current.length; i++) {
				if (current[i] === e.target.value) {
					add = false;
					current.splice(i,1)
				}
			}
		}
		if (add === true) {
			current.push(e.target.value)
		}
		setMyndigheter(current)
		console.log(myndigheter);
	}


	const searchButtonClicked = (e) => {
		handleMust();
		handleMustNot();
		handleDates();

		let jsonObject = finalQuery;
		console.log(jsonObject);
		
		if (myndigheter.length !== 0) {
			let listToAdd = ""
			for (let i = 0; i < myndigheter.length; i++) {
				listToAdd = listToAdd + myndigheter[i]
				if (i !== myndigheter.length - 1) {
					listToAdd = listToAdd + ","
				}
			}
			let addr = "http://localhost:9200/" + listToAdd + "/_search"
			setReqAddr(addr)
		}

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
							value={phraseToMatch}
							onChange={(e) => setPhraseToMatch(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Utan dessa ord..."
							value={termsNotToMatch}
							onChange={(e) => setTermsNotToMatch(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Inte innehållandes denna fras..."
							value={phraseNotToMatch}
							onChange={(e) => setPhraseNotToMatch(e.target.value)}
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
							<input type="checkbox" value={"riksdagen"} onChange={ handleCheckbox}/> Riksdagen <br />
						<input type="checkbox" value={"arbetsformedlingen"} onChange={ handleCheckbox}/>{" "}
						Arbetsförmedlingen <br />
						<input type="checkbox" value={"bra"} onChange={ handleCheckbox}/> BRÅ <br />
						<input type="checkbox" value={"msb"} onChange={ handleCheckbox}/> MSB <br />
						<input type="checkbox" value={"fhm"} onChange={ handleCheckbox}/> Folkhälsomyndigheten <br />
						<input type="checkbox" value={"forsakringskassan"} onChange={ handleCheckbox}/>
						Försäkringskassan <br />
						<input type="checkbox" value={"esv"} onChange={ handleCheckbox}/> Ekonomistyrningsverket{" "}
						<br />
						<input type="checkbox" value={"polisen"} onChange={ handleCheckbox}/> Polisen <br />
						<input type="checkbox" value={"pts"} onChange={ handleCheckbox} /> Post- och telestyrelsen{" "}
						<br />
						<input type="checkbox" value={"fi"} onChange={ handleCheckbox} /> Finansinspektionen <br />
						<input type="checkbox" value={"riksbanken"} onChange={ handleCheckbox} /> Riksbanken <br />
						<input type="checkbox" value={"foi"} onChange={ handleCheckbox}/> FOI <br />
						<input
							type="checkbox"
							value={"socialstyrelsen"}
						/> Socialstyrelsen <br />
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
