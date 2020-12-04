


function verificarReq(){
  valid = true;
  var telefono1 = document.getElementById("telefono1").value;
  var telefono2 = document.getElementById("telefono2").value;
  var telefono3 = document.getElementById("telefono3").value;
  var correo = document.getElementById("correo").value;
  valid1 = valid && validateEmail(correo);
  valid2 = valid && isNumeric(telefono1) && isNumeric(telefono2) && isNumeric(telefono3);
  valid4 = valid && validateEmail(correo) && isNumeric(telefono1) && isNumeric(telefono2) isNumeric(telefono3);
  if(!valid1){
    document.getElementById("error").innerHTML = 'Correo no valido';
  }else if (!valid2) {
    document.getElementById("error").innerHTML = 'Telefono no valido';
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
$('#editar').submit(verificarReq);
