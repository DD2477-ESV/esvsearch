import React, { useState } from "react";
import { Document, Page } from "react-pdf/dist/esm/entry.webpack";

export default function ViewDocument(props) {
        const [numPages, setNumPages] = useState(null);

        function onDocumentLoadSuccess({ numPages }) {
                setNumPages(numPages);
        }

        return (
                <Document file={props.docURL} onLoadSuccess={onDocumentLoadSuccess}>
                        {Array.from(new Array(numPages), (el, index) => (
                                <Page key={`page_${index + 1}`} pageNumber={index + 1} />
                        ))}
                </Document>
        );
}

/* // DIsplay one page
export default function ViewDocument(props) {
        const [numPages, setNumPages] = useState(null);
        const [pageNumber, setPageNumber] = useState(1);

        function onDocumentLoadSuccess({ numPages }) {
                setNumPages(numPages);
                setPageNumber(1);
        }

    function changePage(offset) {
                setPageNumber((prevPageNumber) => prevPageNumber + offset);
        }

    function previousPage(e) {
        e.preventDefault();
                changePage(-1);
        }

    function nextPage(e) {
        e.preventDefault();
                changePage(1);
        }

        return (
                <>
                        <Document file={props.docURL} onLoadSuccess={onDocumentLoadSuccess}>
                                <Page pageNumber={pageNumber} />
                        </Document>
                        <div>
                                <p>
                                        Page {pageNumber || (numPages ? 1 : "--")} of {numPages || "--"}
                                </p>
                                <button type="button" disabled={pageNumber <= 1} onClick={previousPage}>
                                        Previous
                                </button>
                                <button
                                        type="button"
                                        disabled={pageNumber >= numPages}
                                        onClick={nextPage}
                                >
                                        Next
                                </button>
                        </div>
                </>
        );
}
 */