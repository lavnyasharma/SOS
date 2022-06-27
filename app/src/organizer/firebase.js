import axiosInstance from "../ax";

const config = {
  apiKey: "AIzaSyDgi6FVp9BFb3wlkt3ZPUUt2OQM7BsXOYo",
  authDomain: "thesteth-ddc2f.firebaseapp.com",
  projectId: "thesteth-ddc2f",
  storageBucket: "thesteth-ddc2f.appspot.com",
  messagingSenderId: "561822156916",
  appId: "1:561822156916:web:139f306711ff7564c32921",
  measurementId: "G-TQR2F07DFE",
};

try {
  window.firebase.initializeApp(config);
} catch {}

function IntitalizeFireBaseMessaging() {
  const messaging = window.firebase.messaging();
  var token = messaging
    .requestPermission()
    .then(function () {
      return messaging.getToken();
    })
    .then(function (token) {
      

      fmcjk(token);
    })
    .catch(function (reason) {
      console.log(reason);
    });
}
async function fmcjk(token) {
  try {
    const response = await axiosInstance.post("fmc/add/", {
      fmc_uid:localStorage.getItem("fmc_token")?localStorage.getItem("fmc_token"):"",
      fmc_token: token,
    });
    console.log(response.data["code"]);
    if (response.data["data"]["code"] === 200) {
      localStorage.setItem("fmc_token", response.data["data"]["store"]);
    } else {
      

    }
    console.log(response.data);
  } catch (error) {
    console.log(error.response.data["error"]["message"]);
  }
}

export default IntitalizeFireBaseMessaging;
