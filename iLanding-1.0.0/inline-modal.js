document.addEventListener("DOMContentLoaded", () => {
  
    // Modal functionality
    const modal = document.getElementById("myModal");
    const modalTriggers = document.querySelectorAll(".modal-trigger");
    const closeBtns = document.querySelectorAll(".close-btn");

    // Open modal
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            const userUUID = this.getAttribute('data-user-uuid');
            const userType = this.getAttribute('data-user-type');
            console.log('USER-ID', userUUID, userType);

            e.preventDefault();
            modal.style.display = "flex";
            document.addEventListener("keydown", handleKeyDown);
        });
    });

    // Close modal
    function closeModal() {
        modal.style.display = "none";
        document.removeEventListener("keydown", handleKeyDown);
    };

    // ESC key handler
    function handleKeyDown(event) {
        if (event.key === "Escape") {
            closeModal();
        }
    };

    // Close modal when clicking close buttons
    closeBtns.forEach(btn => {
        btn.addEventListener('click', closeModal);
    });

    // Close modal when clicking outside content
    modal.addEventListener("click", function(event) {
        if (event.target === modal) {
            closeModal();
        }
    });

});