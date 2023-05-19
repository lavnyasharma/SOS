import axiosInstance from "../../../ax";
import { te, ts } from "../../global/errbox";

async function guestsos(phone, lati, lon) {
  try {
    const response = await axiosInstance.post("guest/sos/", {
      pno: phone,
      lat: lati,
      long: lon,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      ts(response.data["data"]["message"]);
      localStorage.setItem("guest_sos", "true");
      localStorage.setItem("guest_token", response.data["data"]["token"]);
    } else {
    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
    te(error.response.data["error"]["message"]);
  }
}

async function updatecoordsos(token, lati, lon) {
  try {
    const response = await axiosInstance.post("guest/cood/", {
      token: token,
      lat: lati,
      long: lon,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      ts(response.data["data"]["message"]);
    } else {
    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
    te(error.response.data["error"]["message"]);
  }
}

async function loggedsos( lati, lon) {
  try {
    const response = await axiosInstance.post("logged/sos/", {
      lat: lati,
      long: lon,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      ts(response.data["data"]["message"]);
      localStorage.setItem("guest_sos", "true");
      localStorage.setItem("guest_token", response.data["data"]["token"]);
    } else {
    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
    te(error.response.data["error"]["message"]);
  }
}

async function guestfreewaysos(phone, lati, lon) {
  try {
    const response = await axiosInstance.post("freeway/", {
      pno: phone,
      lat: lati,
      long: lon,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      ts("A  request has been sent");
      localStorage.setItem("guest_freeway_sos", "true");
      localStorage.setItem(
        "guest_freeway_token",
        response.data["data"]["token"]
      );
    } else {
    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
    te(error.response.data["error"]["message"]);
  }
}
export {loggedsos, guestsos, updatecoordsos, guestfreewaysos };
