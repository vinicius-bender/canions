document.addEventListener('DOMContentLoaded', function () {
  // Botão Avaliar
  document.querySelectorAll('.btn-avaliar').forEach(btn => {
    btn.addEventListener('click', function () {
      const obsId = this.dataset.id;
      abrirModal(obsId);
    });
  });

  // Fecha o modal
  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-fechar-modal')) {
      fecharModal();
    }
  });

  function abrirModal(obsId) {
    fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`)
      .then(response => response.text())
      .then(html => {
        document.getElementById('modal-content').innerHTML = html;
        document.getElementById('modal-container').style.display = 'flex';

        // Botão Rejeitar
        const btnRejeitar = document.querySelector('.btn-rejeitar');
        if (btnRejeitar) {
          btnRejeitar.addEventListener('click', function () {
            rejeitarObservacao(this.dataset.id);
          });
        }

        // Formulário de aprovação
        const form = document.getElementById('avaliar-form');
        if (form) {
          form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(form);

            // Adiciona manualmente o campo "aprovar"
            formData.append('aprovar', '1');

            const submitBtn = form.querySelector('button[type="submit"]');
            submitBtn.disabled = true;

            fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`, {
              method: 'POST',
              body: formData,
              headers: {
                'X-CSRFToken': getCookie('csrftoken')
              },
            })
              .then(res => res.json())
              .then(data => {
                if (data.success) {
                  alert('Observação aprovada!');
                  location.reload();
                } else {
                  let msg = 'Erro ao aprovar.';
                  if (data.errors) {
                    msg += '\n' + Object.entries(data.errors).map(
                      ([field, errors]) => `${field}: ${errors.join(', ')}`
                    ).join('\n');
                  } else if (data.error) {
                    msg += `\n${data.error}`;
                  }
                  alert(msg);
                  submitBtn.disabled = false;
                }
              });
          });

        }
      });
  }

  function rejeitarObservacao(obsId) {
    if (confirm("Tem certeza que deseja rejeitar?")) {
      fetch(`/observacoes/pendentes/rejeitar-observacao/${obsId}/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
        },
      }).then(res => {
        if (res.ok) {
          alert('Observação rejeitada.');
          location.reload();
        }
      });
    }
  }

  function fecharModal() {
    document.getElementById('modal-container').style.display = 'none';
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      document.cookie.split(';').forEach(cookie => {
        const c = cookie.trim();
        if (c.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(c.substring(name.length + 1));
        }
      });
    }
    return cookieValue;
  }
});