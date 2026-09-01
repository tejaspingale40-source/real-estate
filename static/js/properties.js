// PROPERTIES JAVASCRIPT FILE

document.addEventListener('DOMContentLoaded', () => {
    // Quick search input clear button handler
    const searchInputs = document.querySelectorAll('input[name="q"]');
    searchInputs.forEach(input => {
        input.addEventListener('keyup', (e) => {
            if (e.key === 'Escape') {
                input.value = '';
            }
        });
    });
});
