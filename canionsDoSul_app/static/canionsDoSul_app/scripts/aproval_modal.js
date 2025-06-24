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
    if (e.target.classList.contains('btn-fechar-modal') ||
      e.target.classList.contains('fechar-button')) {
      fecharModal();
    }
  });

  function abrirModal(obsId) {
    fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`)
      .then(response => response.text())
      .then(html => {
        document.getElementById('modal-content').innerHTML = html;
        document.getElementById('modal-container').style.display = 'flex';

        inicializarSelects(); // <-- AQUI: chama a função após carregar o conteúdo

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

  document.addEventListener('click', function (e) {
    if (e.target.classList.contains('btn-delete-image')) {
      const mediaId = e.target.dataset.imageId;
      if (confirm('Deseja realmente excluir esta mídia?')) {
        fetch(`/observacoes/midia/${mediaId}/excluir/`, {
          method: 'POST',
          headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
          },
          credentials: 'same-origin',
        })
          .then(res => res.json())
          .then(data => {
            if (data.success) {
              document.querySelector(`.media-item[data-id="${mediaId}"]`).remove();
            } else {
              alert('Erro ao excluir a mídia: ' + data.error);
            }
          })
          .catch(err => alert('Erro ao excluir a mídia: ' + err));
      }
    }
  });

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      for (let cookie of document.cookie.split(';')) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  const speciesSelect = document.getElementById('id_species');
  if (speciesSelect) {
    speciesSelect.addEventListener('change', function () {
      const speciesId = this.value;
      if (speciesId) {
        fetch(`/especies/${speciesId}/habitat/`)  // Crie essa rota
          .then(response => response.json())
          .then(data => {
            const habitatInput = document.getElementById('id_habitat');
            if (habitatInput && data.habitat) {
              habitatInput.value = data.habitat;
            }
          });
      }
    });
  }
});