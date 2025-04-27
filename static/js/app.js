// Task Master - Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Format dates to local format
    const formatDates = () => {
        const dateElements = document.querySelectorAll('.format-date');
        dateElements.forEach(element => {
            const dateString = element.getAttribute('data-date');
            if (dateString) {
                const date = new Date(dateString);
                element.textContent = date.toLocaleDateString();
            }
        });
    };
    
    // Initialize tooltips
    const initTooltips = () => {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    };
    
    // Toggle completed tasks visibility
    const setupToggleCompleted = () => {
        const toggleBtn = document.getElementById('toggleCompletedBtn');
        const todoItems = document.querySelectorAll('.todo-completed');
        let isHidden = false;
        
        if (toggleBtn) {
            toggleBtn.addEventListener('click', function() {
                isHidden = !isHidden;
                todoItems.forEach(item => {
                    item.style.display = isHidden ? 'none' : '';
                });
                
                toggleBtn.innerHTML = isHidden ? 
                    '<i class="fas fa-eye"></i> Show Completed' : 
                    '<i class="fas fa-eye-slash"></i> Hide Completed';
            });
        }
    };

    // Setup task filtering
    const setupTaskFiltering = () => {
        const filterSelect = document.getElementById('priorityFilter');
        if (filterSelect) {
            filterSelect.addEventListener('change', function() {
                const value = this.value;
                const todoItems = document.querySelectorAll('.todo-item');
                
                todoItems.forEach(item => {
                    if (value === 'all') {
                        item.style.display = '';
                    } else if (value === 'high' && !item.classList.contains('priority-high')) {
                        item.style.display = 'none';
                    } else if (value === 'medium' && !item.classList.contains('priority-medium')) {
                        item.style.display = 'none';
                    } else if (value === 'low' && !item.classList.contains('priority-low')) {
                        item.style.display = 'none';
                    } else {
                        item.style.display = '';
                    }
                });
            });
        }
    };

    // Setup datetime picker for the reminder and due date fields
    const setupDateTimePickers = () => {
        const dateTimeInputs = document.querySelectorAll('.datetimepicker');
        if (dateTimeInputs.length > 0) {
            dateTimeInputs.forEach(input => {
                // If using a datetime picker library, initialize it here
                // This is a placeholder for when a datetime picker is added
                console.log('Datetime picker initialized for', input.id);
            });
        }
    };

    // Initialize all functionality
    formatDates();
    initTooltips();
    setupToggleCompleted();
    setupTaskFiltering();
    setupDateTimePickers();
});