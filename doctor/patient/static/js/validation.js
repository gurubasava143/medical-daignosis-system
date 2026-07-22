// validation.js - Centralized client‑side validation

// This script attaches a submit handler to every form on the page.
// It relies on HTML5 validation attributes (required, type, pattern, min, max).
// When a form is invalid, it prevents submission and shows a Bootstrap‑styled alert.

document.addEventListener('DOMContentLoaded', function () {
  const forms = document.querySelectorAll('form');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      // Reset previous alerts
      const existingAlert = form.querySelector('.validation-alert');
      if (existingAlert) existingAlert.remove();

      if (!form.checkValidity()) {
        e.preventDefault();
        e.stopPropagation();

        // Find the first invalid element
        const firstInvalid = form.querySelector(':invalid');
        const message = firstInvalid && firstInvalid.validationMessage ? firstInvalid.validationMessage : 'Please fill out this field correctly.';

        // Insert alert element at the top of the form
        const alertDiv = document.createElement('div');
        alertDiv.className = 'alert alert-danger validation-alert';
        alertDiv.role = 'alert';
        alertDiv.textContent = message;
        form.prepend(alertDiv);

        // Focus the invalid element
        firstInvalid.focus();
      } else {
        // Optionally, you can add a success indicator here
        form.classList.add('was-validated');
      }
    });
  });
});
