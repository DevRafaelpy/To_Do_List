
// Aqui é pra validar
const senha = document.getElementById('cad-senha');
const confirma = document.getElementById('cad-confirma');

function conferirSenhas() {
    confirma.setCustomValidity(
        senha.value !== confirma.value ? 'Senha incorreta.' : ''
    );
}

senha.addEventListener('input', conferirSenhas);
confirma.addEventListener('input', conferirSenhas);