import react from "react";
import React, { useEffect, useState } from "react";
import { useParams } from "react-router";
import "../../../css/search.css";
import { getsosData } from "./logic";

//main search body
function MainBody() {
  const i = useParams();
  const [data, setData] = useState(" ");
  useEffect(() => {
    getsosData(i.token, setData);
    console.log(i.token);
    document.title = "Search";
  }, []);
  return (
    <div className="main-body">
      <div className="map">
        <div className="child">
          <img src={process.env.PUBLIC_URL + "/mpp.jpeg"} alt="map" />
        </div>
      </div>
      <div className="map2">
        <div className="tkn">
          <b>SOS Id:</b> {data==" "?"Loading": data.token}
        </div>
        <div className="tkn">
          <b>Long:</b> {data==" "?"Loading": data.long}
        </div>
        <div className="tkn">
          <b>Lat:</b> {data==" "?"Loading": data.lat}
        </div>

        <div className="tkn">
          <b>time:</b> {data==" "?"Loading": data.time}
        </div>
        <div className="tkn">
          <b>Status:</b> {data==" "?"Loading": "tracking"}
        </div>
      </div>
    </div>
  );
}
// global search box
function Search() {
  
  return (
    <React.Fragment>
      <div className="search">
        <MainBody />
      </div>
    </React.Fragment>
  );
}

export { Search, MainBody };
