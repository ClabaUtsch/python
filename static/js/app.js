// modo escuro com localStorage
document.addEventListener('DOMContentLoaded', function() {
    var body = document.getElementById('body-pagina');
    var btn = document.getElementById('btn-modo-escuro');

    // carrega preferencia salva
    if (localStorage.getItem('modoEscuro') === 'true') {
        body.classList.add('modo-escuro', 'bg-dark', 'text-light');
        btn.innerHTML = '<i class="bi bi-sun"></i>';
    }

    btn.addEventListener('click', function() {
        body.classList.toggle('modo-escuro');
        body.classList.toggle('bg-dark');
        body.classList.toggle('text-light');

        if (body.classList.contains('modo-escuro')) {
            localStorage.setItem('modoEscuro', 'true');
            btn.innerHTML = '<i class="bi bi-sun"></i>';
        } else {
            localStorage.setItem('modoEscuro', 'false');
            btn.innerHTML = '<i class="bi bi-moon-stars"></i>';
        }
    });
});
