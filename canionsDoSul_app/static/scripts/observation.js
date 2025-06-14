document.addEventListener("DOMContentLoaded", function () {
    const carousel = document.getElementById('carousel');
    const prevBtn = document.querySelector('.carousel-btn.prev');
    const nextBtn = document.querySelector('.carousel-btn.next');

    if (carousel && prevBtn && nextBtn) {
        const item = carousel.querySelector('.media-item');
        if (!item) return;

        const itemWidth = item.getBoundingClientRect().width;
        const gap = parseFloat(getComputedStyle(carousel).gap) || 0;

        function moveCarousel(direction) {
            const scrollAmount = direction * (itemWidth + gap);
            carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        }

        prevBtn.addEventListener('click', () => moveCarousel(-1));
        nextBtn.addEventListener('click', () => moveCarousel(1));
    }

    // Modal: imagem e vídeo
    const modal = document.getElementById("mediaModal");
    const modalImg = document.getElementById("modalImage");
    const modalVid = document.getElementById("modalVideo");
    const closeBtn = document.querySelector(".modal .close");

    // Imagem
    document.querySelectorAll(".media-item img").forEach(img => {
        img.addEventListener("click", function () {
            modal.style.display = "flex";
            modalImg.src = this.src;
            modalImg.style.display = "block";
            modalVid.style.display = "none";
            modalVid.pause();
        });
    });

    // Vídeo
    document.querySelectorAll(".media-item video").forEach(vid => {
    const container = vid.parentElement;
    container.addEventListener("click", function () {
        const source = vid.querySelector("source")?.src || vid.currentSrc;
        if (!source) return;

        modal.style.display = "flex";
        modalVid.src = source;
        modalVid.style.display = "block";
        modalImg.style.display = "none";
        modalVid.play();
    });
});

    closeBtn.addEventListener("click", function () {
        modal.style.display = "none";
        modalImg.src = "";
        modalVid.src = "";
        modalVid.pause();
    });

    modal.addEventListener("click", function (e) {
        if (e.target === modal) {
            modal.style.display = "none";
            modalImg.src = "";
            modalVid.src = "";
            modalVid.pause();
        }
    });
});