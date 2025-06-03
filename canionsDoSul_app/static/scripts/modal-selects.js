function inicializarSelects() {
  const familySelect = document.getElementById('id_family');
  const genusSelect = document.getElementById('id_genus');
  const speciesSelect = document.getElementById('id_species');

  if (familySelect && genusSelect) {
    familySelect.addEventListener('change', function () {
      const familyId = this.value;
      genusSelect.innerHTML = '<option value="">---------</option>';
      speciesSelect.innerHTML = '<option value="">---------</option>';

      if (familyId) {
        fetch(`/buscar-generos/${familyId}/`)
          .then(response => response.json())
          .then(data => {
            data.generos.forEach(function (genus) {
              const option = document.createElement('option');
              option.value = genus.id;
              option.textContent = genus.name;
              genusSelect.appendChild(option);
            });
          });
      }
    });

    genusSelect.addEventListener('change', function () {
      const genusId = this.value;
      speciesSelect.innerHTML = '<option value="">---------</option>';

      if (genusId) {
        fetch(`/buscar-especies/${genusId}/`)
          .then(response => response.json())
          .then(data => {
            data.especies.forEach(function (specie) {
              const option = document.createElement('option');
              option.value = specie.id;
              option.textContent = specie.scientific_name;
              speciesSelect.appendChild(option);
            });
          });
      }
    });
  }
}