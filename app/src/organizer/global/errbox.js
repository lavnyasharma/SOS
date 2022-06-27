import { useEffect } from "react";
import "../../css/popup.css";

function te(msg = "error") {
  console.log(msg);
  document.getElementById("error-popup").style.top = "80%";
  document.getElementById("error-text").innerHTML = msg;
  setTimeout(() => {
    document.getElementById("error-popup").style.top = "200%";
  }, 4000);
}

function ts(msg = "sucess") {
  console.log(msg);
  document.getElementById("sucess-popup").style.top = "80%";
  document.getElementById("sucess-text").innerHTML = msg;
  setTimeout(() => {
    document.getElementById("sucess-popup").style.top = "200%";
  }, 6000);
}
function SPopup(props) {
  return (
    <div
      className="popup-body"
      id="sucess-popup"
      style={{ transition: "0.3s" }}
    >
      <div className="popup-box sucss" id="sucess-text"></div>
    </div>
  );
}

function Popup(props) {
  return (
    <div className="popup-body" id="error-popup" style={{ transition: "0.3s" }}>
      <div className="popup-box err" id="error-text"></div>
    </div>
  );
}
export default Popup;
export { te, ts, SPopup };
