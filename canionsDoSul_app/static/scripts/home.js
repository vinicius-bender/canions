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

window.addEventListener("DOMContentLoaded", function () {
    // Os valores reais são inseridos dinamicamente no HTML (data-* attributes)
    animateCount("count-species", parseInt(document.getElementById("count-species").dataset.value));
    animateCount("count-records", parseInt(document.getElementById("count-records").dataset.value));
    animateCount("count-approved", parseInt(document.getElementById("count-approved").dataset.value));
});