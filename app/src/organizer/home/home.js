import React, { useEffect, useState } from "react";
import "../../css/home.css";

import MainScrHome from "./Mainscreen/Msrc";

import { Switch,Route } from "react-router-dom";

export default function Home() {
  return (
    <React.Fragment>
      <Switch>
        <Route path="/" exact component={MainScrHome} />
        
      </Switch>
    </React.Fragment>
  );
}
