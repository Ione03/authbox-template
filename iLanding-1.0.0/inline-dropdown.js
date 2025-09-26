document.addEventListener("DOMContentLoaded", () => {

    // Mobile-friendly dropdown toggle
    document.querySelectorAll('.hover-dropdown').forEach(dropdown => {
        const content = dropdown.querySelector('.dropdown-content');
        let isTouchDevice = 'ontouchstart' in window;
        
        if (isTouchDevice) {
            // For touch devices, use click events
            dropdown.addEventListener('click', function(e) {
                e.stopPropagation();
                const allDropdowns = document.querySelectorAll('.dropdown-content');
                allDropdowns.forEach(dd => {
                    if (dd !== content) dd.style.display = 'none';
                });
                
                if (content.style.display === 'block') {
                    content.style.display = 'none';
                } else {
                    content.style.display = 'block';
                    content.style.opacity = '1';
                    content.style.transform = 'translateY(0)';
                }
            });
        } else {
            // For non-touch devices, keep hover behavior
            dropdown.addEventListener('mouseenter', () => {
                content.style.display = 'block';
                content.style.opacity = '0';
                content.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    content.style.opacity = '1';
                    content.style.transform = 'translateY(0)';
                }, 10);
            });
            
            dropdown.addEventListener('mouseleave', () => {
                content.style.opacity = '0';
                content.style.transform = 'translateY(-10px)';
                
                setTimeout(() => {
                    content.style.display = 'none';
                }, 300);
            });
        }
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.hover-dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(content => {
                content.style.display = 'none';
            });
        }
    });

});