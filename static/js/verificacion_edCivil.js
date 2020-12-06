


function verificarReq(){
  valid = true;
  var telefono = document.getElementById("telefono").value;

  valid2 = valid && isNumeric(telefono);


  if (!valid2) {
    document.getElementById("error").innerHTML = 'Telefono no valido';
  }
  return valid2
}

function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}

function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}
$('#editar').submit(verificarReq);
