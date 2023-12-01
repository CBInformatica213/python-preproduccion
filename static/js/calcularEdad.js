document.addEventListener("DOMContentLoaded", function() {
    const fechaNacimientoInput = document.getElementById("fechaNacimiento");
    const edadInput = document.getElementById("edad");

    // Agrega un controlador de eventos al campo de fecha de nacimiento
    fechaNacimientoInput.addEventListener("change", calcularEdad);

    // Función para calcular la edad
    function calcularEdad() {
      // Obtiene la fecha de nacimiento del campo de entrada
      const fechaNacimiento = new Date(fechaNacimientoInput.value);

      // Obtiene la fecha actual
      const fechaActual = new Date();

      // Calcula la diferencia en años
      const edad = fechaActual.getFullYear() - fechaNacimiento.getFullYear();

      // Verifica si ya ha pasado el cumpleaños de la persona este año
      if (
        fechaActual.getMonth() < fechaNacimiento.getMonth() ||
        (fechaActual.getMonth() === fechaNacimiento.getMonth() &&
          fechaActual.getDate() < fechaNacimiento.getDate())
      ) {
        edad--;
      }

      // Actualiza el campo de entrada de edad
      edadInput.value = edad;
    }
  });