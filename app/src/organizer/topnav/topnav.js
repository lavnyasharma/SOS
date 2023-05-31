import React, { useContext, useEffect, useState } from "react";
import { useHistory } from "react-router-dom";
import { authContext } from "../../App";
import "../../css/topnav.css";
import { te } from "../global/errbox";


function Topnav() {
  const history = useHistory();
  const auth = useContext(authContext);
  const [name, setName] = useState("archit");
  const [gender, setGender] = useState("male");
  const [phone, setPhone] = useState(
    localStorage.getItem("guest_phone")
      ? localStorage.getItem("guest_phone")
      : ""
  );
  const open = () => {
    history.push("/ma");
  };
  useEffect(() => {}, [phone]);
  // hair
  const avatar =
    "https://avatars.dicebear.com/api/" +
    gender +
    "/" +
    name +
    ".svg?mood[]=happy&hair[]=cap";
  return (
    <div className="TopNav">
      <div className="M_m d_T"></div>

      <div className="N_T">
        {auth == "1" ? (
          "Hi, User"
        ) : (
          <>
            <input
              id="gpno"
              type="number"
              value={phone}
              className="headinput"
              placeholder="Phone number"
              onChange={(e) => {
                if (phone.length <= 10) {
                  setPhone(e.target.value);
                } else {
                  setPhone(e.target.value);

                  te("Phone number should be 10 digits");
                }
              }}
            />
            <div
              className="svbtm"
              onClick={() => {
                if (phone.length == 10) {
                  localStorage.setItem("guest_phone", phone);
                }
              }}
            >
              save
            </div>
          </>
        )}
      </div>
      <div
        onClick={() => {
          history.push("/ma");
        }}
        className="M_m"
        style={
          auth == "1"
            ? { backgroundImage: "url(" + avatar + ")" }
            : {
                border: "none",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }
        }
      >
        {auth == "1" ? "" : "Login"}
      </div>
    </div>
  );
}
export default Topnav;
