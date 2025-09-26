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
    console.log('=',overlay.style.display);
    if (overlay.style.display === 'flex') {
        overlay.style.display = 'none';
    } else {
        overlay.style.display = 'flex';

        setTimeout(() => {
          overlay.style.display = "none";
        }, 700);
    }
});
