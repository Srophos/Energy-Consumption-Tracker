// Energy Tracker JavaScript

// Auto-hide flash messages after 5 seconds
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash');
    
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.transition = 'opacity 0.5s';
            message.style.opacity = '0';
            setTimeout(function() {
                message.style.display = 'none';
            }, 500);
        }, 5000);
    });
});

// Calculate energy in real-time on the form
const powerInput = document.getElementById('power_watts');
const hoursInput = document.getElementById('hours_used');

if (powerInput && hoursInput) {
    function calculateEnergy() {
        const power = parseFloat(powerInput.value) || 0;
        const hours = parseFloat(hoursInput.value) || 0;
        const energy = (power * hours) / 1000;
        
        // You can add a live preview element here if needed
        console.log(`Estimated energy: ${energy.toFixed(2)} kWh`);
    }
    
    powerInput.addEventListener('input', calculateEnergy);
    hoursInput.addEventListener('input', calculateEnergy);
}

// Form validation
const forms = document.querySelectorAll('form');

forms.forEach(function(form) {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(function(field) {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#ef4444';
            } else {
                field.style.borderColor = '#e2e8f0';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            alert('Please fill in all required fields');
        }
    });
});

// Set max date to today for date inputs
const dateInputs = document.querySelectorAll('input[type="date"]');
const today = new Date().toISOString().split('T')[0];

dateInputs.forEach(function(input) {
    if (!input.hasAttribute('max')) {
        input.setAttribute('max', today);
    }
});
