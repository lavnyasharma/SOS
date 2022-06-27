function NameValidation(name) {
  let regName = /^[A-Za-z]+$/;

  if (!regName.test(name)) {
    return false;
  }
  return true;
}

function PincodeValidation(pin) {
  let regPin = /^\d{6}$/;

  if (!regPin.test(pin)) {
    return false;
  }
  return true;
}

function PhoneValidation(b) {
  let a = /^\d{10}$/;
  if (a.test(b)) {
    return true;
  }
  return false;
}

function EmailValidation(enteredEmail) {
  var mail_format =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  if (mail_format.test(enteredEmail)) {
    return true;
  }
  return false;
}

function AgeValidation(age) {
  if (!(age > 1 && age < 100)) {
    return false;
  }
  return true;
}
function AddressValidation(address) {
  if (address == "") {
    return false;
  }
  return true;
}
function PasswordValidation(password) {
    if (password.length < 8) {
      return false;
    }
    return true;
  }
function GenderValidation(gender) {
  if (gender == "") {
    return false;
  }
  return true;
}
export {
  NameValidation,
  PincodeValidation,
  PhoneValidation,
  EmailValidation,
  AgeValidation,
  AddressValidation,
  GenderValidation,
  PasswordValidation
};
