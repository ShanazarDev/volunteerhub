// Custom JavaScript for VolunteerHub

document.addEventListener('DOMContentLoaded', function() {
    // Set up Bootstrap components
    setupBootstrapComponents();
    
    // Add form validation styling
    setupFormValidation();
    
    // Format datetime-local inputs with current values
    formatDateTimeInputs();
});

/**
 * Set up Bootstrap components like tooltips, popovers
 */
function setupBootstrapComponents() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

/**
 * Add custom styling to form validation
 */
function setupFormValidation() {
    // Add Bootstrap validation classes to form elements
    var forms = document.querySelectorAll('.needs-validation');
    
    Array.prototype.slice.call(forms).forEach(function (form) {
        form.addEventListener('submit', function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });
    
    // Style form controls
    var formControls = document.querySelectorAll('input, select, textarea');
    formControls.forEach(function(element) {
        if (!element.classList.contains('form-control') && 
            element.type !== 'radio' && 
            element.type !== 'checkbox' &&
            element.type !== 'hidden' &&
            element.type !== 'submit') {
            element.classList.add('form-control');
        }
    });
}

/**
 * Format datetime-local inputs with current values
 */
function formatDateTimeInputs() {
    var dateTimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    
    dateTimeInputs.forEach(function(input) {
        // If input has no value but has a default-value attribute
        if (!input.value && input.getAttribute('data-default-value')) {
            try {
                var defaultDate = new Date(input.getAttribute('data-default-value'));
                var year = defaultDate.getFullYear();
                var month = (defaultDate.getMonth() + 1).toString().padStart(2, '0');
                var day = defaultDate.getDate().toString().padStart(2, '0');
                var hours = defaultDate.getHours().toString().padStart(2, '0');
                var minutes = defaultDate.getMinutes().toString().padStart(2, '0');
                
                input.value = `${year}-${month}-${day}T${hours}:${minutes}`;
            } catch (e) {
                console.error('Error formatting date:', e);
            }
        }
    });
}

/**
 * Dynamic category filter for event list
 */
function filterEventsByCategory(categoryId) {
    // Get all event cards
    var eventCards = document.querySelectorAll('.event-card');
    
    // If "all" selected, show all events
    if (categoryId === 'all') {
        eventCards.forEach(function(card) {
            card.style.display = 'block';
        });
        return;
    }
    
    // Otherwise, filter by category
    eventCards.forEach(function(card) {
        var cardCategoryId = card.getAttribute('data-category');
        
        if (cardCategoryId === categoryId) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}
