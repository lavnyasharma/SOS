import React from "react";
import "../../css/dialogue.css";

function CloseIco() {
  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="var(--FontMajor)"
      strokeWidth="1"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  );
}

function Dialogue(props) {
  const Body = props.body ? props.body : "div";
  return (
    <div className="dialogue-body" id={props.parentid}>
      <div className="dialogue-box">
        <div className="hf">
          <div className="hf-title">{props.title}</div>
          {props.close ? (
            <div
              className="close"
              onClick={() => {
                document.getElementById(props.parentid).style.opacity = "0";
                document.getElementById(props.parentid).style.zIndex = "-2000";
              }}
            >
              <CloseIco />
            </div>
          ) : (
            ""
          )}
        </div>
        <div className="db">
          <Body {...props} />
        </div>
        <div className="hf"></div>
      </div>
    </div>
  );
}

export default Dialogue;
