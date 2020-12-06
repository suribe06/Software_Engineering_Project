



function verificarReq(){
  valid = true;
  var telefono1 = document.getElementById("telefono1").value;
  var telefono2 = document.getElementById("telefono2").value;
  var telefono3 = document.getElementById("telefono3").value;

  valid2 = valid && isNumeric2(telefono1) && isNumeric2(telefono2) && isNumeric2(telefono3);
  console.log(valid2)
  valid4 = valid && valid2;
  if (!valid2) {
    document.getElementById("error").innerHTML = 'Telefono no valido';
  }
  return valid4
}

function isNumeric2(n) {
  return (!isNaN(parseFloat(n)) && isFinite(n)) || n=="";
}
