import axiosInstance from "../../ax";
import { closedil, opendil } from "./login";
import { te, ts } from "../global/errbox";

const setTokens = (a, r) => {
  localStorage.setItem("access_token", a);

  localStorage.setItem("refresh_token", r);
};
async function handleRegisterSubmit(phone) {
  try {
    const response = await axiosInstance.post("registerphone/", {
      phone_number: phone,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      opendil("otp");
      ts(response.data["data"]["message"])
    } else {
    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
    te(error.response.data["error"]["message"]);
  }
}

async function handleOtpSubmit(sotp) {
  try {
    const response = await axiosInstance.post("verifyotp/", {
      otp: sotp,
    });
    console.log(response);
    if (response.status === 201) {
      localStorage.setItem("set_token", response.data.data["set_token"]);
      ts(response.data["data"]["message"])
      opendil("spass");
      closedil("otp");
    } else {
    }
    console.log(response.data.data["set_token"]);
  } catch (error) {
    console.log(error.response.status);
    te(error.response.data["error"]["message"]);
  }
}

async function handleSpassSubmit(spass, history) {
  try {
    const response = await axiosInstance.post("password/set/", {
      password: spass,
      verification_token: localStorage.getItem("set_token"),
    });
    console.log(response);
    if (response.status === 202) {
      ts(response.data["data"]["message"])
      closedil("spass");
      localStorage.removeItem("set_token");
      setTokens(
        response.data.data["tokens"]["access"],
        response.data.data["tokens"]["refresh"]
      );
      history.push("/");
    } else {
    }
    console.log(response.status);
  } catch (error) {
    te(error.response.data["error"]["message"]);
  }
}

async function handleLoginSubmit(phone, pass, history) {
  try {
    const response = await axiosInstance.post("login/password/", {
      password: pass,
      credentials: phone,
    });
    console.log(response);
    if (response.status === 202) {
      ts(response.data["data"]["message"])
      setTokens(
        response.data.data["tokens"]["access"],
        response.data.data["tokens"]["refresh"]
      );
      console.log(response.data.data);
      localStorage.setItem("usertype",response.data.data['usertype'])
      history.push("/");
    } else {
    }
    console.log(response.status);
    return true;
  } catch (error) {
    console.log(error.response);
    te(error.response.data["error"]["message"]);
    
  }
}

async function handleResetPassword(phone, pass) {
  try {
    const response = await axiosInstance.post("password/change/", {
      password: pass,
      credential: phone,
    });
    console.log(response);
    if (response.status === 200) {
      ts(response.data["data"]["message"])
    } else {
    }
    console.log(response.status);
  } catch (error) {
    te(error.response.data["error"]["message"]);
  }
}
export {
  handleRegisterSubmit,
  handleOtpSubmit,
  handleSpassSubmit,
  handleResetPassword,
  handleLoginSubmit,
};
