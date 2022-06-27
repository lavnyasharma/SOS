import { React, useEffect, useState } from "react";
import "../../css/doctor.css";
import { HeadBar } from "../home/LikedItems/LikedItem";
import Backico from "../home/search/ico.js";
import { useHistory, useParams } from "react-router-dom";
import { book, getbatches, getinfo, gettimings } from "./logic";
import { DateData } from "../data";
import Loder from "./ico";
function CreateRipple(e) {
  const parent = e.target.parentElement;
  const grandparent = e.target.parentElement.parentElement;
  let scrollPercentage =
    grandparent.scrollLeft /
    (grandparent.scrollWidth - grandparent.clientWidth);
  console.log(grandparent.scrollWidth);

  const ripple = document.createElement("div");
  ripple.className = "ripple";
  ripple.style.left =
    e.pageX - parent.offsetLeft + grandparent.scrollLeft + "px";
  ripple.style.top =
    e.pageY - parent.offsetTop + document.body.scrollTop + "px";
  parent.appendChild(ripple);
  setTimeout(() => {
    parent.removeChild(ripple);
  }, 1000);
}

function DocInfoHead(props) {
  const [holder, setHolder] = useState(10);
  useEffect(() => {
    let h = document.getElementById("holderbox").offsetWidth;
    setHolder(h - 0.12 * h);
  }, []);
  console.log(props.pinfo);
  return (
    <div className="head" style={{ height: `${holder}px` }}>
      <div className="head-left" id="holderbox">
        <div
          className="holder"
          style={{
            height: `${holder}px`,
            width: `${holder}px`,
            backgroundColor: `#${props.color}`,
          }}
        ></div>
      </div>
      <div className="head-right">
        <span className="dr-name">
          Dr.&nbsp;{props.pinfo ? props.pinfo["first_name"] : ""}&nbsp;
          {props.pinfo ? props.pinfo["last_name"] : ""}
        </span>
        <div className="dr-speciality">Dermatoligy ,Virology & Leprosy</div>
        <div className="dr-location">jammu</div>
      </div>
    </div>
  );
}

function Biography(props) {
  const readmore = () => {
    const rmbdy = document.getElementById("rm-bdy");
    const rm = document.getElementById("rm");
    if (rm.innerHTML == "Read more") {
      rm.innerHTML = "Show less";
      rmbdy.style.overflow = "visible";
      rmbdy.style.whiteSpace = "pre-wrap";
    } else {
      rm.innerHTML = "Read more";
      rmbdy.style.overflow = "hidden";
      rmbdy.style.whiteSpace = "nowrap";
    }
  };
  return (
    <div className="biography">
      <div className="head small-title-font">BIOGRAPHY</div>
      <div
        className="body"
        id="rm-bdy"
        onClick={() => {
          readmore();
        }}
      >
        {props.statement ? props.statement["professional_statement"] : ""}
      </div>
      <div
        className="rm"
        id="rm"
        onClick={() => {
          readmore();
        }}
      >
        Read more
      </div>
    </div>
  );
}

function SearchBoxItem(props) {
  const history = useHistory();
  function SearchTo(e) {
    history.push("/search/" + props.name);
  }
  return (
    <div
      className="sugges-item"
      onClick={() => {
        SearchTo();
      }}
    >
      {props.name}
    </div>
  );
}

