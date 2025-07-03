// function fetchGeolocation() {
//     const city = document.getElementById("id_city_name").value.trim();
//     const state = document.getElementById("id_state_name").value.trim();
//     const statusDiv = document.getElementById("location-status");

//     if (city && state) {
//         statusDiv.textContent = "Buscando localização...";

//         // const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=Brasil&format=json&addressdetails=1`;
//         const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&format=json&addressdetails=1`;
//         fetch(url)
//             .then(response => response.json())
//             .then(data => {
//                 if (data && data.length > 0) {
//                     const location = data[0];
//                     const address = location.address;
//                     const country = (address.country || "").toLowerCase();

//                     if (country.includes("brasil") || country.includes("brazil")) {
//                         document.getElementById("id_latitude").value = location.lat;
//                         document.getElementById("id_longitude").value = location.lon;
//                         document.getElementById("id_country_name").value = "Brasil";
//                         statusDiv.textContent = "✅ Localização encontrada com sucesso!";
//                     } else {
//                         document.getElementById("id_latitude").value = "";
//                         document.getElementById("id_longitude").value = "";
//                         document.getElementById("id_country_name").value = primeiraLetraDeCadaPalavraMaiuscula(country);
//                         statusDiv.textContent = "🌍 A cidade/estado informados não pertencem ao Brasil.";
//                     }
//                 } else {
//                     document.getElementById("id_latitude").value = "";
//                     document.getElementById("id_longitude").value = "";
//                     // document.getElementById("id_country_name").value = "";
//                     document.getElementById("id_country_name").value = country;
//                     statusDiv.textContent = "❌ Localização não encontrada.";
//                 }
//             })
//             .catch(error => {
//                 console.error("Erro ao buscar a geolocalização:", error);
//                 statusDiv.textContent = "⚠️ Erro ao buscar a geolocalização.";
//             });
//     }
// }

// function fetchGeolocation() {
//     const city = document.getElementById("id_city_name").value.trim();
//     const state = document.getElementById("id_state_name").value.trim();
//     const statusDiv = document.getElementById("location-status");
//     const spinner = document.getElementById("loading-spinner");
//     const submitButton = document.getElementById("submit-button");

//     if (city && state) {
//         statusDiv.textContent = "";
//         spinner.style.display = "inline"; // mostra o spinner
//         submitButton.disabled = true;

//         const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&format=json&addressdetails=1`;

//         fetch(url)
//             .then(response => response.json())
//             .then(data => {
//                 spinner.style.display = "none"; // esconde o spinner
//                 if (data && data.length > 0) {
//                     const location = data[0];
//                     const address = location.address;
//                     const country = (address.country || "").toLowerCase();

//                     if (country.includes("brasil") || country.includes("brazil")) {
//                         document.getElementById("id_latitude").value = location.lat;
//                         document.getElementById("id_longitude").value = location.lon;
//                         document.getElementById("id_country_name").value = "Brasil";
//                         statusDiv.textContent = "✅ Localização encontrada com sucesso!";
//                         submitButton.disabled = false; // habilita o botão
//                     } else {
//                         limparCamposLocalizacao();
//                         document.getElementById("id_country_name").value = primeiraLetraDeCadaPalavraMaiuscula(country);
//                         statusDiv.textContent = "🌍 A cidade/estado informados não pertencem ao Brasil.";
//                         submitButton.disabled = true;
//                     }
//                 } else {
//                     limparCamposLocalizacao();
//                     statusDiv.textContent = "❌ Localização não encontrada.";
//                     submitButton.disabled = true;
//                 }
//             })
//             .catch(error => {
//                 console.error("Erro ao buscar a geolocalização:", error);
//                 spinner.style.display = "none";
//                 statusDiv.textContent = "⚠️ Erro ao buscar a geolocalização.";
//                 submitButton.disabled = true;
//             });
//     } else {
//         statusDiv.textContent = "";
//         spinner.style.display = "none";
//         submitButton.disabled = true;
//     }
// }

// function limparCamposLocalizacao() {
//     document.getElementById("id_latitude").value = "";
//     document.getElementById("id_longitude").value = "";
//     document.getElementById("id_country_name").value = "";
// }

// function primeiraLetraDeCadaPalavraMaiuscula(frase) {
//     return frase.split(" ").map(function (palavra) {
//         return palavra.charAt(0).toUpperCase() + palavra.slice(1);
//     }).join(" ");
// }

// function setupAutocomplete(inputId, suggestionBoxId, endpoint) {
//     const input = document.getElementById(inputId);
//     const suggestionsBox = document.getElementById(suggestionBoxId);

//     input.addEventListener("input", function () {
//         const query = input.value.trim();

//         if (query.length < 2) {
//             suggestionsBox.innerHTML = "";
//             return;
//         }

//         fetch(`${endpoint}?q=${encodeURIComponent(query)}`)
//             .then(response => response.json())
//             .then(data => {
//                 suggestionsBox.innerHTML = "";
//                 data.forEach(item => {
//                     const div = document.createElement("div");
//                     div.textContent = item;
//                     div.classList.add("suggestion-item");
//                     div.addEventListener("click", function () {
//                         input.value = item;
//                         suggestionsBox.innerHTML = "";
//                     });
//                     suggestionsBox.appendChild(div);
//                 });
//             });
//     });

