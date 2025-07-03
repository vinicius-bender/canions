// const map = L.map('map').setView([-30.0, -51.0], 6); // Região Sul

// L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//     attribution: '&copy; OpenStreetMap contributors'
// }).addTo(map);

// let marker;

// function buscarLocalizacao(lat, lng) {
//     const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}&accept-language=pt-BR`;

//     fetch(url)
//         .then(response => response.json())
//         .then(data => {
//             const address = data.address;
//             document.getElementById('id_city_name').value = address.city || address.town || address.village || '';
//             document.getElementById('id_state_name').value = address.state || '';
//             document.getElementById('id_country_name').value = address.country || 'Brasil';
//         })
//         .catch(error => {
//             console.error('Erro ao buscar localização:', error);
//         });
// }

// map.on('click', function (e) {
//     const lat = e.latlng.lat.toFixed(8);
//     const lng = e.latlng.lng.toFixed(8);

//     document.getElementById('id_latitude').value = lat;
//     document.getElementById('id_longitude').value = lng;

//     if (marker) map.removeLayer(marker);
//     marker = L.marker([lat, lng]).addTo(map);

//     buscarLocalizacao(lat, lng);
// });

// document.getElementById('btn_buscar_localizacao').addEventListener('click', function () {
//     const lat = document.getElementById('id_latitude').value;
//     const lng = document.getElementById('id_longitude').value;

//     if (lat && lng) {
//         if (marker) map.removeLayer(marker);
//         marker = L.marker([lat, lng]).addTo(map);
//         map.setView([lat, lng], 12);
//         buscarLocalizacao(lat, lng);
//     } else {
//         alert('Preencha latitude e longitude.');
//     }
// });

// document.addEventListener('DOMContentLoaded', () => {
//     const family = document.getElementById('id_family');
//     const genus = document.getElementById('id_genus');
//     const species = document.getElementById('id_species');
//     const scientificName = document.getElementById('id_popular_name');

//     const debounce = (func, delay) => {
//         let timeout;
//         return function (...args) {
//             clearTimeout(timeout);
//             timeout = setTimeout(() => func.apply(this, args), delay);
//         };
//     };

//     const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
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

//     // Contador de caracteres para notes
//     const textarea = document.getElementById('id_notes');
//     const counter = document.getElementById('char-count');
//     const maxLength = 2000;

//     if (textarea && counter) {
//         textarea.addEventListener('input', () => {
//             let text = textarea.value;
//             if (text.length > maxLength) {
//                 textarea.value = text.slice(0, maxLength);
//             }
//             counter.textContent = `${textarea.value.length} / ${maxLength}`;
//         });
//     }
// });

const map = L.map('map').setView([-30.0, -51.0], 6); // Região Sul

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

let marker;

function buscarLocalizacao(lat, lng) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}&accept-language=pt-BR`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const address = data.address || {};
            document.getElementById('id_city_name').value = address.city || address.town || address.village || '';
            document.getElementById('id_state_name').value = address.state || '';
            document.getElementById('id_country_name').value = address.country || 'Brasil';
        })
        .catch(error => {
            console.error('Erro ao buscar localização:', error);
        });
}

map.on('click', function (e) {
    const lat = e.latlng.lat.toFixed(8);
    const lng = e.latlng.lng.toFixed(8);

    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;

    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lng]).addTo(map);

    buscarLocalizacao(lat, lng);
});

document.getElementById('btn_buscar_localizacao').addEventListener('click', function () {
    const lat = document.getElementById('id_latitude').value;
    const lng = document.getElementById('id_longitude').value;

    if (lat && lng) {
        if (marker) map.removeLayer(marker);
        marker = L.marker([lat, lng]).addTo(map);
        map.setView([lat, lng], 12);
        buscarLocalizacao(lat, lng);
    } else {
        alert('Preencha latitude e longitude.');
    }
});

document.addEventListener('DOMContentLoaded', () => {
    const family = document.getElementById('id_family');
    const genus = document.getElementById('id_genus');
    const species = document.getElementById('id_species');
    const scientificName = document.getElementById('id_popular_name');

    const debounce = (func, delay) => {
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    };

    const setupStyledAutocomplete = (input, suggestionsId, url, onSelect = null, extraParams = null) => {
        const suggestionBox = document.getElementById(suggestionsId);

        input.addEventListener('input', debounce(() => {
            const term = input.value.trim();
            if (term.length === 0) {
                suggestionBox.innerHTML = '';
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
                    data.forEach(item => {
                        const value = typeof item === 'object' ? item.scientific_name || item.name : item;
                        const div = document.createElement('div');
                        div.textContent = value;
                        if (item.popular_name) div.dataset.popularName = item.popular_name;

                        div.addEventListener('click', () => {
                            input.value = value;
                            suggestionBox.innerHTML = '';
                            if (onSelect) onSelect(value, div.dataset.popularName || '');
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

    setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
    setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => {
        return { family: family.value };
    });
    setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popName) => {
        scientificName.value = popName;
    }, () => {
        return {
            family: family.value,
            genus: genus.value
        };
    });

    // Contador de caracteres para notes
    const textarea = document.getElementById('id_notes');
    const counter = document.getElementById('char-count');
    const maxLength = 2000;

    if (textarea && counter) {
        textarea.addEventListener('input', () => {
            let text = textarea.value;
            if (text.length > maxLength) {
                textarea.value = text.slice(0, maxLength);
            }
            counter.textContent = `${textarea.value.length} / ${maxLength}`;
        });
    }

    // document.getElementById('submit-button').addEventListener('click', function (e) {
    //     const city = document.getElementById('id_city_name').value.trim();
    //     const state = document.getElementById('id_state_name').value.trim();

    //     const validCities = [
    //         ["Praia Grande", "Santa Catarina"],
    //         ["Jacinto Machado", "Santa Catarina"],
    //         ["Timbé do Sul", "Santa Catarina"],
    //         ["Morro Grande", "Santa Catarina"],
    //         ["Torres", "Rio Grande do Sul"],
    //         ["Mampituba", "Rio Grande do Sul"],
    //         ["Cambará do Sul", "Rio Grande do Sul"]
    //     ];

    //     const isValid = validCities.some(([c, s]) =>
    //         c.toLowerCase() === city.toLowerCase() && s.toLowerCase() === state.toLowerCase()
    //     );

    //     if (!isValid) {
    //         e.preventDefault();
    //         alert("Apenas cidades do Geoparque são permitidas.");
    //     }
    // });
});