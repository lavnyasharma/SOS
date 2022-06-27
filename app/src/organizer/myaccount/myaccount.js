import react, { useContext, useState, useEffect } from "react";
import React from "react";
import { Redirect } from "react-router";

import { authContext } from "../../App";
import "../../css/myaccount.css";
import { te } from "../global/errbox";
import { HeadBar } from "../home/LikedItems/LikedItem";
import Backico from "../home/search/ico";
import { getProfileData, UpdateProfileData } from "./logic";
import {
  AddressValidation,
  AgeValidation,
  EmailValidation,
  GenderValidation,
  NameValidation,
  PhoneValidation,
  PincodeValidation,
} from "./validation";

// input bar
const Input = (props) => {
  const updatestate = (e) => {
    if (props.updatestate) {
      props.updatestate(e.target.value);
    }
  };

  const checkValidation = (e) => {
    if (props.validation && props.validdata) {
      props.validdata(e.target.value, props.id, props.validation);
    }
  };

  return (
    <react.Fragment>
      <input
        type={props.type}
        placeholder={props.placeholder}
        id={props.id}
        className="full-input"
        next={props.tabIndex + 1}
        value={props.value !== "" ? props.value : null}
        onChange={(e) => {
          updatestate(e);
          checkValidation(e);
        }}
        disabled={props.disabled}
        {...props}
        onBlur={(e) => {
          checkValidation(e);
        }}
        maxLength={parseInt(props.maxlength)}
      />
      <label htmlFor={props.id} id={`label${props.id}`}>
        {props.labelname}
      </label>
    </react.Fragment>
  );
};
// half size input bar
function HalfInput(props) {
  return (
    <div className="half">
      <Input {...props} />
    </div>
  );
}
// full size input bar
function FullInput(props) {
  return (
    <div className="container">
      <div className="full">
        <Input {...props} />
      </div>
    </div>
  );
}

// select
function HalfInputSelect(props) {
  const updatestate = (e) => {
    if (props.updatestate) {
      props.updatestate(e.target.value);
    }
  };

  const checkValidation = (e) => {
    if (props.validdata) {
      props.validdata(e.target.value, props.id, props.validation);
    }
  };

  return (
    <div className="half">
      <select
        type={props.type}
        placeholder={props.placeholder}
        id={props.id}
        className="full-input"
        tabIndex={props.tabIndex}
        value={props.value !== "" ? props.value : null}
        onChange={(e) => {
          updatestate(e);
          checkValidation(e);
        }}
        onBlur={(e) => {
          checkValidation(e);
        }}
      >
        {Object.keys(props.options).map((key, index) => (
          <option
            key={key}
            disabled={index === 0 ? true : false}
            selected={index === 0 ? true : false}
            value={props.options[key]}
          >
            {key}
          </option>
        ))}
      </select>
      <label htmlFor={props.id} id={`label${props.id}`}>
        {props.labelname}
      </label>
    </div>
  );
}

function MyAccountBody() {
  const [valid, setValid] = useState([
    "fname",
    "age",
    "email",
    "gender",
    "address",
    "pincode",
  ]);
  const [fname, setFname] = useState("");
  const [lname, setLname] = useState("");
  const [email, setEmail] = useState("");
  const [phone, setPhone] = useState("");
  const [pin, setPin] = useState("");
  const [address, setAddress] = useState("");
  const [gender, setGender] = useState("");
  const [age, setAge] = useState("");

  useEffect(() => {
    getProfileData(
      setAge,
      setGender,
      setPhone,
      setEmail,
      setLname,
      setFname,
      setAddress,
      setPin
    );
  }, []);
  const ifInvalid = (id) => {
    document.getElementById(id).style.border = "2px solid var(--error)";
    document.getElementById(`label${id}`).style.color = "var(--error)";
    setTimeout(() => {
      document.getElementById(id).style.border = "";
      document.getElementById(`label${id}`).style.color = "";
    }, 3000);
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
        document.getElementById(id).style.border = "";
        document.getElementById(`label${id}`).style.color = "";
        setValid(valid.filter((item) => item !== id));
      }
    }
  };
  const validation = (e) => {
    e.preventDefault();
    console.log(valid);
    if (valid.length === 0) {
      UpdateProfileData(age, gender, email, lname, fname, address, pin);
    } else {
      for (let i = 0; i < valid.length; i++) {
        ifInvalid(valid[i]);
      }
      te("Following fields are required");
      return false;
    }
  };
  return (
    <div className="myaccount-body">
      <form
        onSubmit={(e) => {
          validation(e);
        }}
      >
        
        <div className="container">
          <HalfInput
            placeholder="First Name"
            id="fname"
            labelname="First Name"
            tabIndex="0"
            type="text"
            value={fname}
            updatestate={setFname}
            validation={NameValidation}
            validdata={checkValidation}
          />
          <HalfInput
            placeholder="Last Name"
            id="lname"
            labelname="Last Name"
            tabIndex="1"
            type="text"
            value={lname}
            updatestate={setLname}
          />
        </div>
        <FullInput
          placeholder="Email"
          id="email"
          labelname="Email"
          tabIndex="2"
          type="email"
          value={email}
          updatestate={setEmail}
          validation={EmailValidation}
          validdata={checkValidation}
        />
        <FullInput
          placeholder="Phone No."
          id="phone"
          labelname="Phone No."
          tabIndex="3"
          type="tel"
          value={phone}
          updatestate={setPhone}
          disabled={true}
          maxlength={10}
          validation={PhoneValidation}
          validdata={checkValidation}
        />
        <div className="container">
          <HalfInputSelect
            placeholder="Gender"
            id="gender"
            labelname="Gender"
            tabIndex="4"
            type="select"
            options={{
              "select an option": "",
              male: "m",
              female: "f",
              other: "o",
            }}
            value={gender}
            updatestate={setGender}
            validation={GenderValidation}
            validdata={checkValidation}
          />
          <HalfInput
            placeholder="Age"
            id="age"
            labelname="Age"
            tabIndex="5"
            type="number"
            value={age}
            updatestate={setAge}
            validation={AgeValidation}
            validdata={checkValidation}
          />
        </div>
        <FullInput
          placeholder="Pincode"
          id="pincode"
          labelname="Pincode"
          tabIndex="6"
          type="number"
          value={pin}
          updatestate={setPin}
          validation={PincodeValidation}
          validdata={checkValidation}
        />
        <FullInput
          placeholder="Full Address"
          id="address"
          labelname="Full Address"
          tabIndex="7"
          type="text"
          value={address}
          updatestate={setAddress}
          validdata={checkValidation}
          validation={AddressValidation}
        />
        <div className="container"></div>
        <div className="container"></div>
        <button
          className="save-btn"
          type="submit"
          onSubmit={(e) => {
            validation(e);
          }}
        >
          save
        </button>
      </form>
    </div>
  );
}

function MyaAccount(props) {
  const auth = useContext(authContext);
  useEffect(() => {
    document.title = "My Account";
  }, []);
  return (
    <React.Fragment>
      {auth == "1" ? (
        <div className="myaccount-main">
          <HeadBar name="My Account" icon={Backico} back={true} />
          <MyAccountBody />
        </div>
      ) : (
        <Redirect to="/login" />
      )}
    </React.Fragment>
  );
}
export default MyaAccount;
export { MyaAccount, HalfInputSelect, FullInput };
