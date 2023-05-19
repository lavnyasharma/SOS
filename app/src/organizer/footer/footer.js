import React, { useEffect, useState } from "react";

import "../../css/footer.css";
import { useHistory } from "react-router-dom";
import {
  HomeIco,
  SearchIco,
  Add,
  HeartIcon,
  SettingsIco,
  Ambu,
  
} from "./ico";
import { useContext } from "react";
import { authContext } from "../../App";

export default function Footer() {
  const auth = useContext(authContext);
  const history = useHistory();
  const route = history.location.pathname;
  const changeRoute = (route) => {
    setIsOpen(route.replace("/", ""));
    history.push(route);
  };
  const [isOpen, setIsOpen] = useState(route.replace("/", ""));
  useEffect(() => {
    history.listen((location) => {
      if (history.action === "POP" || history.action === "PUSH") {
        setIsOpen(location.pathname.replace("/", ""));
      }
    });
  }, [isOpen]);
  return (
    <div className="Main_footer ">
      <div
        className={isOpen === "" ? "active" : ""}
        onClick={() => {
          changeRoute("");
        }}
      >
        <HomeIco />
      </div>

      <div
          className="vslbtn"
          onClick={() => {
            history.push("/visuals");
          }}
          
        >
       
         
        
        <div className="Icon_container2">
        <Add/>
        </div>
      </div>
      
      {auth == '1' && localStorage.getItem('usertype') == 'h' ?  <div
        className={isOpen === "freeway" ? "active" : ""}
        onClick={() => {
          changeRoute("lst");
        }}
      >
        <div className="Icon_container2">
          <Ambu />
        </div>
      </div> : " "} 

      <div
        className={isOpen === "setting" ? "active" : ""}
        onClick={() => {
          changeRoute("setting");
        }}
      >
        <SettingsIco />
      </div>
    </div>
  );
}
