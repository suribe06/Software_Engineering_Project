

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
function revisarFormE(){
  var NitId = document.getElementById('NIT');
  var nombreF = document.getElementById('nombre');
  var direccionF = document.getElementById('direccion');
  var telefonoF = document.getElementById('telefono');
  var responsableF = document.getElementById('responsable');
  var cargoF = document.getElementById('cargo');
  var celength = true
  var ver = true
  if(nombreF.value.length == 0){
    celength = celength&&false
  }
  if(responsableF.value.length == 0){
    celength = celength&&false
  }
  if(cargoF.value.length == 0){
    celength = celength&&false
  }
  if (!celength){
    alert('por favor llenar todos los espacios obligatorios del fomulario')
    ver = false
  }
  else if(allLetter(nombreF)&&allLetter(responsableF)&&allLetter(cargoF)&&isNumeric(NitId.value)&&isNumeric(telefonoF.value)){

  }
  else{
    alert('los datos ingresados no son correctos')
    ver = false
  }
  return ver

}

aceptar.addEventListener('click',function(){




  /*
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("myTable");
  tr = table.getElementsByTagName("tr");
  select = document.getElementById('selecting')
  for (i = 0; i < tr.length; i++) {
    var valueS = select.options[select.selectedIndex].value
    td = tr[i].getElementsByTagName("td")[valueS];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }*/
  overlay.classList.remove('active')




})
aceptar2.addEventListener('click', function(){
  overlay2.classList.remove('active')
})

function openPage(pageName, menu ,id , elmnt) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  men = document.getElementsByClassName("container-fluid");

  for (i = 0; i < men.length; i++) {
    men[i].style.display = "none";
  }

  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  document.getElementById(pageName).style.display = "block";
  document.getElementById(menu).style.display = "block";
  document.getElementById(id).style.backgroundColor = "#3E90DB";
}

function load(){
  document.getElementById('RegistroEmpleado').style.display = "block";

  men = document.getElementsByClassName("container-fluid");

  for (i = 0; i < men.length; i++) {
    men[i].style.display = "none";
  }
  document.getElementById("cont").style.display = "block";
  document.getElementById('RegistroEmpleado').style.display = "block";
  document.getElementById('Reg').style.backgroundColor = "#3E90DB";
}

loading = load();


function empty(){

  var nit = document.getElementById('NIT').value = ""
  var nombre = document.getElementById('nombre').value = ""
  var direccion = document.getElementById('direccion').value = ""
  var telefono = document.getElementById('telefono').value =""
  var responsable = document.getElementById('responsable').value = ""
  var cargo = document.getElementById('cargo').value = ""


}
