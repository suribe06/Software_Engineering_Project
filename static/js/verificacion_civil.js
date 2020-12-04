


function verificarReq(){
  valid = true;
  var telefono = document.getElementById("telefono").value;
  var correo = document.getElementById("correo").value;
  var documento = document.getElementById("documento").value;
  valid1 = valid && validateEmail(correo);
  valid2 = valid && isNumeric(telefono);
  valid3 = valid && isNumeric(documento);
  valid4 = valid && validateEmail(correo) && isNumeric(telefono) && isNumeric(documento);
  if(!valid1){
    document.getElementById("error").innerHTML = 'Correo no valido';
  }else if (!valid2) {
    document.getElementById("error").innerHTML = 'Telefono no valido';
  }else if (!valid3) {
    document.getElementById("error").innerHTML = 'Numero de documento no valido';
  }
  return valid4
}

function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
$('#registro').submit(verificarReq);
