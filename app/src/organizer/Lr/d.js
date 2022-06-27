import React, { useEffect, useState } from "react";
import { KeyIco, NextIco } from "./ico";
import {
  handleOtpSubmit,
  handleRegisterSubmit,
  handleResetPassword,
  handleSpassSubmit,
} from "./logic";
import { closedil } from "./login";

// open dil close dil
const opendil = (id) => {
  document.getElementById(id).style.opacity = "1";
  document.getElementById(id).style.zIndex = "99999";
};

function dgi(id) {
  return document.getElementById(id);
}

// otp verification dilouge body
function VerifyOtp(props) {
  const [otp, setOtp] = useState("");
  useEffect(() => {
    if (otp.length === 6) {
      dgi("otpinput").style.width = "70%";
      dgi("otpbutton").style.width = "30%";
    } else {
      dgi("otpinput").style.width = "100%";
      dgi("otpbutton").style.width = "0%";
    }
  }, [otp]);
  return (
    <div className="dark-mode-choice">
      <div className="dark-mode-choice-item">
        <div className="dic di">
          <KeyIco />
        </div>
        <div className="dic dt">Enter 6 digit OTP</div>
        <div className="dic oi">
          <div className="otpinput">
            <input
              type="number"
              placeholder="******"
              className="starplace"
              id="otpinput"
              value={otp}
              onChange={(e) => {
                if (e.target.value.length <= 6) {
                  setOtp(e.target.value);
                }
              }}
            />

            <button
              onClick={() => {
                if (otp.length === 6) {
                  handleOtpSubmit(otp);
                }
              }}
              id="otpbutton"
            >
              <NextIco />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

// reset password
function ResetPassword(props) {
  const [phone, setPhone] = useState("");
  const [pass, setPass] = useState("");
  const [cpass, setCpass] = useState("");
  const [penter, setPenter] = useState(false);
  useEffect(() => {
    if (phone.length === 10) {
      dgi("passinput").style.width = "80%";
      dgi("passbutton").style.width = "20%";
    } else {
      dgi("passinput").style.width = "100%";
      dgi("passbutton").style.width = "0%";
    }
    if ((pass.length > 8 && !penter) || (cpass.length > 8 && penter)) {
      dgi("passotpinput").style.width = "60%";
      dgi("passotpbutton").style.width = "20%";
    } else {
      dgi("passotpinput").style.width = "80%";
      dgi("passotpbutton").style.width = "0%";
    }
  }, [phone, pass, cpass, penter]);
  return (
    <div className="dark-mode-choice">
      <div className="dark-mode-choice-item">
        <div className="dic di">
          <KeyIco />
        </div>
        <div id="resettitle" className="dic dt">
          Phone Number
        </div>
        <div className="dic oi">
          <div className="otpinput" style={{ width: "80%" }}>
            <div
              id="rphoneprompt"
              style={{ width: "100%", transition: "0.3s" }}
            >
              <input
                type="number"
                placeholder="Phone Number"
                id="passinput"
                value={phone}
                onChange={(e) => {
                  if (e.target.value.length <= 11) {
                    setPhone(e.target.value);
                  }
                }}
              />

              <button
                id="passbutton"
                onClick={() => {
                  dgi("rphoneprompt").style.width = "0%";
                  dgi("rotpprompt").style.width = "100%";
                  dgi("resettitle").innerText = "Enter Password";
                  dgi("passotpinput").focus();
                }}
              >
                <NextIco />
              </button>
            </div>
            <div id="rotpprompt" style={{ width: "0", transition: "0.3s" }}>
              <button
                id="backotpbutton"
                style={{
                  transform: "rotate(180deg)",
                  float: "left",
                }}
                onClick={() => {
                  if (!penter) {
                    dgi("rphoneprompt").style.width = "100%";
                    dgi("rotpprompt").style.width = "0%";
                    dgi("resettitle").innerText = "Phone Number";
                    dgi("passinput").focus();
                    setPass("");
                  } else {
                    setPenter(false);
                    setCpass("");
                    dgi("resettitle").innerText = "Enter Password";
                    dgi("passotpinput").focus();
                  }
                }}
              >
                <NextIco />
              </button>
              <input
                type="password"
                placeholder={!penter ? "New password" : "Confirm Passwod"}
                id="passotpinput"
                value={penter ? cpass : pass}
                onChange={(e) => {
                  penter ? setCpass(e.target.value) : setPass(e.target.value);
                }}
              />
              <button
                id="passotpbutton"
                onClick={() => {
                  if (pass.length > 8 && !penter) {
                    setPenter(true);
                    dgi("resettitle").innerText = "Confirm Password";
                    dgi("passotpinput").focus();
                  } else if (cpass.length > 8 && penter) {
                    if (pass === cpass) {
                      handleResetPassword(phone, pass);
                      closedil("rpass");
                    } else {
                      dgi("resettitle").innerText = "Password not matching";

                      setTimeout(() => {
                        dgi("resettitle").innerText = "Confirm Password";
                      }, 3000);
                    }
                  }
                }}
              >
                <NextIco />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function SetPassword(props) {
  const [pass, setPass] = useState("");
  const [cpass, setCpass] = useState("");
  const [penter, setPenter] = useState(false);
  useEffect(() => {
    if ((pass.length > 8 && !penter) || (cpass.length > 8 && penter)) {
      dgi("setpassotpinput").style.width = "80%";
      dgi("setpassotpbutton").style.width = "20%";
      if (penter) {
        dgi("setpassotpinput").style.width = "60%";
      }
    } else {
      dgi("setpassotpinput").style.width = "100%";
      dgi("setpassotpbutton").style.width = "0%";
      if (penter) {
        dgi("setpassotpinput").style.width = "80%";
      }
    }
  }, [pass, cpass, penter]);
  return (
    <div className="dark-mode-choice">
      <div className="dark-mode-choice-item">
        <div className="dic di">
          <KeyIco />
        </div>
        <div id="setresettitle" className="dic dt">
          Enter Password
        </div>
        <div className="dic oi">
          <div className="otpinput" style={{ width: "80%" }}>
            <div
              id="setrotpprompt"
              style={{ width: "100%", transition: "0.3s" }}
            >
              <button
                id="setbackotpbutton"
                style={{
                  transform: "rotate(180deg)",
                  float: "left",
                  width: "0%",
                }}
                onClick={() => {
                  setPenter(false);
                  setCpass("");
                  dgi("setbackotpbutton").style.width = "0%";
                  dgi("setresettitle").innerText = "Enter Password";
                  dgi("setpassotpinput").focus();
                }}
              >
                <NextIco />
              </button>
              <input
                type="password"
                placeholder={!penter ? "New password" : "Confirm Passwod"}
                id="setpassotpinput"
                value={penter ? cpass : pass}
                onChange={(e) => {
                  penter ? setCpass(e.target.value) : setPass(e.target.value);
                }}
              />
              <button
                id="setpassotpbutton"
                onClick={() => {
                  if (pass.length > 8 && !penter) {
                    setPenter(true);
                    dgi("setbackotpbutton").style.width = "20%";
                    dgi("setresettitle").innerText = "Confirm Password";
                    dgi("setpassotpinput").focus();
                  } else if (cpass.length > 8 && penter) {
                    if (pass === cpass) {
                      handleSpassSubmit(pass, props.history);
                    } else {
                      dgi("setresettitle").innerText = "Password not matching";

                      setTimeout(() => {
                        dgi("setresettitle").innerText = "Confirm Password";
                      }, 3000);
                    }
                  }
                }}
              >
                <NextIco />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default VerifyOtp;
export { ResetPassword, SetPassword };
