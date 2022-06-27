import axiosInstance from "../../../ax";
import { ts } from "../../global/errbox";

async function logout(history) {
  var c = localStorage.getItem("Auth_state")
    ? localStorage.removeItem("Auth_state")
    : null;
  var m = localStorage.getItem("access_token")
    ? localStorage.removeItem("access_token")
    : null;
    var k = localStorage.getItem("usertype")
    ? localStorage.removeItem("usertype")
    : null;
  var m = localStorage.getItem("access_token")
    ? localStorage.removeItem("access_token")
    : null;
  try {
    let response = await axiosInstance.post("logout/", {
      refresh_token: localStorage.getItem("refresh_token"),
    });
    if (response.status === 205) {
      ts("logged out");
      history.push("/");
    }
    var m = localStorage.getItem("refresh_token")
      ? localStorage.removeItem("refresh_token")
      : null;

    return response;
  } catch (error) {
    console.log("User error: ", JSON.stringify(error, null, 4));
  }
}

export { logout };
