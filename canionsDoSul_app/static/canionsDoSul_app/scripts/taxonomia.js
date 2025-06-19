// document.addEventListener('DOMContentLoaded', () => {
//     const family = document.getElementById('family');
//     const genus = document.getElementById('genus');
//     const species = document.getElementById('species');
//     const popularName = document.getElementById('popular_name');
//     const cadeia = document.getElementById('cadeia-preview');

//     const debounce = (func, delay) => {
//         let timeout;
//         return function (...args) {
//             clearTimeout(timeout);
//             timeout = setTimeout(() => func.apply(this, args), delay);
//         };
//     };

//     function atualizarCadeia() {
//         cadeia.innerHTML = `<span id="family-color">${family.value || 'Família'}</span> - <span id="genus-color">${genus.value || 'Gênero'}</span> - <span id="species-color">${species.value || 'Espécie'}</span>`;
//     }

//     const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null) => {
//         const suggestionBox = document.getElementById(suggestionsId);

//         input.addEventListener('input', debounce(() => {
//             const term = input.value;
//             if (term.length === 0) {
//                 suggestionBox.innerHTML = '';
//                 return;
//             }

//             fetch(`${url}?term=${term}`)
//                 .then(response => response.json())
//                 .then(data => {
//                     suggestionBox.innerHTML = '';
//                     data.forEach(item => {
//                         const value = typeof item === 'object' ? item.scientific_name : item;
//                         const div = document.createElement('div');
//                         div.textContent = value;
//                         if (item.popular_name) div.dataset.popularName = item.popular_name;

//                         div.addEventListener('click', () => {
//                             input.value = value;
//                             suggestionBox.innerHTML = '';
//                             if (onSelect) onSelect(value, div.dataset.popularName || '');
//                             atualizarCadeia();
//                         });

//                         suggestionBox.appendChild(div);
//                     });
//                 });
//         }, 150));

//         // Oculta a lista quando clicar fora
//         document.addEventListener('click', (e) => {
//             if (!suggestionBox.contains(e.target) && e.target !== input) {
//                 suggestionBox.innerHTML = '';
//             }
//         });
//     };

//     setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
//     setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/');
//     setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
//         popularName.value = popName;
//     });

//     [family, genus, species].forEach(el => el.addEventListener('input', atualizarCadeia));

//     //Contador
//     const textarea = document.getElementById('habitat');
//     const counter = document.getElementById('char-count');
//     const maxLength = 2000;
//     const warningThreshold = 1800;

//     if (textarea && counter) {
//         textarea.addEventListener('input', () => {
//             let text = textarea.value;

//             // Impede caracteres além do limite
//             if (text.length > maxLength) {
//                 textarea.value = text.slice(0, maxLength);
//             }

//             const currentLength = textarea.value.length;
//             counter.textContent = `${currentLength} / ${maxLength}`;

//             // Aplica ou remove classe de aviso
//             if (currentLength >= warningThreshold) {
//                 counter.classList.add('warning');
//             } else {
//                 counter.classList.remove('warning');
//             }
//         });
//     }
// });

document.addEventListener('DOMContentLoaded', () => {
    const family = document.getElementById('family');
    const genus = document.getElementById('genus');
    const species = document.getElementById('species');
    const popularName = document.getElementById('popular_name');
    const cadeia = document.getElementById('cadeia-preview');

    const debounce = (func, delay) => {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    function atualizarCadeia() {
        cadeia.innerHTML = `<span id="family-color">${family.value || 'Família'}</span> - <span id="genus-color">${genus.value || 'Gênero'}</span> - <span id="species-color">${species.value || 'Espécie'}</span>`;
    }

    const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
        const suggestionBox = document.getElementById(suggestionsId);

        input.addEventListener('input', debounce(() => {
            const term = input.value.trim();
            if (term.length === 0) {
                suggestionBox.innerHTML = '';
                return;
            }

            let params = new URLSearchParams({ term });

            // Adiciona parâmetros adicionais, como família e gênero
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
                    data.forEach(item => {
                        const value = typeof item === 'object' ? item.scientific_name || item.name : item;
                        const div = document.createElement('div');
                        div.textContent = value;
                        if (item.popular_name) div.dataset.popularName = item.popular_name;

                        div.addEventListener('click', () => {
                            input.value = value;
                            suggestionBox.innerHTML = '';
                            if (onSelect) onSelect(value, div.dataset.popularName || '');
                            atualizarCadeia();
                        });

                        suggestionBox.appendChild(div);
                    });
                });
        }, 150));

        document.addEventListener('click', (e) => {
            if (!suggestionBox.contains(e.target) && e.target !== input) {
                suggestionBox.innerHTML = '';
            }
        });
    };

    // Autocomplete para Família (independente)
    setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');

    // Autocomplete para Gênero (dependente da Família)
    setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => {
        return { family: family.value };
    });

    // Autocomplete para Espécie (dependente da Família e Gênero)
    setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
        popularName.value = popName;
    }, () => {
        return {
            family: family.value,
            genus: genus.value
        };
    });

    [family, genus, species].forEach(el => el.addEventListener('input', atualizarCadeia));

    // Contador de caracteres do habitat
    const textarea = document.getElementById('habitat');
    const counter = document.getElementById('char-count');
    const maxLength = 2000;
    const warningThreshold = 1800;

    if (textarea && counter) {
        textarea.addEventListener('input', () => {
            let text = textarea.value;

            if (text.length > maxLength) {
                textarea.value = text.slice(0, maxLength);
            }

            const currentLength = textarea.value.length;
            counter.textContent = `${currentLength} / ${maxLength}`;

            if (currentLength >= warningThreshold) {
                counter.classList.add('warning');
            } else {
                counter.classList.remove('warning');
            }
        });
    }
});