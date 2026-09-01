// FILTERS JAVASCRIPT FILE

document.addEventListener('DOMContentLoaded', () => {
    const filterForm = document.getElementById('filterForm');
    if (filterForm) {
        // Auto-submit filter form on select change if desired
        const selects = filterForm.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', () => {
                filterForm.submit();
            });
        });
    }
});
