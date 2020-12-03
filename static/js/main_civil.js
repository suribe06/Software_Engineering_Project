var openPopUp1 = document.getElementById('filtrar'),
    openPopUp2 = document.getElementById('filtrar2'),
    overlay = document.getElementById('overlay'),
    overlay2 = document.getElementById('overlay2'),
    popUp = document.getElementById('popUp'),
    aceptar = document.getElementById('buttonFilt')
    aceptar2 = document.getElementById('buttonFilt2')

openPopUp1.addEventListener('click', function(){
  overlay.classList.add('active')
})

openPopUp2.addEventListener('click', function(){
  overlay2.classList.add('active')
})

function validateEmail(email) {
  var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(email);
}
function allLetter(inputtxt){
      var letters = /^[A-Za-z]+$/;
      if(inputtxt.value.match(letters))
      {
      //alert('Your name have accepted : you can try another');
      return true;
      }
      else
      {
      //alert('Please input alphabet characters only');
      return false;
      }
}
function isNumeric(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
}

aceptar.addEventListener('click',function(){
  overlay.classList.remove('active')
})

aceptar2.addEventListener('click', function(){
  overlay2.classList.remove('active')
})
