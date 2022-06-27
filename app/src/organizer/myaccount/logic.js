import axiosInstance from "../../ax";
import {te, ts} from '../global/errbox'
async function getProfileData(
  setAge,
  setGender,
  setPhone,
  setEmail,
  setLname,
  setFname,
  setAddress,
  setPin
) {
  try {
    const response = await axiosInstance.get("profile/get/", {});
    console.log(response);
    if (response.status === 200) {
      console.log(response.data.data[0]);
      setPhone(response.data.data[0]["phone_number"]);
      setAge(response.data.data[0]["age"]);
      setFname(response.data.data[0]["first_name"]);
      setLname(response.data.data[0]["last_name"]);
      setEmail(response.data.data[0]["email"]);
      setGender(response.data.data[0]["gender"]);
      setPin(response.data.data[0]["pin"]);
      setAddress(response.data.data[0]["address"]);
    } else {
    }
    console.log(response.status);
  } catch (error) {
    te(error.response.data['error']['message']);
  }
}

async function UpdateProfileData(
  age,
  gender,
  email,
  lname,
  fname,
  address,
  pin
) {
  try {
    const response = await axiosInstance.patch("profile/update/", {
      first_name: fname,
      last_name: lname,
      age: age,
      email: email,
      gender: gender,
      pincode: pin,
      address: address,
    });
    console.log(response);
    if (response.status === 200) {
      ts(response.data["data"]["message"])
    } else {
    }
    console.log(response.status);
  } catch (error) {
    te(error.response.data['error']['message']);
  }
}

export { getProfileData, UpdateProfileData };
