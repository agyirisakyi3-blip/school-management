document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (typeof bootstrap !== 'undefined') {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
    
    // Initialize all dropdowns
    const dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
    dropdownElementList.forEach(function (dropdownToggleEl) {
        new bootstrap.Dropdown(dropdownToggleEl);
    });
    
    // Mobile sidebar toggle
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (window.innerWidth < 768) {
        sidebar?.classList.add('show');
    }
    
    // Confirm delete
    window.confirmDelete = function(message) {
        return confirm(message || 'Are you sure you want to delete this item?');
    };
    
    // Print function
    window.printReport = function() {
        window.print();
    };
    
    // Add loading state to forms
    const forms = document.querySelectorAll('form[data-loading]');
    forms.forEach(function(form) {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });
    
    // Table row hover effect
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('click', function() {
            const link = row.querySelector('a.btn');
            if (link) {
                window.location.href = link.href;
            }
        });
        row.style.cursor = 'pointer';
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-fill search from URL params
    const urlParams = new URLSearchParams(window.location.search);
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput && urlParams.has('search')) {
        searchInput.value = urlParams.get('search');
    }
    
    // Smooth scroll to anchors
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
});
