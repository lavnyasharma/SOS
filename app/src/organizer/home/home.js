import React, { useEffect, useState } from "react";
import "../../css/home.css";
import Msrc from "./Mainscreen/Msrc";
import MainScrHome from "./Mainscreen/Msrc";

import { Switch,Route } from "react-router-dom";
import Footer from "../footer/footer";
import LikedItem from "./LikedItems/LikedItem";
export default function Home() {
  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={MainScrHome} />
        
      </Switch>
    </React.Fragment>
  );
}
