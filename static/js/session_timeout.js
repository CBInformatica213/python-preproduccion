// Establece el tiempo de espera de la sesión en milisegundos (1 minuto en este caso)
const tiempoEsperaSesionEnMilisegundos = 120000;

// Función para restablecer el tiempo de espera de la sesión
function restablecerTiempoEsperaSesion() {
  clearTimeout(window.tiempoEsperaSesion);
  window.tiempoEsperaSesion = setTimeout(cerrarSesionUsuario, tiempoEsperaSesionEnMilisegundos);
}

// Función para cerrar la sesión del usuario
function cerrarSesionUsuario() {
  console.log("Cerrando sesión...");
  fetch('/logout', { method: 'POST' })
    .then(() => {
      // Redirige al usuario a la página de inicio de sesión o cualquier otra página deseada después de cerrar sesión
      window.location.href = '/'; // Cambia '/' por la URL deseada si es necesario
      document.addEventListener('click', function (event) {
        console.log('Elemento clicado:', event.target);
      });
    })
    .catch((error) => {
      console.error('Error de cierre de sesión:', error);
    });
}

// Agrega escuchadores de eventos para restablecer el tiempo de espera de la sesión en caso de interacción del usuario
document.addEventListener('mousemove', restablecerTiempoEsperaSesion);
document.addEventListener('mousedown', restablecerTiempoEsperaSesion);
document.addEventListener('keypress', restablecerTiempoEsperaSesion);



// Inicializa la cuenta regresiva del tiempo de espera de la sesión al cargar la página
restablecerTiempoEsperaSesion();
