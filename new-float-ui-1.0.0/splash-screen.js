// Function to fade out the overlay
function fadeOutOverlay(overlay, duration = 1300) {
    overlay.style.transition = `opacity ${duration}ms ease-out`;
    overlay.style.opacity = '0';
    
    // Hide the overlay after the transition completes
    setTimeout(() => {
        overlay.style.display = 'none';
    }, duration);
};

// Function to show the overlay
function showOverlay(overlay) {
    overlay.style.display = 'flex';
    // Trigger reflow to ensure transition works
    void overlay.offsetWidth;
    overlay.style.opacity = '1';
};

document.addEventListener("DOMContentLoaded", () => {
  // var pageLoading = document.querySelector(".page-loading");

  // if (pageLoading) {
  //   window.addEventListener("load", () => {
  //     pageLoading.classList.add("hide");

  //     setTimeout(() => {
  //       pageLoading.style.display = "none";
  //     }, 1000);
  //   });
  // }
  const overlay = document.getElementById('loadingOverlay');
  // // console.log('=',overlay.style.display);
  // if (overlay.style.display === 'flex') {
  //     overlay.style.display = 'none';
  // } else {
  //     // overlay.style.display = 'flex';

  //     setTimeout(() => {
  //       // overlay.style.display = "none";
  //       overlay.style.transition = `opacity ${duration}ms ease-out`;
  //       overlay.style.opacity = '0';

  //     }, 1000);
  // };

  showOverlay(overlay);
  fadeOutOverlay(overlay);

});
