import React, { useContext, useEffect, useState } from "react";
import "../../css/lr.css";
import { HeadBar } from "../home/LikedItems/LikedItem";
import Backico from "../home/search/ico";
import { FullInput } from "../myaccount/myaccount";
import { PasswordValidation, PhoneValidation } from "../myaccount/validation";
import { Switch, useHistory, Route, Redirect } from "react-router-dom";
import Dialogue from "../global/dialogue";
import { handleLoginSubmit, handleRegisterSubmit } from "./logic";
import VerifyOtp, { ResetPassword, SetPassword } from "./d";
import { authContext } from "../../App";
import { te } from "../global/errbox";
// open dil close dil
const opendil = (id) => {
  document.getElementById(id).style.opacity = "1";
  document.getElementById(id).style.zIndex = "99999";
};
const closedil = (id) => {
  document.getElementById(id).style.opacity = "0";
  document.getElementById(id).style.zIndex = "-99999";
};
function dgi(id) {
  return document.getElementById(id);
}
// register
function Register(props) {
  const history = useHistory();
  const [valid, setValid] = useState(["Rphone"]);
  const [phone, setPhone] = useState("");
  const ifInvalid = (id) => {
    dgi(id).style.border = "2px solid var(--error)";
    dgi(`label${id}`).style.color = "var(--error)";
    setTimeout(() => {
      dgi(id).style.border = "";
      dgi(`label${id}`).style.color = "";
    }, 3000);
  };
  function validation(e) {
    if (valid.length === 0) {
      console.log(phone);
      const resp = handleRegisterSubmit(phone);
      console.log(Promise.resolve(resp));
    } else {
      for (let i = 0; i < valid.length; i++) {
        ifInvalid(valid[i]);
      }
      te("Following fields are required");
      return false;
    }
  }
  const checkValidation = (value, id, validationfunc) => {
    if (validationfunc) {
      let outcome = validationfunc(value);
      if (!outcome) {
        setValid(() => {
          let list = Array.from(valid);
          list.push(id);
          return list;
        });
        ifInvalid(id);
      } else {
        dgi(id).style.border = "";
        dgi(`label${id}`).style.color = "";
        setValid(valid.filter((item) => item !== id));
      }
    }
  };
  return (
    <React.Fragment>
      <div className="login">
        <div className="lr-head">
          <h2>Register</h2>
        </div>

        <FullInput
          placeholder="Phone No."
          id="Rphone"
          labelname="Phone No."
          tabIndex="0"
          type="number"
          maxlength={10}
          validation={PhoneValidation}
          value={phone}
          updatestate={setPhone}
          validdata={checkValidation}
        />

        <div className="container center-box">
          <button
            onClick={(e) => {
              validation(e);
            }}
          >
            verify
          </button>
        </div>

        <div
          className="lr-switch"
          onClick={() => {
            history.push("/login");
          }}
        >
          {" Login"}
        </div>
      </div>
      <Dialogue
        parentid="spass"
        title="Set Password"
        body={SetPassword}
        close={false}
        history={history}
      />
    </React.Fragment>
  );
}
// login
function Login() {
  const history = useHistory();
  const [valid, setValid] = useState(["Lphone", "Lpassword"]);
  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const ifInvalid = (id) => {
    dgi(id).style.border = "2px solid var(--error)";
    dgi(`label${id}`).style.color = "var(--error)";
    setTimeout(() => {
      dgi(id).style.border = "";
      dgi(`label${id}`).style.color = "";
    }, 3000);
  };
  const validation = (e) => {
    e.preventDefault();
    console.log(valid);
    if (valid.length === 0) {
      handleLoginSubmit(phone, password, history);
      return true;
    } else {
      for (let i = 0; i < valid.length; i++) {
        ifInvalid(valid[i]);
      }
      te("Following fields are required")
      return false;
    }
  };
  const checkValidation = (value, id, validationfunc) => {
    if (validationfunc) {
      let outcome = validationfunc(value);
      if (!outcome) {
        setValid(() => {
          let list = Array.from(valid);
          list.push(id);
          return list;
        });
        console.log(valid);
        ifInvalid(id);
      } else {
        dgi(id).style.border = "";
        dgi(`label${id}`).style.color = "";
        setValid(valid.filter((item) => item !== id));
      }
    }
  };
  return (
    <div className="login">
      <div className="lr-head">
        <h2>Login</h2>
      </div>
      {/* <div className="lr-input">
          <input type="text" id="login" placeholder="Phone Number" />
          <label htmlFor="login"></label>
      </div> */}
      <FullInput
        placeholder="Phone No."
        id="Lphone"
        labelname="Phone No."
        tabIndex="0"
        type="number"
        maxlength={10}
        validation={PhoneValidation}
        value={phone}
        updatestate={setPhone}
        validdata={checkValidation}
      />
      <FullInput
        placeholder="Password."
        id="Lpassword"
        labelname="Password"
        tabIndex="1"
        type="password"
        value={password}
        updatestate={setPassword}
        validation={PasswordValidation}
        validdata={checkValidation}
      />
      <div className="container center-box">
        <button
          onClick={(e) => {
            validation(e);
          }}
        >
          login
        </button>
      </div>
      <div className="lr-forgot small-title-font">
        <span
          onClick={() => {
            opendil("rpass");
          }}
        >
          {"Forgot Password"}
        </span>
      </div>
      <div
        className="lr-switch"
        onClick={() => {
          history.push("/register");
        }}
      >
        {" Register"}
      </div>
    </div>
  );
}

const Lrbdy = () => {
  return (
    <div className="lr-body">
      <HeadBar name="Login or Register" icon={Backico} back={true} />
      <Switch>
        <Route path="/login/" component={Login} />
        <Route path="/register/" component={Register} registerphone="" />
      </Switch>
      <Dialogue
        parentid="otp"
        title="Verify Otp"
        body={VerifyOtp}
        close={false}
      />
      <Dialogue
        parentid="rpass"
        title="Reset Password"
        body={ResetPassword}
        close={true}
      />
    </div>
  );
};
export default function LoginAndRegister() {
  const auth = useContext(authContext);
  useEffect(() => {
    document.title = "Login and Register";
  });
  return (
    <React.Fragment>
      {auth == "1" ? <Redirect to="/" /> : <Lrbdy />}
    </React.Fragment>
  );
}

export { opendil, closedil, Login };
