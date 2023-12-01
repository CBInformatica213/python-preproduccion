function validarCorreo(){

	var emailField = document.getElementById('correo');

	var emailValue = emailField.value.trim();

	if (emailValue === null || emailValue=== '' || emailValue.toLowerCase() === 'empty' || emailValue.toLowerCase() === 'none' || emailValue.toLowerCase() === 'vacio') {
		return true;
	}

	var validEmail = /^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/;

	if (validEmail.test(emailValue)) {
		return true;
	} else {
		alert('Formato de correo inválido, asegúrese de que esté correctamente escrito.');
		return false;
	}
}