document.addEventListener('DOMContentLoaded', () => {
  const modalContainer = document.getElementById('modal-container');
  const modalContent = document.getElementById('modal-content');

  // Função para fechar modal e limpar conteúdo
  function fecharModal() {
    modalContainer.style.display = 'none';
    modalContent.innerHTML = '';
  }

  // Fecha modal ao clicar fora do conteúdo
  modalContainer.addEventListener('click', (e) => {
    if (e.target === modalContainer) fecharModal();
  });

  // Delegação de clique para botões dos ícones
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-icon');
    if (!btn) return;

    const url = btn.dataset.url;  // pega URL completa
    const action = btn.dataset.action;
    if (!url || !action) return;

    fetch(url)
      .then(r => r.text())
      .then(html => {
        modalContent.innerHTML = html;
        modalContainer.style.display = 'flex';

        // Botão fechar dentro do modal
        modalContent.querySelectorAll('.btn-fechar-modal').forEach(btnFechar => {
          btnFechar.addEventListener('click', fecharModal);
        });

        modalContent.querySelectorAll('.close-btn').forEach(btnFechar => {
          btnFechar.addEventListener('click', fecharModal);
        });

        // Formulário de edição
        if (action === 'edit') {
          const editForm = document.getElementById('edit-form');
          if (editForm) {
            editForm.addEventListener('submit', e => {
              e.preventDefault();
              const formData = new FormData(editForm);
              fetch(url, { method: 'POST', body: formData })
                .then(r => r.json())
                .then(data => {
                  if (data.success) window.location.reload();
                  else alert('Erro ao salvar edição');
                });
            });
          }
        }

        // Formulário de exclusão
        if (action === 'delete') {
          const deleteForm = document.getElementById('delete-form');
          if (deleteForm) {
            deleteForm.addEventListener('submit', e => {
              e.preventDefault();
              const formData = new FormData(deleteForm);
              fetch(url, { method: 'POST', body: formData })
                .then(r => r.json())
                .then(data => {
                  if (data.success) window.location.reload();
                  else alert('Erro ao excluir');
                });
            });
          }
        }
      })
      .catch(() => alert('Erro ao carregar modal'));
  });

  // Filtro em tempo real do input searchInput
  const searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', () => {
      const searchValue = searchInput.value.toLowerCase();
      document.querySelectorAll('.species-list-item').forEach(item => {
        const nome = item.dataset.nome.toLowerCase();
        item.style.display = nome.includes(searchValue) ? 'flex' : 'none';
      });
    });
  }
});





// document.addEventListener('DOMContentLoaded', () => {
//   const modalContainer = document.getElementById('modal-container');
//   const modalContent = document.getElementById('modal-content');

//   const iconButtons = document.querySelectorAll('.btn-icon');

//   if (!iconButtons.length) {
//     console.warn('Nenhum botão com .btn-icon encontrado.');
//   }

//   iconButtons.forEach(button => {
//     button.addEventListener('click', () => {
//       const id = button.dataset.id;
//       const action = button.dataset.action;

//       console.log(`Clicado: ${action} | ID: ${id}`);

//       let url = '';

//       if (action === 'info') url = `/especie/${id}/info/`;
//       else if (action === 'edit') url = `/especie/${id}/editar/`;
//       else if (action === 'delete') url = `/especie/${id}/deletar/`;

//       fetch(url)
//         .then(r => r.text())
//         .then(html => {
//           modalContent.innerHTML = html;
//           modalContainer.style.display = 'flex';

//           if (action === 'edit') {
//             document.getElementById('edit-form').addEventListener('submit', e => {
//               e.preventDefault();
//               const formData = new FormData(e.target);
//               fetch(url, {
//                 method: 'POST',
//                 body: formData
//               }).then(r => r.json()).then(data => {
//                 if (data.success) window.location.reload();
//               });
//             });
//           }

//           if (action === 'delete') {
//             document.getElementById('delete-form').addEventListener('submit', e => {
//               e.preventDefault();
//               const formData = new FormData(e.target);
//               fetch(url, {
//                 method: 'POST',
//                 body: formData
//               }).then(r => r.json()).then(data => {
//                 if (data.success) window.location.reload();
//               });
//             });
//           }
//         });
//     });
//   });
// });

// document.addEventListener('DOMContentLoaded', () => {
//   const modalContainer = document.getElementById('modal-container');
//   const modalContent = document.getElementById('modal-content');

//   document.querySelectorAll('.btn-icon').forEach(button => {
//     button.addEventListener('click', () => {
//       const id = button.dataset.id;
//       const action = button.dataset.action;
//       let url = '';

//       if (action === 'info') url = `/especie/${id}/info/`;
//       else if (action === 'edit') url = `/especie/${id}/editar/`;
//       else if (action === 'delete') url = `/especie/${id}/deletar/`;

//       fetch(url)
//         .then(r => r.text())
//         .then(html => {
//           modalContent.innerHTML = html;
//           modalContainer.style.display = 'flex';

//           if (action === 'edit') {
//             document.getElementById('edit-form').addEventListener('submit', e => {
//               e.preventDefault();
//               const formData = new FormData(e.target);
//               fetch(url, {
//                 method: 'POST',
//                 body: formData
//               }).then(r => r.json()).then(data => {
//                 if (data.success) window.location.reload();
//               });
//             });
//           }

//           if (action === 'delete') {
//             document.getElementById('delete-form').addEventListener('submit', e => {
//               e.preventDefault();
//               const formData = new FormData(e.target);
//               fetch(url, {
//                 method: 'POST',
//                 body: formData
//               }).then(r => r.json()).then(data => {
//                 if (data.success) window.location.reload();
//               });
//             });
//           }
//         });
//     });
//   });

//   // 🔍 Filtro em tempo real
//   const searchInput = document.getElementById('searchInput');
//   if (searchInput) {
//     searchInput.addEventListener('input', () => {
//       const searchValue = searchInput.value.toLowerCase();
//       document.querySelectorAll('.species-list-item').forEach(item => {
//         const nome = item.dataset.nome.toLowerCase();
//         item.style.display = nome.includes(searchValue) ? 'flex' : 'none';
//       });
//     });
//   }
// });

// function fecharModal() {
//   document.getElementById('modal-container').style.display = 'none';
//   document.getElementById('modal-content').innerHTML = '';
// }