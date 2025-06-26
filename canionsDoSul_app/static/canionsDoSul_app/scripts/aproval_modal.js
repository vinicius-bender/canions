// document.addEventListener('DOMContentLoaded', function () {
//   // Botão Avaliar
//   document.querySelectorAll('.btn-avaliar').forEach(btn => {
//     btn.addEventListener('click', function () {
//       const obsId = this.dataset.id;
//       abrirModal(obsId);
//     });
//   });

//   // Fecha o modal
//   document.addEventListener('click', function (e) {
//     if (e.target.classList.contains('btn-fechar-modal') ||
//       e.target.classList.contains('fechar-button')) {
//       fecharModal();
//     }
//   });

//   function abrirModal(obsId) {
//     fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`)
//       .then(response => response.text())
//       .then(html => {
//         document.getElementById('modal-content').innerHTML = html;
//         document.getElementById('modal-container').style.display = 'flex';

//         inicializarSelects(); // <-- AQUI: chama a função após carregar o conteúdo

//         // Botão Rejeitar
//         const btnRejeitar = document.querySelector('.btn-rejeitar');
//         if (btnRejeitar) {
//           btnRejeitar.addEventListener('click', function () {
//             rejeitarObservacao(this.dataset.id);
//           });
//         }

//         // Formulário de aprovação
//         const form = document.getElementById('avaliar-form');
//         if (form) {
//           form.addEventListener('submit', function (e) {
//             e.preventDefault();
//             const formData = new FormData(form);
//             formData.append('aprovar', '1');

//             const submitBtn = form.querySelector('button[type="submit"]');
//             submitBtn.disabled = true;

//             fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`, {
//               method: 'POST',
//               body: formData,
//               headers: {
//                 'X-CSRFToken': getCookie('csrftoken')
//               },
//             })
//               .then(res => res.json())
//               .then(data => {
//                 if (data.success) {
//                   alert('Observação aprovada!');
//                   location.reload();
//                 } else {
//                   let msg = 'Erro ao aprovar.';
//                   if (data.errors) {
//                     msg += '\n' + Object.entries(data.errors).map(
//                       ([field, errors]) => `${field}: ${errors.join(', ')}`
//                     ).join('\n');
//                   } else if (data.error) {
//                     msg += `\n${data.error}`;
//                   }
//                   alert(msg);
//                   submitBtn.disabled = false;
//                 }
//               });
//           });
//         }
//       });
//   }

//   function rejeitarObservacao(obsId) {
//     if (confirm("Tem certeza que deseja rejeitar?")) {
//       fetch(`/observacoes/pendentes/rejeitar-observacao/${obsId}/`, {
//         method: 'POST',
//         headers: {
//           'X-CSRFToken': getCookie('csrftoken')
//         },
//       }).then(res => {
//         if (res.ok) {
//           alert('Observação rejeitada.');
//           location.reload();
//         }
//       });
//     }
//   }

//   function fecharModal() {
//     document.getElementById('modal-container').style.display = 'none';
//   }

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//       document.cookie.split(';').forEach(cookie => {
//         const c = cookie.trim();
//         if (c.startsWith(name + '=')) {
//           cookieValue = decodeURIComponent(c.substring(name.length + 1));
//         }
//       });
//     }
//     return cookieValue;
//   }

//   document.addEventListener('click', function (e) {
//     if (e.target.classList.contains('btn-delete-image')) {
//       const mediaId = e.target.dataset.imageId;
//       if (confirm('Deseja realmente excluir esta mídia?')) {
//         fetch(`/observacoes/midia/${mediaId}/excluir/`, {
//           method: 'POST',
//           headers: {
//             'X-CSRFToken': getCookie('csrftoken'),
//             'Content-Type': 'application/json',
//           },
//           credentials: 'same-origin',
//         })
//           .then(res => res.json())
//           .then(data => {
//             if (data.success) {
//               document.querySelector(`.media-item[data-id="${mediaId}"]`).remove();
//             } else {
//               alert('Erro ao excluir a mídia: ' + data.error);
//             }
//           })
//           .catch(err => alert('Erro ao excluir a mídia: ' + err));
//       }
//     }
//   });

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//       for (let cookie of document.cookie.split(';')) {
//         cookie = cookie.trim();
//         if (cookie.startsWith(name + '=')) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }

//   const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
//         const suggestionBox = document.getElementById(suggestionsId);

