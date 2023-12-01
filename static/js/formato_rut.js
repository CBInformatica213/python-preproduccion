function formatearRutEnTiempoReal() {
    const rutInput = document.getElementById("search_rut");
    const mensajeRut = document.getElementById("mensajeRut");
    const rut = rutInput.value.trim().replace(/[-.]/g, "");

    const rutFormateado = formatearRut(rut);
    rutInput.value = rutFormateado;

    if (rut === "") {
        mensajeRut.textContent = "";
        return;
    }

    const rutValido = validarRutChileno(rut);

    if (rutValido) {
        mensajeRut.textContent = "RUT válido: " + rutFormateado;
    } else {
        mensajeRut.textContent = "RUT inválido";
    }
}

    function validarRutChileno(rut) {
        if (typeof rut !== "string") return false;

        const cleanRut = rut.replace(/[-.]/g, "");
        const pattern = /^[0-9]+-[0-9kK]{1}$/;

        if (!pattern.test(cleanRut)) return false;

        const [digits, verifier] = cleanRut.split("-");
        const verifierUpper = verifier.toUpperCase();
        const factor = [2, 3, 4, 5, 6, 7, 2, 3];
        let sum = 0;

        for (let i = digits.length - 1, j = 0; i >= 0; i--, j++) {
            sum += parseInt(digits.charAt(i)) * factor[j];
        }

        const remainder = sum % 11;
        const calculatedVerifier = (11 - remainder).toString();

        if (calculatedVerifier === "10" && verifierUpper === "K") return true;
        if (calculatedVerifier === verifierUpper) return true;

        return false;
}

    function formatearRut(rut) {
        const cleanRut = rut.replace(/[-.]/g, "");
        const digits = cleanRut.slice(0, -1);
        const verifier = cleanRut.slice(-1);
        const formattedRut = digits.replace(/\B(?=(\d{3})+(?!\d))/g, ".") + "-" + verifier;
        return formattedRut;
}