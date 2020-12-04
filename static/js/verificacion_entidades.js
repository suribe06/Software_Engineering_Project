


function verificarReq(){
  valid = true;
  var telefono1 = document.getElementById("telefono1").value;
  var telefono2 = document.getElementById("telefono2").value;
  var telefono3 = document.getElementById("telefono3").value;
  var correo = document.getElementById("correo").value;
  var NIT = document.getElementById("nit").value;
  valid1 = valid && validateEmail(correo);
  valid2 = valid && isNumeric2(telefono1) && isNumeric2(telefono2) && isNumeric2(telefono3);
  valid3 = valid && isNumeric1(NIT);
  valid4 = valid && valid1 && valid2 && valid3;
  if(!valid1){
    document.getElementById("error").innerHTML = 'Correo no valido';
  }else if (!valid2) {
    document.getElementById("error").innerHTML = 'Telefono no valido';
  }else if (!valid3) {
    document.getElementById("error").innerHTML = 'NIT no valido';
  }
  return valid4
}

function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function isNumeric1(n) {
  return (!isNaN(parseFloat(n)) && isFinite(n));
}


function isNumeric2(n) {
  return (!isNaN(parseFloat(n)) && isFinite(n)) || n=="";
}


$('#registro').submit(verificarReq);
