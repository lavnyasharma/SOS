import React, { useEffect, useState, useCallback, useContext } from "react";
import "../../../css/mainsrc.css";
import { useHistory } from "react-router-dom";
import { guestsos, loggedsos, updatecoordsos } from "./logic";
import NoSleep from "nosleep.js";
import { te } from "../../global/errbox";
import { authContext } from "../../../App";


function openFullscreen(elem) {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) {
    /* Safari */
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
          let elm = document.getElementById("flscrn");
          elm.style.display = "flex";
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
          openFullscreen(elm);
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
      <div className="txt smll flsh" id="ambutx">
        {" "}
      </div>
    </div>
  );
}

function MainScrHome() {
  const auth = useContext(authContext);
  const [lat, setLat] = useState(null);
  const [long, setLong] = useState(null);
  function useLongPress(callback = () => {}, ms = 300) {
    const [startLongPress, setStartLongPress] = useState(false);

    useEffect(() => {
      if (
        localStorage.getItem("guest_sos") === "true" &&
        localStorage.getItem("guest_phone")
      ) {
        let id = navigator.geolocation.watchPosition(success, er);
      }
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
    console.log("test");

    if (localStorage.getItem("guest_token")) {
      console.log("test");
      updatecoordsos(
        localStorage.getItem("guest_token"),
        crd.latitude,
        crd.longitude
      );
      let elm = document.getElementById("flscrn");
      elm.style.display = "flex";
    
    }
    else if (auth == "1"){
      loggedsos(crd.latitude, crd.longitude);
      let elm = document.getElementById("flscrn");
      elm.style.display = "flex";
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
      openFullscreen(elm);
    }
    else {
      guestsos(phone, crd.latitude, crd.longitude);
      let elm = document.getElementById("flscrn");
      elm.style.display = "flex";
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
      openFullscreen(elm);
    }

    console.log("Your current position is:", crd.latitude, crd.longitude);
  }
  function er(err) {
    console.warn("ERROR(" + err.code + "): " + err.message);
  }
  function afterpress() {
    if (localStorage.getItem("guest_phone")) {
      setTimeout(() => {
        document.getElementById("ambutx").innerHTML =
          "Help is on the way  <br> Dont Worry..!!! <br> For more detail please upload a pic of the incident";
      }, 10000);
      let id = navigator.geolocation.watchPosition(success, er);
    } else if (auth == "1") {
      setTimeout(() => {
        document.getElementById("ambutx").innerHTML =
          "Help is on the way  <br> Dont Worry..!!! <br> For more detail please upload a pic of the incident";
      }, 10000);
      let id = navigator.geolocation.watchPosition(success, er);
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
  }, 2000);
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
    
      <div className="kpclms">
        Found an Injured animal Just click the button
      </div>
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
          <h1 className={h}>
            {localStorage.getItem("guest_sos") === "true" ? "Active" : "Help"}
          </h1>
          <h5 className={h}>
            {localStorage.getItem("guest_sos") === "true"
              ? "click to enable sos mode"
              : "press for 2 seconds"}
          </h5>
        </button>
      </div>
      <div className="msg">
        <div className="kpclm">Dont Worry!!</div>
        <div className="bdy">
          Your location will be shared with the nearest help centre.
        </div>
      </div>
    </div>
  );
}

function Msrc() {
  const [width, setWidth] = useState(window.innerWidth);
  const [height, setHeight] = useState(window.innerHeight);
  useEffect(() => {
    function handleResize() {
      setWidth(window.innerWidth);
      setHeight(window.innerHeight);
    }
    document.title = "Thesteth";
    window.addEventListener("resize", handleResize);
  }, []);
  return (
    <div className="Main_home" style={{ width: width, height: height }}>
      <MainScrHome />
      <Flscrn />
    </div>
  );
}

export default Msrc;
