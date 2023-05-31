import "./App.css";
import Topnav from "./organizer/topnav/topnav";
import Home from "./organizer/home/home";
import Footer from "./organizer/footer/footer";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Setting from "./organizer/home/setting/setting";
import MyaAccount from "./organizer/myaccount/myaccount";
import { createContext, useContext, useEffect } from "react";
import { detectmedia } from "./organizer/dark";
import IntitalizeFireBaseMessaging from "./organizer/firebase";
import Demo from "./organizer/imageuploader/image";
import LoginAndRegister from "./organizer/Lr/login";
import Popup, { SPopup } from "./organizer/global/errbox";
import Frwy from "./organizer/home/Mainscreen/Freeway";
import { Search } from "./organizer/home/search/search";
import React from "react";
import { Lst } from "./organizer/home/search/soslst";

// context
export const authContext = createContext(
  localStorage.getItem("access_token") ? 1 : 0
);
function App() {
  function messf() {
    const messaging = window.firebase.messaging();
    messaging.onMessage(function (payload) {
      console.log(payload);
      const notificationOption = {
        body: payload.notification.body,
        icon: payload.notification.icon,
      };

      if (Notification.permission === "granted") {
        var notification = new Notification(
          payload.notification.title,
          notificationOption
        );
        console.log("hoho");
        notification.onclick = function (ev) {
          ev.preventDefault();
          window.open(payload.notification.click_action, "_blank");
          notification.close();
        };
      }
    });
    messaging.onTokenRefresh(function () {
      messaging
        .getToken()
        .then(function (newtoken) {
          console.log("New Token : " + newtoken);
        })
        .catch(function (reason) {
          console.log(reason);
        });
    });
  }
  useEffect(() => {
    try {
      if (window.firebase.messaging.isSupported()) {
        IntitalizeFireBaseMessaging();

        messf();
      }
    } catch {}
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition((position) => {
        console.log(position);
      });
    } else {
      console.log("Not Available");
    }
    detectmedia();
    document.title = "Evas";
  }, []);
  return (
    <authContext.Provider value={localStorage.getItem("access_token") ? 1 : 0}>
      <div className="mainapp ">
        <Topnav />
        <Switch>
          <Route exact path="/" component={Home} />
          <Route path="/visuals" component={Demo} />
          <Route path="/freeway" component={Frwy} />
          <Route path="/sos/:token/" component={Search} />
          <Route path="/lst" component={Lst} />
          <Route path="/setting" component={Setting} />
          <Route path="/ma" component={MyaAccount} />
          <Route path="/" component={LoginAndRegister} />
        </Switch>
        <Footer />
        <Popup />
        <SPopup />
      </div>
    </authContext.Provider>
  );
}

export default App;
