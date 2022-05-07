import logo from "./logo.svg";
import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import Header from "./components/Header";
import HomePage from "./components/HomePage";
import ResultPage from "./components/ResultPage";

function App() {
	return (
		<Router>
			<div className="App">
				<Header />
				<Routes>
					<Route path="/" element={<HomePage />} exact={true} />
					{/* <Route
						path="/search/new"
						element ={<ResultPage />} /> */}
				</Routes>
			</div>
		</Router>
	);
}

export default App;
