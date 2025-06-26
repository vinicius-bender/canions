function animateCount(id, endValue, duration = 2000) {
    const element = document.getElementById(id);
    if (!element) return;

    let start = 0;
    const stepTime = Math.max(Math.floor(duration / endValue), 20);

    const step = () => {
        start++;
        element.textContent = start;
        if (start < endValue) {
            setTimeout(step, stepTime);
        }
    };
    step();
}

function closeAnonAlert() {
    const alertBox = document.getElementById('anonAlert');
    if (alertBox) {
        alertBox.style.transition = 'opacity 0.4s ease';
        alertBox.style.opacity = '0';
        setTimeout(() => {
            alertBox.style.display = 'none';
        }, 400);
    }
}

function initMap() {
    const mapContainer = document.getElementById('map');
    //if (!mapContainer || typeof observations === 'undefined' || !Array.isArray(observations)) return;
    if (!mapContainer) return;

    const map = L.map('map').setView([-28.73, -50.82], 7);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    observations.forEach(obs => {
        const marker = L.marker([obs.latitude, obs.longitude]).addTo(map);
        marker.on('click', () => {
            document.getElementById('modalSpecies').textContent = obs.species_name;
            document.getElementById('modalInfo').textContent = `Local: ${obs.city}, ${obs.state}`;
            document.getElementById('modalLink').href = `/observacao/${obs.id}/`;
            document.getElementById('mapModal').style.display = 'block';
        });
    });

    observations.forEach(obs => {
        const marker = L.marker([obs.latitude, obs.longitude]).addTo(map);

        marker.bindPopup(`
            <div class="popup-content">
                <h3>${obs.species_name}</h3>
                <p>Local: ${obs.city}, ${obs.state}</p>
                <a href="/observacoes/${obs.id}/" target="_blank" class="button-link">Ver mais detalhes</a>
            </div>
        `);
    });
}

// Animação de entrada ao scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animate');
        }
    });
}, observerOptions);

// Observar todos os steps
document.querySelectorAll('.flow-step').forEach(step => {
    observer.observe(step);
});

// Animação sequencial dos steps
let delay = 0;
document.querySelectorAll('.flow-step').forEach(step => {
    step.style.transitionDelay = delay + 's';
    delay += 0.2;
});



// Hover effect nos cards
document.querySelectorAll('.flow-step').forEach(card => {
    card.addEventListener('mouseenter', () => {
        card.style.transform = 'translateY(-10px) scale(1.02)';
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'translateY(0) scale(1)';
    });
});

window.addEventListener("DOMContentLoaded", function () {
    animateCount("count-species", parseInt(document.getElementById("count-species")?.dataset.value || 0));
    animateCount("count-records", parseInt(document.getElementById("count-records")?.dataset.value || 0));
    animateCount("count-approved", parseInt(document.getElementById("count-approved")?.dataset.value || 0));

    const closeBtn = document.querySelector(".close-alert");
    if (closeBtn) closeBtn.addEventListener("click", closeAnonAlert);

    initMap();
});