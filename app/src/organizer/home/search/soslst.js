import react from "react";
import React, { useEffect, useState } from "react";
import { useHistory, useParams } from "react-router";
import "../../../css/search.css";
import { getsosallData, getsosData } from "./logic";

//main search body
function MainBody() {
  const history = useHistory();
  const [data, setData] = useState(" ");
  useEffect(() => {
    getsosallData(setData);
  }, []);
  return (
    <div className="main-body">
      <div className="lst">
        {data == " "
          ? "Loading"
          : data.map((item) => {
              return (
                <div className="lstitm" onClick={() => {
                  history.push("/sos/" + item.token);
                }}>
                  <div>
                    <b>Long:</b> {data == " " ? "Loading" : item.long}
                  </div>
                  <div>
                    <b>Lat:</b> {data == " " ? "Loading" : item.lat}
                  </div>
                  <div>
                    <b>Timing:</b> {data == " " ? "Loading" : item.time}
                  </div>
                </div>
              );
            })}
      </div>
    </div>
  );
}
// global search box
function Lst() {
  return (
    <React.Fragment>
      <div className="search">
        <MainBody />
      </div>
    </React.Fragment>
  );
}

export { Lst, MainBody };
