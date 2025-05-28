document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("user-search");
    const select = document.getElementById("user");
    const roleLabel = document.getElementById("role-label");

    input.addEventListener("input", function () {
        const filter = input.value.toLowerCase();
        let found = false;

        for (let option of select.options) {
            const text = option.text.toLowerCase();
            if (text.includes(filter)) {
                option.style.display = "";
                found = true;
            } else {
                option.style.display = "none";
            }
        }

        if (filter.length > 0 && found) {
            select.style.display = "block";
        } else {
            select.style.display = "none";
        }
    });

    select.addEventListener("change", function () {
        const selectedOption = select.options[select.selectedIndex];
        const username = selectedOption.text.split(" (")[0]; // pega apenas o nome

        // Coloca o nome selecionado no campo de busca
        input.value = username;

        // Atualiza o label do cargo
        // roleLabel.textContent = `Promover ${username} para:`;
        const usernameInBold = `<strong>${username}</strong>`;
        
        // Atualiza o label do cargo com o nome em negrito
        roleLabel.innerHTML = `Promover ${usernameInBold} para:`;

        // Oculta o select
        select.style.display = "none";
    });
});