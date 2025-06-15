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

window.addEventListener("DOMContentLoaded", function () {
    animateCount("count-species", parseInt(document.getElementById("count-species").dataset.value));
    animateCount("count-records", parseInt(document.getElementById("count-records").dataset.value));
    animateCount("count-approved", parseInt(document.getElementById("count-approved").dataset.value));

    const closeBtn = document.querySelector(".close-alert");
    if (closeBtn) {
        closeBtn.addEventListener("click", closeAnonAlert);
    }
});