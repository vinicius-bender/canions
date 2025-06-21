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
      const address = data.address;
      document.getElementById('id_city_name').value = address.city || address.town || address.village || '';
      document.getElementById('id_state_name').value = address.state || '';
      document.getElementById('id_country_name').value = address.country || 'Brasil';
    })
    .catch(error => {
      console.error('Erro ao buscar localização:', error);
    });
}

map.on('click', function(e) {
  const lat = e.latlng.lat.toFixed(8);
  const lng = e.latlng.lng.toFixed(8);

  document.getElementById('id_latitude').value = lat;
  document.getElementById('id_longitude').value = lng;

  if (marker) map.removeLayer(marker);
  marker = L.marker([lat, lng]).addTo(map);

  buscarLocalizacao(lat, lng);
});

document.getElementById('btn_buscar_localizacao').addEventListener('click', function() {
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