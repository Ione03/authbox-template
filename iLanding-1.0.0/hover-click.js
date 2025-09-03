// Create a tooltip element
// 2025 Agustus 30
// Authbox.web.id

// function refresh_mode(element_id, modal_title, modal_code, modal_type, tooltip) {
//     const m_object = document.getElementById("main-1");
//     m_object.innerHTML = '<span data-modal-code="bi-icon-70" data-modal-title="bi-arrow-up-short" data-modal-type="icon" data-tooltip="Link ini hanya tampil di mode edit. Silahkan klik untuk mengedit data!">TEST 123</span>'    
// };

document.addEventListener("DOMContentLoaded", () => {
    // Hover
    const tooltip = document.getElementById('custom-tooltip');
    const hoverables = document.querySelectorAll('.hoverable');

    // Modal
    const modal = new bootstrap.Modal(document.getElementById('myModal'));
    // const modal = document.getElementById('myModal');
    // const modalTitle = document.getElementById('modalTitle');
    // const modalCode = document.getElementById('modalCode');
    // const modalType = document.getElementById('modalType');
    // const closeBtn = document.querySelector('.close');
    // const infoForm = document.getElementById('infoForm');

    // $('#infoModal').on('shown.bs.modal', function () {
    //     $(this).find('input:visible:first').focus();
    // });
    

    // Track mouse movement for tooltip
    document.addEventListener('mousemove', (e) => {
        // console.log('Mouse moved:', e.pageX, e.pageY);
        if (tooltip.classList.contains('visible')) {
            tooltip.style.left = (e.pageX + 15) + 'px';
            tooltip.style.top = (e.pageY + 15) + 'px';
        }
    });

    // Tooltip functionality
    hoverables.forEach(element => {
        // Mouse enter - show tooltip
        element.addEventListener('mouseenter', (e) => {
            // console.log('Mouse entered:', e.target);
            const text = element.getAttribute('data-tooltip');
            tooltip.textContent = text;
            tooltip.classList.add('visible');
            tooltip.style.left = (e.pageX + 15) + 'px';
            tooltip.style.top = (e.pageY + 15) + 'px';
        });

        // Mouse leave - hide tooltip
        element.addEventListener('mouseleave', () => {
            tooltip.classList.remove('visible');
        });

        // Click - open modal
        element.addEventListener('click', (e) => {
            e.stopPropagation();
            // console.log('Element clicked:', e.target);
            // If you want to use the modal, uncomment the following lines
            // const modal = new bootstrap.Modal(document.getElementById('myModal'));
            // const title = element.getAttribute('data-modal-title') || 'Information Form';
            // const code = element.getAttribute('data-modal-code') || 'main-0';
            // const type = element.getAttribute('data-modal-type') || 'text';
            // modalTitle.textContent = title;
            // // modalCode.textContent = code;
            // modalType.value = type;
            // modalCode.value = code;
            // openModal();
            modal.show();
        });
    });

    // Modal functions
    // function openModal() {
    //     modal.classList.add('show');
    //     document.body.style.overflow = 'hidden';
    //     tooltip.classList.remove('visible');
    // }

    // function closeModal() {
    //     modal.classList.remove('show');
    //     document.body.style.overflow = '';
    // }

    // Close modal events
    // closeBtn.addEventListener('click', closeModal);

    // window.addEventListener('click', (e) => {
    //     if (e.target === modal) {
    //         closeModal();
    //     }
    //     tooltip.classList.remove('visible');
    // });

    // document.addEventListener('keydown', (e) => {
    //     if (e.key === 'Escape') {
    //         closeModal();
    //     }
    // });

    // Form submission
    // infoForm.addEventListener('submit', (e) => {
    //     e.preventDefault();
        
    //     const formData = {
    //         name: document.getElementById('name').value,
    //         email: document.getElementById('email').value,
    //         message: document.getElementById('message').value,
    //         topic: modalTitle.textContent
    //     };
        
    //     console.log('Form submitted:', formData);
    //     alert(`Thank you, ${formData.name}! Your information about "${formData.topic}" has been submitted.`);
        
    //     // Reset form and close modal
    //     infoForm.reset();
    //     closeModal();
    // });

    // Hide tooltip on click anywhere
    // document.addEventListener('click', () => {
    //     tooltip.classList.remove('visible');
    // });

});
