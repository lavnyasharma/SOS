import React, { useEffect, useState, useCallback } from "react";
import "../../../css/mainsrc.css";
import { useHistory } from "react-router-dom";
import { guestfreewaysos, guestsos, updatecoordsos } from "./logic";
import NoSleep from "nosleep.js";
import { te } from "../../global/errbox";


import { useContext } from "react";
import { authContext } from "../../../App";
function openFullscreen(elem) {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) {
    /* Safari
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) {
    /* IE11 */
    elem.msRequestFullscreen();
  }
}
function Flscrn() {
  const [w, setW] = useState();
  var noSleep = new NoSleep();
  const [h, setH] = useState();

  useEffect(() => {
    
    setH(window.innerHeight);
    setW(window.innerWidth);
  }, []);

  function abortsos() {
    console.log("abort");
    let elm = document.getElementById("flscrn");
    elm.style.display = "none";
    localStorage.removeItem("guest_token");
    localStorage.removeItem("guest_sos");
  }
  return (
    <div style={{ height: h, width: w }} className="flscrn" id="flscrn">
      <div
        className="txt bgg"
        onClick={() => {
          document.addEventListener(
            "fullscreenchange",
            function enableNoSleep() {
              document.removeEventListener(
                "fullscreenchange",
                enableNoSleep,
                false
              );
              noSleep.enable();
            },
            false
          );
        }}
      >
        sos mode
      </div>
      <div className="txt smll"> do not exit</div>
      <div
        className="stpbtn"
        onClick={() => {
          abortsos();
        }}
      >
        Abort
      </div>
    </div>
  );
}

function MainScrHome() {
  const [lat, setLat] = useState(null);
  const [long, setLong] = useState(null);
  let id;
  function useLongPress(callback = () => {}, ms = 300) {
    const [startLongPress, setStartLongPress] = useState(false);

    useEffect(() => {
      let timerId;
      if (startLongPress) {
        timerId = setTimeout(callback, ms);
      } else {
        clearTimeout(timerId);
      }

      return () => {
        clearTimeout(timerId);
      };
    }, [startLongPress]);

    const start = useCallback(() => {
      setStartLongPress(true);
    }, []);
    const stop = useCallback(() => {
      setStartLongPress(false);
    }, []);

    return [
      startLongPress,
      {
        onMouseDown: start,
        onMouseUp: stop,
        onMouseLeave: stop,
        onTouchStart: start,
        onTouchEnd: stop,
      },
    ];
  }
  function success(pos) {
    var noSleep = new NoSleep();
    var crd = pos.coords;
    setLat(crd.latitude);
    setLong(crd.longitude);
    let phone = localStorage.getItem("guest_phone");
    navigator.geolocation.clearWatch(id);
    guestfreewaysos(phone, crd.latitude, crd.longitude);
    navigator.geolocation.clearWatch(id);
  }
  function er(err) {
    console.warn("ERROR(" + err.code + "): " + err.message);
  }
  function afterpress() {
    if (localStorage.getItem("guest_phone")) {
      id = navigator.geolocation.watchPosition(success, er);
    } else {
      let elm = document.getElementById("gpno");
      elm.style.borderBottom = "2px Solid red";
      elm.style.background = "rgba(250, 121, 121, 0.089)";
      te("Enter phone number");
    }
  }
  const [startLongPress, backspaceLongPress] = useLongPress(() => {
    // define sos press
    afterpress();
  }, 3000);
  let className = "";
  let h = "";
  if (startLongPress) {
    className += " start";
    h = "txt-crcl";
  } else {
    className += "";
    h = "";
  }
  const history = useHistory();
  return (
    <div className="mnsrc">
      <div className="circle-cntnr">
        <button
          className={"circle " + className}
          {...(localStorage.getItem("guest_sos") === "true"
            ? (onclick = () => {
                let elm = document.getElementById("flscrn");
                elm.style.display = "flex";
              })
            : backspaceLongPress)}
        >
          <h1 className={h}>{"Freeway"}</h1>
          <h5 className={h}>{"press for 3 seconds"}</h5>
        </button>
      </div>
      <div className="msg">
        <div className="kpclm">Request a freeway</div>
        <div className="bdy">
          After pressing the Freeway button everyone will be notified of your
          emergency.
        </div>
      </div>
    </div>
  );
}

function Frwy() {
  
  const auth = useContext(authContext);
  const history = useHistory();

  const [width, setWidth] = useState(window.innerWidth);
  const [height, setHeight] = useState(window.innerHeight);
  useEffect(() => {
    if(auth != "1")
    {
      history.push("login");
    }
    function handleResize() {
      setWidth(window.innerWidth);
      setHeight(window.innerHeight);
    }
    document.title = "Evas";
    window.addEventListener("resize", handleResize);
  }, []);
  return (
    <div className="Main_home" style={{ width: width, height: height }}>
      <MainScrHome />
    </div>
  );
}

export default Frwy;
