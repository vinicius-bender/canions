// function fetchGeolocation() {
//     const city = document.getElementById("id_city_name").value;
//     const state = document.getElementById("id_state_name").value;
//     const statusDiv = document.getElementById("location-status");

//     if (city && state) {
//       statusDiv.textContent = "Buscando localização...";

//       const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=Brasil&format=json&addressdetails=1`;

//       fetch(url)
//         .then(response => response.json())
//         .then(data => {
//           if (data && data.length > 0) {
//             const location = data[0];
//             const address = location.address;

//             if (address && address.country && address.country.toLowerCase().includes("brazil")) {
//               document.getElementById("id_latitude").value = location.lat;
//               document.getElementById("id_longitude").value = location.lon;
//               document.getElementById("id_country_name").value = "Brasil";
//               statusDiv.textContent = "Localização encontrada com sucesso!";
//             } else {
//               alert("A cidade/estado informados não pertencem ao Brasil. Por favor, verifique.");
//               document.getElementById("id_latitude").value = "";
//               document.getElementById("id_longitude").value = "";
//               document.getElementById("id_country_name").value = "";
//               statusDiv.textContent = "";
//             }
//           } else {
//             alert("Localização não encontrada. Verifique se o nome da cidade e do estado estão corretos.");
//             statusDiv.textContent = "";
//           }
//         })
//         .catch(error => {
//           console.error("Erro ao buscar a geolocalização:", error);
//           alert("Erro ao buscar a geolocalização.");
//           statusDiv.textContent = "";
//         });
//     }
// }

// document.addEventListener("DOMContentLoaded", function () {
//     document.getElementById("id_state_name").addEventListener("blur", fetchGeolocation);
// });


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

document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("id_state_name").addEventListener("blur", fetchGeolocation);
});

function primeiraLetraDeCadaPalavraMaiuscula(frase) {
  return frase.split(" ").map(function(palavra) {
    return palavra.charAt(0).toUpperCase() + palavra.slice(1);
  }).join(" ");
}

// function fetchGeolocation() {
//     const city = document.getElementById("id_city_name").value;
//     const state = document.getElementById("id_state_name").value;

//     if (city && state) {
//       const url = `https://nominatim.openstreetmap.org/search?city=${encodeURIComponent(city)}&state=${encodeURIComponent(state)}&country=Brasil&format=json`;

//       fetch(url)
//         .then(response => response.json())
//         .then(data => {
//           if (data && data.length > 0) {
//             const location = data[0];
//             document.getElementById("id_latitude").value = location.lat;
//             document.getElementById("id_longitude").value = location.lon;
//             document.getElementById("id_country_name").value = "Brasil";  // ou location.display_name se quiser o nome completo
//           } else {
//             alert("Localização não encontrada. Verifique os nomes da cidade e estado.");
//           }
//         })
//         .catch(error => {
//           console.error("Erro ao buscar a geolocalização:", error);
//           alert("Erro ao buscar a geolocalização.");
//         });
//     }
//   }

//   document.addEventListener("DOMContentLoaded", function () {
//     // Quando o usuário sair do campo de estado, tenta buscar os dados
//     document.getElementById("id_state_name").addEventListener("blur", fetchGeolocation);
//   });