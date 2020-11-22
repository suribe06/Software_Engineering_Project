

function openPage(menu ,id , elmnt) {
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
  document.getElementById(menu).style.display = "block";
  document.getElementById(id).style.backgroundColor = "#3E90DB";
}

function load(){

  men = document.getElementsByClassName("container-fluid");

  for (i = 0; i < men.length; i++) {
    men[i].style.display = "none";
  }
  document.getElementById("cont").style.display = "block";
}

loading = load();
