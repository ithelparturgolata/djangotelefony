// record-checkbox.js

document.addEventListener('DOMContentLoaded', function() {
    // Select all checkboxes with the class 'record-checkbox'
    var checkboxes = document.querySelectorAll('.record-checkbox');

    // Add event listener to each checkbox
    checkboxes.forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            // If checkbox is checked, append its value to the phone input
            if (this.checked) {
                appendPhoneNumber(this.value);
            } else {
                removePhoneNumber(this.value);
            }
        });
    });

    // Function to append phone number to the phone input
    function appendPhoneNumber(phoneNumber) {
        var phoneInput = document.getElementById('phone');
        var currentPhoneNumbers = phoneInput.value.split(',').map(function(number) {
            return number.trim();
        });

        // Add phone number if not already present
        if (!currentPhoneNumbers.includes(phoneNumber)) {
            currentPhoneNumbers.push(phoneNumber);
            phoneInput.value = currentPhoneNumbers.join(', ');
        }
    }

    // Function to remove phone number from the phone input
    function removePhoneNumber(phoneNumber) {
        var phoneInput = document.getElementById('phone');
        var currentPhoneNumbers = phoneInput.value.split(',').map(function(number) {
            return number.trim();
        });

        // Remove phone number if present
        var index = currentPhoneNumbers.indexOf(phoneNumber);
        if (index !== -1) {
            currentPhoneNumbers.splice(index, 1);
            phoneInput.value = currentPhoneNumbers.join(', ');
        }
    }
});
