function fetchGeolocation() {
    const city = document.getElementById("id_city_name").value.trim();
    const state = document.getElementById("id_state_name").value.trim();
    const statusDiv = document.getElementById("location-status");

    if (city && state) {
        statusDiv.textContent = "Buscando localização...";

        // const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=Brasil&format=json&addressdetails=1`;
        const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&format=json&addressdetails=1`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data && data.length > 0) {
                    const location = data[0];
                    const address = location.address;
                    const country = (address.country || "").toLowerCase();

                    if (country.includes("brasil") || country.includes("brazil")) {
                        document.getElementById("id_latitude").value = location.lat;
                        document.getElementById("id_longitude").value = location.lon;
                        document.getElementById("id_country_name").value = "Brasil";
                        statusDiv.textContent = "✅ Localização encontrada com sucesso!";
                    } else {
                        document.getElementById("id_latitude").value = "";
                        document.getElementById("id_longitude").value = "";
                        document.getElementById("id_country_name").value = primeiraLetraDeCadaPalavraMaiuscula(country);
                        statusDiv.textContent = "🌍 A cidade/estado informados não pertencem ao Brasil.";
                    }
                } else {
                    document.getElementById("id_latitude").value = "";
                    document.getElementById("id_longitude").value = "";
                    // document.getElementById("id_country_name").value = "";
                    document.getElementById("id_country_name").value = country;
                    statusDiv.textContent = "❌ Localização não encontrada.";
                }
            })
            .catch(error => {
                console.error("Erro ao buscar a geolocalização:", error);
                statusDiv.textContent = "⚠️ Erro ao buscar a geolocalização.";
            });
    }
}

function fetchGeolocation() {
    const city = document.getElementById("id_city_name").value.trim();
    const state = document.getElementById("id_state_name").value.trim();
    const statusDiv = document.getElementById("location-status");
    const spinner = document.getElementById("loading-spinner");
    const submitButton = document.getElementById("submit-button");

    if (city && state) {
        statusDiv.textContent = "";
        spinner.style.display = "inline"; // mostra o spinner
        submitButton.disabled = true;

        const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&format=json&addressdetails=1`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                spinner.style.display = "none"; // esconde o spinner
                if (data && data.length > 0) {
                    const location = data[0];
                    const address = location.address;
                    const country = (address.country || "").toLowerCase();

                    if (country.includes("brasil") || country.includes("brazil")) {
                        document.getElementById("id_latitude").value = location.lat;
                        document.getElementById("id_longitude").value = location.lon;
                        document.getElementById("id_country_name").value = "Brasil";
                        statusDiv.textContent = "✅ Localização encontrada com sucesso!";
                        submitButton.disabled = false; // habilita o botão
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
    return frase.split(" ").map(function (palavra) {
        return palavra.charAt(0).toUpperCase() + palavra.slice(1);
    }).join(" ");
}

let debounceTimer;

document.addEventListener("DOMContentLoaded", function () {
    const cityInput = document.getElementById("id_city_name");
    const stateInput = document.getElementById("id_state_name");
    const submitButton = document.getElementById("submit-button");
    // const btnText = submitButton.querySelector(".btn-text");
    // const btnSpinner = submitButton.querySelector(".btn-spinner");
    // const form = document.querySelector("form");

    let debounceTimer;

    function handleInputChange() {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(fetchGeolocation, 1000);
    }

    cityInput.addEventListener("input", handleInputChange);
    stateInput.addEventListener("input", handleInputChange);
});