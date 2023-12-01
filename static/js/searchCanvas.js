document.querySelectorAll(".editar-campos").forEach(function(button) {
  button.addEventListener("click", function() {
    var row = this.closest("tr");
    var campos = row.querySelectorAll("input");

    campos.forEach(function(campo) {
      if (!campo.classList.contains("campo-no-editable")) {
        campo.removeAttribute("readonly");
      }
    });
  });
});
document.querySelectorAll(".guardar-cambios").forEach(function(button) {
  button.addEventListener("click", function() {
    var row = this.closest("tr");
    var campos = row.querySelectorAll(".campo-editable");
    var data = {};

    campos.forEach(function(campo) {
      data[campo.name] = campo.value;
    });

    // Realiza una solicitud AJAX para guardar los cambios en el servidor
    $.ajax({
      url: "/guardar_cambios",
      type: "POST",
      data: data,
      success: function(response) {
        if (response.message) {
          alert(response.message);
          // Puedes agregar aquí el código para actualizar la interfaz de usuario si lo deseas
        } else {
          alert("No se pudo guardar los cambios.");
        }
      },
      error: function(error) {
        alert("Error al guardar los cambios: " + error.responseText);
      },
    });
  });
});
document.querySelectorAll(".eliminar-button").forEach(function(button) {
  button.addEventListener("click", function() {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
      var row = this.closest("tr");
      var data = {
        COD_CB: COD_CB,
        Rut: row.querySelector("[name='Rut']").value,
        Estado: row.querySelector("[name='Estado']").value,
      };

      // Realiza una solicitud AJAX para eliminar el registro
      $.ajax({
        url: "/eliminar_persona_grupo",
        type: "POST",
        data: data,
        success: function(response) {
          alert("Registro eliminado con éxito.");
          // Puedes redirigir o recargar la página aquí si es necesario
        },
        error: function(error) {
          alert("Error al eliminar el registro: " + error);
        },
      });
    }
  });
});

document
  .getElementById("eliminar-button")
  .addEventListener("click", function() {
    if (confirm("¿Estás seguro de que deseas eliminar este registro?")) {
      document.getElementById("eliminar-form").submit();
    }
  });

function volverAInicio() {
  // Simula el comportamiento del enlace al volver a inicio
  window.location.href = "{{ url_for('home') }}";
}

function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}

function performSearch() {
  let timeoutId;
  clearTimeout(timeoutId);

  timeoutId = setTimeout(() => {
    const searchTerm = document.getElementById("NameOrRutSearch").value;

    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `term=${encodeURIComponent(searchTerm)}`,
    })
      .then(response => response.json())
      .then(result => {
        const autocompleteResults = document.getElementById(
          "autocompleteResults"
        );

        // Elimina los resultados anteriores
        autocompleteResults.innerHTML = "";

        // Limita la cantidad de resultados a mostrar (por ejemplo, 5)
        const maxResults = 10;
        const resultsToShow = result.slice(0, maxResults);

        // Crea divs para cada resultado y agrega al div de autocompletar
        resultsToShow.forEach(persona => {
          const resultDiv = document.createElement("div");
          resultDiv.classList.add("autocomplete-item");
          resultDiv.textContent = `${persona.RUT} - ${persona.Nombre} ${persona.A_Paterno} ${persona.A_Materno}`;

          // Agrega un evento click para llenar el textbox con el resultado seleccionado
          resultDiv.addEventListener("click", () => {
            document.getElementById("NameOrRutSearch").value = persona.RUT;
            autocompleteResults.innerHTML = ""; // Limpia los resultados
          });

          autocompleteResults.appendChild(resultDiv);
        });
      })
      .catch(error => console.error("Error:", error));
  }, 300);

  document.getElementById('NameOrRutSearch').addEventListener('input', function() {
    const rut = this.value;
    fetch('/mostrar_nombre_grupo?rut=' + rut)
        .then(response => response.json())
        .then(data => {
            document.getElementById('nombre_grupo').textContent = data.nombre_grupo;
        })
        .catch(error => console.error('Error:', error));
  });
}
// Agrega una función para limpiar la búsqueda
function limpiarBusqueda() {
  document.getElementById("NameOrRutSearch").value = "";
  document.getElementById("autocompleteResults").innerHTML = "";
}


function busquedaRukan() {
  let timeoutId;
  clearTimeout(timeoutId);

  timeoutId = setTimeout(() => {
    const searchTerm = document.getElementById("rukanAndNameSearch").value;

    fetch("/searchRukan", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `term=${encodeURIComponent(searchTerm)}`,
    })
      .then(response => response.json())
      .then(result => {
        const autocompleteResults = document.getElementById(
          "rukanAndNameResults"
        );

        // Elimina los resultados anteriores
        autocompleteResults.innerHTML = "";

        // Limita la cantidad de resultados a mostrar (por ejemplo, 5)
        const maxResults = 10;
        const resultsToShow = result.slice(0, maxResults);

        // Crea divs para cada resultado y agrega al div de autocompletar
        resultsToShow.forEach(rukan => {
          const resultDiv = document.createElement("div");
          resultDiv.classList.add("autocomplete-item");
          resultDiv.textContent = `${rukan.COD_RUKAN} - ${rukan.NOMBRE}`;

          // Agrega un evento click para llenar el textbox con el resultado seleccionado
          resultDiv.addEventListener("click", () => {
            document.getElementById("rukanAndNameSearch").value = rukan.COD_RUKAN;
            autocompleteResults.innerHTML = ""; // Limpia los resultados
          });

          autocompleteResults.appendChild(resultDiv);
        });
      })
      .catch(error => console.error("Error:", error));
  }, 300);
}

// Agrega una función para limpiar la búsqueda
function limpiarBusquedaRukan() {
  document.getElementById("rukanAndNameSearch").value = "";
  document.getElementById("rukanAndNameResults").innerHTML = "";
}

function volverAInicio() {
  // Simula el comportamiento del enlace al volver a inicio
  window.location.href = "{{ url_for('home') }}";
}

function openCity(evt, cityName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(cityName).style.display = "block";
  evt.currentTarget.className += " active";
}