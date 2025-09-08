// swiper-init.js
document.addEventListener('DOMContentLoaded', function() {
    const swiperConfig = {
        loop: true,
        speed: 600,
        autoplay: {
            delay: 5000
        },
        slidesPerView: "auto",
        pagination: {
            el: ".swiper-pagination",
            type: "bullets",
            clickable: true
        },
        breakpoints: {
            320: {
                slidesPerView: 2,
                spaceBetween: 40
            },
            480: {
                slidesPerView: 3,
                spaceBetween: 60
            },
            640: {
                slidesPerView: 4,
                spaceBetween: 80
            },
            992: {
                slidesPerView: 6,
                spaceBetween: 120
            }
        }
    };

    // Initialize all swipers with class 'init-swiper'
    const swipers = document.querySelectorAll('.init-swiper');
    
    swipers.forEach(swiperElement => {
        new Swiper(swiperElement, swiperConfig);
    });
});