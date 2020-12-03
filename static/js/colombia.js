

var xhReq = new XMLHttpRequest();
xhReq.open("GET", '/static/js/colombia.json', false);
xhReq.send(null);
var jsonDatos = JSON.parse(xhReq.responseText);
xhReq.open("GET", '/static/js/barrios.json', false);
xhReq.send(null);
var jsonDatos_2 = JSON.parse(xhReq.responseText);
var dep = document.getElementById("departamento");
var municipio = document.getElementById("municipio");
var barrio = document.getElementById("barrio");
var executed = false;


function cargarDepartamento(){

    if(!executed){
  		let auxHTML = '';
      auxHTML+= '<option  disabled selected>Departamento</option>'
      for(var i in jsonDatos){
  			auxHTML += '<option value="'+ jsonDatos[i].departamento +'">'+ jsonDatos[i].departamento +'</option>';

      }
  		dep.innerHTML = auxHTML;
      executed = true
    }
}

cargarDepartamento();



function cargarMunicipio(){
		let auxHTML = '';
    new_dep = document.getElementById("departamento").value
    console.log(new_dep)
    auxHTML+= '<option  disabled selected>Municipio</option>'
    for (var index in jsonDatos){
      console.log(jsonDatos[index].departamento == new_dep)
      if(jsonDatos[index].departamento == new_dep){
        console.log(jsonDatos[index].ciudades)
        for(var i in jsonDatos[index].ciudades){
    			auxHTML += '<option value="'+ jsonDatos[index].ciudades[i] +'">'+ jsonDatos[index].ciudades[i] +'</option>';

        }
      }
    }
		municipio.innerHTML = auxHTML;
}


function cargarBarrios(){
		let auxHTML = '';
    new_mun = document.getElementById("municipio").value
    console.log(new_mun)
    auxHTML+= '<option  disabled selected>Barrio</option>'
    for (var index in jsonDatos_2){
      console.log(jsonDatos_2[index].ciudad == new_mun)
      if(jsonDatos_2[index].ciudad == new_mun){
        console.log(jsonDatos_2[index].barrios)
        for(var i in jsonDatos_2[index].barrios){
    			auxHTML += '<option value="'+ jsonDatos_2[index].barrios[i] +'">'+ jsonDatos_2[index].barrios[i] +'</option>';

        }
      }
    }
		barrio.innerHTML = auxHTML;
}