//         input.addEventListener('input', debounce(() => {
//             const term = input.value.trim();
//             if (term.length === 0) {
//                 suggestionBox.innerHTML = '';
//                 return;
//             }

//             let params = new URLSearchParams({ term });

//             if (extraParams) {
//                 const extra = extraParams();
//                 Object.entries(extra).forEach(([key, value]) => {
//                     if (value) params.append(key, value);
//                 });
//             }

//             fetch(`${url}?${params.toString()}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     suggestionBox.innerHTML = '';
//                     data.forEach(item => {
//                         const value = typeof item === 'object' ? item.scientific_name || item.name : item;
//                         const div = document.createElement('div');
//                         div.textContent = value;
//                         if (item.popular_name) div.dataset.popularName = item.popular_name;

//                         div.addEventListener('click', () => {
//                             input.value = value;
//                             suggestionBox.innerHTML = '';
//                             if (onSelect) onSelect(value, div.dataset.popularName || '');
//                         });

//                         suggestionBox.appendChild(div);
//                     });
//                 });
//         }, 150));

//         document.addEventListener('click', (e) => {
//             if (!suggestionBox.contains(e.target) && e.target !== input) {
//                 suggestionBox.innerHTML = '';
//             }
//         });
//     };

//     setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
//     setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => {
//         return { family: family.value };
//     });
//     setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
//         scientificName.value = popName;
//     }, () => {
//         return {
//             family: family.value,
//             genus: genus.value
//         };
//     });

//   // const speciesSelect = document.getElementById('id_species');
//   // if (speciesSelect) {
//   //   speciesSelect.addEventListener('change', function () {
//   //     const speciesId = this.value;
//   //     if (speciesId) {
//   //       fetch(`/especies/${speciesId}/habitat/`)  // Crie essa rota
//   //         .then(response => response.json())
//   //         .then(data => {
//   //           const habitatInput = document.getElementById('id_habitat');
//   //           if (habitatInput && data.habitat) {
//   //             habitatInput.value = data.habitat;
//   //           }
//   //         });
//   //     }
//   //   });
//   // }
// });

// document.addEventListener('DOMContentLoaded', function () {
//   document.querySelectorAll('.btn-avaliar').forEach(btn => {
//     btn.addEventListener('click', function () {
//       const obsId = this.dataset.id;
//       abrirModal(obsId);
//     });
//   });

//   document.addEventListener('click', function (e) {
//     if (
//       e.target.classList.contains('btn-fechar-modal') ||
//       e.target.classList.contains('fechar-button')
//     ) {
//       fecharModal();
//     }

//     if (e.target.classList.contains('btn-delete-image')) {
//       const mediaId = e.target.dataset.imageId;
//       if (confirm('Deseja realmente excluir esta mídia?')) {
//         fetch(`/observacoes/midia/${mediaId}/excluir/`, {
//           method: 'POST',
//           headers: {
//             'X-CSRFToken': getCookie('csrftoken'),
//             'Content-Type': 'application/json',
//           },
//           credentials: 'same-origin',
//         })
//           .then(res => res.json())
//           .then(data => {
//             if (data.success) {
//               document.querySelector(`.media-item[data-id="${mediaId}"]`).remove();
//             } else {
//               alert('Erro ao excluir a mídia: ' + data.error);
//             }
//           })
//           .catch(err => alert('Erro ao excluir a mídia: ' + err));
//       }
//     }
//   });

//   function abrirModal(obsId) {
//     fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`)
//       .then(response => response.text())
//       .then(html => {
//         document.getElementById('modal-content').innerHTML = html;
//         document.getElementById('modal-container').style.display = 'flex';

//         // Elementos já no DOM
//         const family = document.getElementById('id_family');
//         const genus = document.getElementById('id_genus');
//         const species = document.getElementById('id_species');
//         const scientificName = document.getElementById('id_species');
//         const habitatInput = document.getElementById('id_habitat');

//         // Função debounce
//         function debounce(func, wait) {
//           let timeout;
//           return function (...args) {
//             clearTimeout(timeout);
//             timeout = setTimeout(() => func.apply(this, args), wait);
//           };
//         }

//         // Autocomplete com estilo
//         const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
//           const suggestionBox = document.getElementById(suggestionsId);

//           input.addEventListener('input', debounce(() => {
//             const term = input.value.trim();
//             if (term.length === 0) {
//               suggestionBox.style.display = 'block';
//               suggestionBox.innerHTML = '';
//               return;
//             }

