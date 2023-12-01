function telefono() {
    const numeroTelefono = document.getElementById("fono").value;

    if (numeroTelefono.startsWith("2") || numeroTelefono.startsWith("9")) {
        if (numeroTelefono.length === 9 && /^\d+$/.test(numeroTelefono)) {
            
        } else {
            alert("Por favor, ingrese un número de teléfono válido (9/2 12345678).");
        }
    } else {
        alert("El número de teléfono debe empezar con 9 o 2.");
    }
}