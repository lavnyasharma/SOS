import { React, useContext, useEffect, useState } from "react";
import "../../../css/setting.css";
import { detectmedia, turnDarkOn } from "../../dark";
import "../../../css/LikedItems.css";
import { useHistory } from "react-router-dom";
import { SettingsIco } from "../../footer/ico";
import Backico, { Mobileico, Nfico } from "./ico";
import Dialogue from "../../global/dialogue";
import { logout } from "./logic.js";
import { authContext } from "../../../App";
function HeadBar(props) {
  // back button

  return (
    <div className="header">
      <div className="small-part head-display-svg ">
        <SettingsIco />
      </div>
      <div className="big-part">
        <div className="head-wrapper">
          <div className="head-input">Settings</div>
        </div>
      </div>
      <div className="small-part-2"></div>
    </div>
  );
}

function ToogleButton(props) {
  return (
    <div class="list-item">
      <input
        type="checkbox"
        id={props.id}
        checked={props.isToggleOn ? "checked" : ""}
        onChange={() => {
          if (props.handleClick) props.handleClick();
        }}
        onClick={props.init}
      />
      <label for={props.id}></label>
    </div>
  );
}
function SettingBody() {
  const auth = useContext(authContext);
  const history = useHistory();
  const [dark, setDark] = useState(
    localStorage.getItem("dark") === "true" ? true : false
  );
  const [notification, setNotification] = useState(false);

  const updateDark = () => {
    setDark(!dark);
    localStorage.setItem("dark", !dark);
    turnDarkOn(!dark);
  };
  const updateNotification = () => {
    if (Notification.permission !== "granted") {
      document.getElementById("nf").style.opacity = "1";
      document.getElementById("nf").style.zIndex = "99999";
    } else {
      setNotification(!notification);
    }
  };
  return (
    <div className="body">
      {auth == "1" ? (
        <div
          className="item"
          onClick={() => {
            history.push("/ma");
          }}
        >
          <div className="content">
            <div>My Account</div>
            <div className="small">Manage personal information</div>
          </div>
          <div className="icon">
            <Backico />
          </div>
        </div>
      ) : (
        <div
          class="setting-lr"
          onClick={() => {
            history.push("login");
          }}
        >
          Login or Register
        </div>
      )}

      <div className="item">
        <div
          className="content"
          onClick={() => {
            document.getElementById("ds").style.opacity = "1";
            document.getElementById("ds").style.zIndex = "99999";
          }}
        >
          <div>Dark Mode</div>
          <div className="small">change theme</div>
        </div>
        <div className="icon">
          {localStorage.getItem("darkmodechoice") === "false" ? (
            <ToogleButton
              id="dark"
              isToggleOn={dark}
              handleClick={updateDark}
            />
          ) : (
            <Mobileico />
          )}
        </div>
      </div>
      <div className="item">
        <div className="content">
          <div>Notifications</div>
          <div className="small">Notification access</div>
        </div>
        <div className="icon">
          <ToogleButton
            id="notification"
            isToggleOn={notification}
            handleClick={updateNotification}
          />
        </div>
      </div>
      <div className="item">
        <div className="content">
          <div>Feedback</div>
          <div className="small">Rate us</div>
        </div>
        <div className="icon">
          <Backico />
        </div>
      </div>
      <div className="item">
        <div className="content">
          <div>Support</div>
          <div className="small">Contact us</div>
        </div>
        <div className="icon">
          <Backico />
        </div>
      </div>
      {auth == "1" ? (
        <div
          className="item"
          onClick={() => {
            logout(history);
          }}
        >
          <div className="content">Logout</div>
          <div className="icon">
            <Backico />
          </div>
        </div>
      ) : (
        ""
      )}
    </div>
  );
}
const DarkModeChoice = (props) => {
  return (
    <div className="dark-mode-choice">
      <div className="dark-mode-choice-item">
        <div className="dic di">
          <Mobileico />
        </div>
        <div className="dic dt">Use device theme</div>
        <div className="dic dbu">
          <ToogleButton {...props} />
        </div>
      </div>
    </div>
  );
};
const NotificationDeniedMessage = (props) => {
  return (
    <div className="dark-mode-choice">
      <div className="dark-mode-choice-item">
        <div className="dic di">
          <Nfico />
        </div>
        <div className="dic dt">Notifications are not allowed</div>
        <div className="dic dbu">
          {"Settings > Site Settings > Thesteth > Allow Notifications"}
        </div>
      </div>
    </div>
  );
};

function Setting() {
  const [choice, setChoice] = useState(
    localStorage.getItem("darkmodechoice") === "true" ? true : false
  );
  useEffect(() => {
    detectmedia();
    document.title = "Settings";
  }, [choice]);
  const updatechoice = () => {
    setChoice(!choice);
    localStorage.setItem("darkmodechoice", !choice);
    detectmedia();
  };
  return (
    <div className="Setting-Main">
      <HeadBar />

      <SettingBody />
      <Dialogue
        parentid="ds"
        title="Dark Mode"
        body={DarkModeChoice}
        id="device"
        isToggleOn={choice}
        handleClick={updatechoice}
        close={true}
      />

      <Dialogue
        parentid="nf"
        title="Notifications"
        body={NotificationDeniedMessage}
        close={true}
      />
    </div>
  );
}
export default Setting;
