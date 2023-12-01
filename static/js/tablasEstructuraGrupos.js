document.addEventListener("DOMContentLoaded", function () {
    // Mostrar la primera pestaña por defecto
    document.getElementById("gral").style.display = "block";
  });

function openTab(evt, tabName) {
    // Ocultar todas las pestañas
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Desactivar todos los botones
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Mostrar la pestaña actual y activar el botón
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
  }
  
  // Mostrar la primera pestaña por defecto
  document.getElementById("gral").style.display = "block";
  