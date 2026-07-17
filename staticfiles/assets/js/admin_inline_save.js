document.addEventListener('DOMContentLoaded', function () {
    const statusFields = document.querySelectorAll('select[name$="product_status"]');

    statusFields.forEach(function (field) {
        field.addEventListener('change', function () {
            const row = this.closest('tr');
            const form = row.closest('form');
            const saveButton = form.querySelector('input[name="_save"]');

            // Automatically trigger the save button
            if (saveButton) {
                saveButton.click();
            }
        });
    });
});
