importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");
importScripts(
  "https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"
);

const firebaseConfig = {
  apiKey: "AIzaSyDgi6FVp9BFb3wlkt3ZPUUt2OQM7BsXOYo",
  authDomain: "thesteth-ddc2f.firebaseapp.com",
  projectId: "thesteth-ddc2f",
  storageBucket: "thesteth-ddc2f.appspot.com",
  messagingSenderId: "561822156916",
  appId: "1:561822156916:web:139f306711ff7564c32921",
  measurementId: "G-TQR2F07DFE",
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.setBackgroundMessageHandler(function (payload) {
  console.log(payload);
  const notification = JSON.parse(payload);
  const notificationOption = {
    body: notification.body,
    icon: notification.icon,
  };
  return self.registration.showNotification(
    payload.notification.title,
    notificationOption
  );
});