//             let params = new URLSearchParams({ term });

//             if (extraParams) {
//               const extra = extraParams();
//               Object.entries(extra).forEach(([key, value]) => {
//                 if (value) params.append(key, value);
//               });
//             }

//             fetch(`${url}?${params.toString()}`)
//               .then(response => response.json())
//               .then(data => {
//                 suggestionBox.innerHTML = '';
//                 data.forEach(item => {
//                   const value = typeof item === 'object' ? item.scientific_name || item.name : item;
//                   const div = document.createElement('div');
//                   div.textContent = value;
//                   if (item.popular_name) div.dataset.popularName = item.popular_name;

//                   div.addEventListener('click', () => {
//                     input.value = value;
//                     suggestionBox.innerHTML = '';
//                     if (onSelect) onSelect(value, div.dataset.popularName || '');
//                   });

//                   suggestionBox.appendChild(div);
//                 });
//               });
//           }, 150));

//           document.addEventListener('click', (e) => {
//             if (!suggestionBox.contains(e.target) && e.target !== input) {
//               suggestionBox.innerHTML = '';
//             }
//           });
//         };

//         // Inicializa autocompletes
//         setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
//         setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => {
//           return { family: family.value };
//         });

//         family.addEventListener('change', () => {
//           genus.value = '';
//           species.value = '';
//           habitatInput.value = '';
//         });

//         setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
//           if (scientificName) {
//             scientificName.value = selected;
//           }

//           // Busca habitat
//           if (family.value && genus.value && selected) {
//             const params = new URLSearchParams({
//               family: family.value,
//               genus: genus.value,
//               term: selected
//             });
//             fetch(`/get-habitat/?${params.toString()}`)
//               .then(res => res.json())
//               .then(data => {
//                 if (data && data.habitat && habitatInput) {
//                   habitatInput.value = data.habitat;
//                 }
//               });
//           }
//         }, () => {
//           return {
//             family: family.value,
//             genus: genus.value
//           };
//         });

//         // Botão Rejeitar
//         const btnRejeitar = document.querySelector('.btn-rejeitar');
//         if (btnRejeitar) {
//           btnRejeitar.addEventListener('click', function () {
//             rejeitarObservacao(this.dataset.id);
//           });
//         }

//         // Formulário
//         const form = document.getElementById('avaliar-form');
//         if (form) {
//           form.addEventListener('submit', function (e) {
//             e.preventDefault();
//             const formData = new FormData(form);
//             formData.append('aprovar', '1');

//             const submitBtn = form.querySelector('button[type="submit"]');
//             submitBtn.disabled = true;

//             fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`, {
//               method: 'POST',
//               body: formData,
//               headers: {
//                 'X-CSRFToken': getCookie('csrftoken')
//               },
//             })
//               .then(res => res.json())
//               .then(data => {
//                 if (data.success) {
//                   alert('Observação aprovada!');
//                   location.reload();
//                 } else {
//                   let msg = 'Erro ao aprovar.';
//                   if (data.errors) {
//                     msg += '\n' + Object.entries(data.errors).map(
//                       ([field, errors]) => `${field}: ${errors.join(', ')}`
//                     ).join('\n');
//                   } else if (data.error) {
//                     msg += `\n${data.error}`;
//                   }
//                   alert(msg);
//                   submitBtn.disabled = false;
//                 }
//               });
//           });
//         }
//       });
//   }

//   function rejeitarObservacao(obsId) {
//     if (confirm("Tem certeza que deseja rejeitar?")) {
//       fetch(`/observacoes/pendentes/rejeitar-observacao/${obsId}/`, {
//         method: 'POST',
//         headers: {
//           'X-CSRFToken': getCookie('csrftoken')
//         },
//       }).then(res => {
//         if (res.ok) {
//           alert('Observação rejeitada.');
//           location.reload();
//         }
//       });
//     }
//   }

//   function fecharModal() {
//     document.getElementById('modal-container').style.display = 'none';
//   }

