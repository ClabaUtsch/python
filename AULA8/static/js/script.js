document.addEventListener('DOMContentLoaded', function () {

    const formulario = document.getElementById('form-consulta');
    const botao      = document.getElementById('btn-buscar');
    const btnText    = botao ? botao.querySelector('.btn-text') : null;
    const input      = document.getElementById('especialidade');


    if (formulario && botao) {
        formulario.addEventListener('submit', function () {
            if (!input || !input.value.trim()) return;
            botao.classList.add('loading');
            botao.disabled = true;
            if (btnText) btnText.textContent = 'Buscando...';
        });
    }


    if (input) input.focus();


    if (input) {
        input.addEventListener('blur', function () {
            this.value = this.value
                .toLowerCase()
                .replace(/\b\w/g, c => c.toUpperCase());
        });
    }

});


function preencherBusca(especialidade) {
    const input = document.getElementById('especialidade');
    if (input) {
        input.value = especialidade;
        input.focus();
    }
}