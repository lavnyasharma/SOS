import React, { useEffect, useState } from "react";
import "../../../../css/search.css";
import "../../../../css/result.css";
import { useParams, useHistory } from "react-router";
import Backico from "../ico";
import { SearchIco } from "../../../footer/ico";

function SearchBar(props) {
  const history = useHistory();
  const [querry, setQuerry] = useState("");
  useEffect(() => {
    if (props.querry) {
      setQuerry(props.querry);
    }
  }, []);
  // back button
  const backHandel = () => {
    history.goBack();
  };
  // back to search option

  const backtosearch = () => {
    document.getElementById("search-bar").focus();
    history.push("/search");
  };

  return (
    <div className="header">
      <div
        className="small-part"
        onClick={() => {
          backHandel();
        }}
      >
        <Backico />
      </div>
      <div className="big-part">
        <div className="search-wrapper">
          <input
            className="search-input"
            type="search"
            placeholder="Search"
            onFocus={(e) => {
              backtosearch();
            }}
            value={props.id}
          />
        </div>
        <div className="button-wrapper">
          <button
            className="search-button"
            onClick={() => {
              backtosearch();
            }}
          >
            <SearchIco />
          </button>
        </div>
      </div>
      <div className="small-part-2"></div>
    </div>
  );
}
const ResultItem = (props) => {
  const history = useHistory();
  const changePage = () => {
    history.push(`/doc/result/${props.color}`);
  };
  return (
    <div
      className="result-item "
      onClick={() => {
        changePage();
      }}
    >
      <div
        className="result-child"
        style={{ backgroundColor: props.color }}
      ></div>
    </div>
  );
};
const Body = () => {
  return (
    <div className="body">
      <ResultItem color="pink" />
    </div>
  );
};

// footer
function Footer() {
  return <div className="footer"></div>;
}

function SearchResult() {
  const { id } = useParams();
  const [height, setHeight] = useState(window.innerHeight - 58 - 0.6 * 16);
  useEffect(() => {
    window.addEventListener("resize", () => {
      setHeight(window.innerHeight - 58 - 0.6 * 16);
    });
    document.title = id + " - Search Result";
  }, []);
  return (
    <div className="search">
      <SearchBar id={id} />
      <div className="main-result-body" style={{ height: height }}>
        <div className="head small-title-font">
          <span>
            Showing results for: <span className="search-text">{id}</span>
          </span>
        </div>
        <Body />
        <Footer />
      </div>
    </div>
  );
}

export default SearchResult;
