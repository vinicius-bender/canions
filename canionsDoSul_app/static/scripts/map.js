const map = L.map('map').setView([-30.0, -51.0], 6); // Região Sul

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  let marker;

  function buscarLocalizacao(lat, lng) {
    const url = `https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}&accept-language=pt-BR`;

    $.getJSON(url, function(data) {
      const address = data.address;
      $('#id_city_name').val(address.city || address.town || address.village || '');
      $('#id_state_name').val(address.state || '');
      $('#id_country_name').val(address.country || 'Brasil');
    });
  }

  map.on('click', function(e) {
    const lat = e.latlng.lat.toFixed(8);
    const lng = e.latlng.lng.toFixed(8);

    // Atualiza inputs
    $('#id_latitude').val(lat);
    $('#id_longitude').val(lng);

    // Adiciona marcador
    if (marker) map.removeLayer(marker);
    marker = L.marker([lat, lng]).addTo(map);

    buscarLocalizacao(lat, lng);
  });

  // Quando o botão for clicado, busca localização a partir dos inputs
  $('#btn_buscar_localizacao').click(function() {
    const lat = $('#id_latitude').val();
    const lng = $('#id_longitude').val();

    if (lat && lng) {
      // Move o marcador
      if (marker) map.removeLayer(marker);
      marker = L.marker([lat, lng]).addTo(map);
      map.setView([lat, lng], 12);
      buscarLocalizacao(lat, lng);
    } else {
      alert('Preencha latitude e longitude.');
    }
  });