//     // Fecha sugestões ao clicar fora
//     document.addEventListener("click", function (event) {
//         if (!input.contains(event.target) && !suggestionsBox.contains(event.target)) {
//             suggestionsBox.innerHTML = "";
//         }
//     });
// }

// let debounceTimer;

// document.addEventListener("DOMContentLoaded", function () {
//     const cityInput = document.getElementById("id_city_name");
//     const stateInput = document.getElementById("id_state_name");
//     const submitButton = document.getElementById("submit-button");
//     // const btnText = submitButton.querySelector(".btn-text");
//     // const btnSpinner = submitButton.querySelector(".btn-spinner");
//     // const form = document.querySelector("form");

//     let debounceTimer;

//     function handleInputChange() {
//         clearTimeout(debounceTimer);
//         debounceTimer = setTimeout(fetchGeolocation, 1000);
//     }

//     cityInput.addEventListener("input", handleInputChange);
//     stateInput.addEventListener("input", handleInputChange);

//      setupAutocomplete("id_family", "family-suggestions", "/autocomplete-family/");
//     setupAutocomplete("id_genus", "genus-suggestions", "/autocomplete-genus/");
//     setupAutocomplete("id_species", "species-suggestions", "/autocomplete-species/");

// });

function fetchGeolocation() {
    const city = document.getElementById("id_city_name").value.trim();
    const state = document.getElementById("id_state_name").value.trim();
    const statusDiv = document.getElementById("location-status");
    const spinner = document.getElementById("loading-spinner");
    const submitButton = document.getElementById("submit-button");

    if (city && state) {
        statusDiv.textContent = "";
        spinner.style.display = "inline";
        submitButton.disabled = true;

        const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&format=json&addressdetails=1`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                spinner.style.display = "none";
                if (data && data.length > 0) {
                    const location = data[0];
                    const address = location.address;
                    const country = (address.country || "").toLowerCase();

                    if (country.includes("brasil") || country.includes("brazil")) {
                        document.getElementById("id_latitude").value = location.lat;
                        document.getElementById("id_longitude").value = location.lon;
                        document.getElementById("id_country_name").value = "Brasil";
                        statusDiv.textContent = "✅ Localização encontrada com sucesso!";
                        submitButton.disabled = false;
                    } else {
                        limparCamposLocalizacao();
                        document.getElementById("id_country_name").value = primeiraLetraDeCadaPalavraMaiuscula(country);
                        statusDiv.textContent = "🌍 A cidade/estado informados não pertencem ao Brasil.";
                        submitButton.disabled = true;
                    }
                } else {
                    limparCamposLocalizacao();
                    statusDiv.textContent = "❌ Localização não encontrada.";
                    submitButton.disabled = true;
                }
            })
            .catch(error => {
                console.error("Erro ao buscar a geolocalização:", error);
                spinner.style.display = "none";
                statusDiv.textContent = "⚠️ Erro ao buscar a geolocalização.";
                submitButton.disabled = true;
            });
    } else {
        statusDiv.textContent = "";
        spinner.style.display = "none";
        submitButton.disabled = true;
    }
}

function limparCamposLocalizacao() {
    document.getElementById("id_latitude").value = "";
    document.getElementById("id_longitude").value = "";
    document.getElementById("id_country_name").value = "";
}

function primeiraLetraDeCadaPalavraMaiuscula(frase) {
    return frase.split(" ").map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(" ");
}

// --- AUTOCOMPLETE MODERNO ---

const debounce = (func, delay) => {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
};

function setupStyledAutocomplete(input, suggestionsId, url, onSelect = null, extraParams = null) {
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

                    div.classList.add('suggestion-item');

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
}

// --- INICIALIZAÇÃO ---
document.addEventListener("DOMContentLoaded", function () {
    const cityInput = document.getElementById("id_city_name");
    const stateInput = document.getElementById("id_state_name");
    const submitButton = document.getElementById("submit-button");

    cityInput.addEventListener("input", debounce(fetchGeolocation, 400));
    stateInput.addEventListener("input", debounce(fetchGeolocation, 400));

    // --- Autocomplete da fauna ---
    const family = document.getElementById('id_family');
    const genus = document.getElementById('id_genus');
    const species = document.getElementById('id_species');
    const popName = document.getElementById('id_popular_name');

    setupStyledAutocomplete(family, 'family-suggestions', '/autocomplete-family/');
    setupStyledAutocomplete(genus, 'genus-suggestions', '/autocomplete-genus/', null, () => {
        return { family: family.value };
    });
    setupStyledAutocomplete(species, 'species-suggestions', '/autocomplete-species/', (selected, popular) => {
        if (popName) popName.value = popular;
    }, () => {
        return {
            family: family.value,
            genus: genus.value
        };
    });

    // Contador de caracteres para habitat
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
});