function SuggesBox() {
  const data = {
    1: "Doctor",
    2: "Fever",
    3: "Covid",
    4: "Immunologist",
    5: "Family Physician",
    6: "Cardiologist",
    7: "Pediatrician",
  };
  return (
    <div className="sugges-box">
      <div className="head small-title-font">SPECIALITIES</div>
      <div className="body">
        {Object.keys(data).map((key) => {
          return <SearchBoxItem name={data[key]} key={key} />;
        })}
      </div>
    </div>
  );
}
// date item
function DateItem(props) {
  const [aState, setAState] = useState("natural");
  useEffect(() => {
    if (!props.ava) {
      setAState(aState + " disable");
    } else if (props.activeDate) {
      setAState("natural active");
    } else {
      setAState("natural");
    }
  }, [props.UpdateActiveDate]);
  return (
    <div
      style={{ overflow: "hidden" }}
      className={"date-item " + aState}
      data-batchid={props.batchid}
      onClick={(e) => {
        CreateRipple(e);
        if (props.ava) {
          props.UpdateActiveDate(props.batchid);
        }
      }}
    >
      <div className="item number">{props.date}</div>
      <div className="item day">{props.day}</div>
    </div>
  );
}
// date
function Date(props) {
  const data = props.d;
  return (
    <div className="date">
      <div className="title small-title-font">Days</div>
      <div className="body">
        {Object.keys(data).map((key) => {
          return (
            <DateItem
              key={data[key]["BATCHID"]}
              batchid={data[key]["BATCHID"]}
              date={data[key]["date"].split("-")[2]}
              day={data[key]["name"].slice(0, 3)}
              ava={data[key]["active"]}
              activeDate={
                data[key]["BATCHID"] == props.activeDate ? true : false
              }
              UpdateActiveDate={props.UpdateActiveDate}
            />
          );
        })}
      </div>
    </div>
  );
}
// time item
const TimeItem = (props) => {
  const [aState, setAState] = useState("natural");
  useEffect(() => {
    if (!props.ava) {
      setAState("natural disable");
    } else if (props.activeTime) {
      setAState("natural active");
    } else {
      setAState("natural");
    }
  }, [props.UpdateActiveTime]);
  return (
    <div
      onClick={(e) => {
        CreateRipple(e);
        if (props.ava) {
          props.UpdateActiveTime(props.data);
          console.log(props.data);
        }
      }}
      className={"time-item " + aState}
    >
      <div className="t-item">{props.time}</div>
    </div>
  );
};
//time
function Time(props) {
  return (
    <div className="time">
      <div className="title small-title-font">Time</div>
      <div className="body">
        {Object.keys(props.data).map((key) => {
          return (
            <TimeItem
              key={key}
              data={key}
              time={props.data[key]["time"]}
              ava={props.data[key]["ava"]}
              activeTime={key == props.activeTime ? true : false}
              UpdateActiveTime={props.UpdateActiveTime}
            />
          );
        })}
      </div>
    </div>
  );
}
// schedule
function Schedule(props) {
  const { DOCID } = useParams();
  const [activeDate, setActiveDate] = useState(null);
  const [activeTime, setActiveTime] = useState(0);
  const [data, setData] = useState(null);
  const [timings, setTimings] = useState(null);
  const datedata = DateData;
  useEffect(() => {
    if (data === null) {
      getbatches(props.ofid, setData);
    }
  }, [activeDate, activeTime]);
  const UpdateActiveDate = (date) => {
    setActiveDate(date);
    gettimings(date, setTimings);
    setActiveTime(0);
  };
  const BookNowTo = () => {
    if (activeDate && activeTime) {
      book(DOCID, activeDate, activeTime);
    }
  };
  const UpdateActiveTime = (time) => {
    setActiveTime(time);
  };
  return (
    <>
      <div className="Schedule">
        <div className="head">SCHEDULE</div>
        {data !== null ? (
          <Date
            data={datedata}
            d={data}
            UpdateActiveDate={UpdateActiveDate}
            activeDate={activeDate}
          />
        ) : (
          <Loder />
        )}
        {timings !== null ? (
          <Time
            data={timings}
            activeTime={activeTime}
            UpdateActiveTime={UpdateActiveTime}
          />
        ) : (
          <div
            style={{
              width: "100%",
              color: "white",
              textAlign: "center",
              marginTop: "20px",
              fontSize: "15px",
            }}
          >
            Select A Date
          </div>
        )}
      </div>
      <BookNow BookNowTo={BookNowTo} />
    </>
  );
}

//book now button
function BookNow(props) {
  const history = useHistory();
  function BookNowTo(e) {
    history.push("/book");
  }
  return (
    <div
      className="book-now"
      onClick={() => {
        props.BookNowTo();
      }}
    >
      Book Now
    </div>
  );
}

// main body
function Doctor() {
  const { DOCID } = useParams();
  const [info, setInfo] = useState(null);

  useEffect(() => {
    if (info === null) {
      getinfo(DOCID, setInfo);
    }

    document.title = DOCID + " - Doctor";
  }, []);

  return (
    <div className="main-doc-body">
      <HeadBar name="Doctor" icon={Backico} back={true} />
      <DocInfoHead pinfo={info !== null ? info["user"] : ""} color={DOCID} />
      <Biography statement={info !== null ? info["doctor"] : ""}></Biography>
      <SuggesBox></SuggesBox>
      {info !== null ? (
        <Schedule ofid={info !== null ? info["ofid"] : ""} />
      ) : (
        <Loder />
      )}

      <div className="footer"></div>
    </div>
  );
}

export default Doctor;
