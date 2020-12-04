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

function download(){
  alert("Su archivo fue descargado con exito");
}

aceptar.addEventListener('click',function(){
  overlay.classList.remove('active')
})

aceptar2.addEventListener('click', function(){
  overlay2.classList.remove('active')
})
