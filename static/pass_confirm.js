var password = document.getElementById("password")
  , confirm_password = document.getElementById("confirm_password");

function validatePassword(value){
  if(password.value !== confirm_password.value) {
    confirm_password.setCustomValidity("Passwords Don't Match");
  } else {
    confirm_password.setCustomValidity('');
    return value;
  }
}

password.onchange = validatePassword;
confirm_password.onkeyup = validatePassword;