//   function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//       for (let cookie of document.cookie.split(';')) {
//         cookie = cookie.trim();
//         if (cookie.startsWith(name + '=')) {
//           cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//           break;
//         }
//       }
//     }
//     return cookieValue;
//   }
// });

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.btn-avaliar').forEach(btn => {
    btn.addEventListener('click', function () {
      const obsId = this.dataset.id;
      abrirModal(obsId);
    });
  });

  document.addEventListener('click', function (e) {
    if (
      e.target.classList.contains('btn-fechar-modal') ||
      e.target.classList.contains('fechar-button')
    ) {
      fecharModal();
    }

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

  function abrirModal(obsId) {
    fetch(`/observacoes/pendentes/avaliar-observacao/${obsId}/modal/`)
      .then(response => response.text())
      .then(html => {
        document.getElementById('modal-content').innerHTML = html;
        document.getElementById('modal-container').style.display = 'flex';

        const family = document.getElementById('id_family');
        const genus = document.getElementById('id_genus');
        const species = document.getElementById('id_species');
        const habitatInput = document.getElementById('id_habitat');

        function debounce(func, wait) {
          let timeout;
          return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
          };
        }

        function updateHabitatVisibility() {
          if (!family.value.trim() || !genus.value.trim() || !species.value.trim()) {
            habitatInput.value = '';
            return false;
          }
          return true;
        }

        const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
          const suggestionBox = document.getElementById(suggestionsId);

          input.addEventListener('input', debounce(() => {
            const term = input.value.trim();
            if (term.length === 0) {
              suggestionBox.innerHTML = '';
              suggestionBox.style.display = 'none';
              return;
            }

            let params = new URLSearchParams({ term });
            if (extraParams) {
              const extra = extraParams();
              Object.entries(extra).forEach(([key, value]) => {
                if (value) params.append(key, value);
              });
            }

            fetch(`${url}?${params.toString()}`)
              .then(response => response.json())
              .then(data => {
                suggestionBox.innerHTML = '';
                if (data.length === 0) {
                  suggestionBox.style.display = 'none';
                  return;
                }
                data.forEach(item => {
                  const value = typeof item === 'object' ? item.scientific_name || item.name : item;
                  const div = document.createElement('div');
                  div.textContent = value;
                  if (item.popular_name) div.dataset.popularName = item.popular_name;

                  div.addEventListener('click', () => {
                    input.value = value;
                    suggestionBox.innerHTML = '';
                    suggestionBox.style.display = 'none';
                    if (onSelect) onSelect(value, div.dataset.popularName || '');
                  });

                  suggestionBox.appendChild(div);
                });
                suggestionBox.style.display = 'block';
              });
          }, 150));

          document.addEventListener('click', (e) => {
            if (!suggestionBox.contains(e.target) && e.target !== input) {
              suggestionBox.innerHTML = '';
              suggestionBox.style.display = 'none';
            }
          });
        };

        // Limpa campos dependentes e habitat ao mudar família (input para pegar qualquer alteração)
        family.addEventListener('input', () => {
          genus.value = '';
          species.value = '';
          habitatInput.value = '';
        });

        // Limpa espécie e habitat ao mudar gênero
        genus.addEventListener('input', () => {
          species.value = '';
          habitatInput.value = '';
        });

        // Quando muda espécie, tenta buscar habitat se todos preenchidos
        species.addEventListener('input', debounce(() => {
          if (updateHabitatVisibility()) {
            const params = new URLSearchParams({
              family: family.value.trim(),
              genus: genus.value.trim(),
              term: species.value.trim()
            });
            fetch(`/get-habitat/?${params.toString()}`)
              .then(res => res.json())
              .then(data => {
                habitatInput.value = data?.habitat || '';
              })
              .catch(() => {
                habitatInput.value = '';
              });
          } else {
            habitatInput.value = '';
          }
        }, 300));

        // Inicializa autocompletes
        setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
        setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => ({
          family: family.value.trim()
        }));
        setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
          species.value = selected;
          if (updateHabitatVisibility()) {
            const params = new URLSearchParams({
              family: family.value.trim(),
              genus: genus.value.trim(),
              term: selected.trim()
            });
            fetch(`/get-habitat/?${params.toString()}`)
              .then(res => res.json())
              .then(data => {
                habitatInput.value = data?.habitat || '';
              })
              .catch(() => {
                habitatInput.value = '';
              });
          } else {
            habitatInput.value = '';
          }
        }, () => ({
          family: family.value.trim(),
          genus: genus.value.trim()
        }));

        // Botão rejeitar
        const btnRejeitar = document.querySelector('.btn-rejeitar');
        if (btnRejeitar) {
          btnRejeitar.addEventListener('click', function () {
            rejeitarObservacao(this.dataset.id);
          });
        }

        // Formulário avaliação
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
});