// MAIN JAVASCRIPT FILE

document.addEventListener('DOMContentLoaded', () => {
    // 1. Mobile Menu Drawer Toggle
    const mobileToggle = document.getElementById('mobileToggle');
    const navMenu = document.getElementById('navMenu');

    if (mobileToggle && navMenu) {
        mobileToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
            mobileToggle.classList.toggle('active');
        });
    }



    // 3. Automatic Toast Message Auto-dismiss after 5 seconds
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.5s ease';
            setTimeout(() => toast.remove(), 500);
        }, 5000);
    });

    // 4. Home Loan EMI Calculator Handler
    const loanAmountRange = document.getElementById('loanAmountRange');
    const interestRateRange = document.getElementById('interestRateRange');
    const loanTenureRange = document.getElementById('loanTenureRange');

    const loanAmountText = document.getElementById('loanAmountText');
    const interestRateText = document.getElementById('interestRateText');
    const loanTenureText = document.getElementById('loanTenureText');

    const monthlyEmiVal = document.getElementById('monthlyEmiVal');
    const principalVal = document.getElementById('principalVal');
    const totalInterestVal = document.getElementById('totalInterestVal');
    const totalAmountVal = document.getElementById('totalAmountVal');

    const principalBar = document.getElementById('principalBar');
    const interestBar = document.getElementById('interestBar');

    function calculateEMI() {
        if (!loanAmountRange || !interestRateRange || !loanTenureRange) return;

        const principal = parseFloat(loanAmountRange.value);
        const annualRate = parseFloat(interestRateRange.value);
        const tenureYears = parseFloat(loanTenureRange.value);

        const monthlyRate = annualRate / (12 * 100);
        const totalMonths = tenureYears * 12;

        // EMI Formula: P * r * (1 + r)^n / ((1 + r)^n - 1)
        const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, totalMonths)) / (Math.pow(1 + monthlyRate, totalMonths) - 1);
        const totalAmount = emi * totalMonths;
        const totalInterest = totalAmount - principal;

        // Formatter for INR
        const formatINR = (val) => new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR', maximumFractionDigits: 0 }).format(val);

        if (loanAmountText) loanAmountText.innerText = formatINR(principal);
        if (interestRateText) interestRateText.innerText = annualRate + '%';
        if (loanTenureText) loanTenureText.innerText = tenureYears + (tenureYears === 1 ? ' Year' : ' Years');

        if (monthlyEmiVal) monthlyEmiVal.innerText = formatINR(emi);
        if (principalVal) principalVal.innerText = formatINR(principal);
        if (totalInterestVal) totalInterestVal.innerText = formatINR(totalInterest);
        if (totalAmountVal) totalAmountVal.innerText = formatINR(totalAmount);

        // Calculate ratios for visual breakdown bar
        const principalPercentage = Math.round((principal / totalAmount) * 100);
        const interestPercentage = 100 - principalPercentage;

        if (principalBar) principalBar.style.width = principalPercentage + '%';
        if (interestBar) interestBar.style.width = interestPercentage + '%';
    }

    if (loanAmountRange && interestRateRange && loanTenureRange) {
        loanAmountRange.addEventListener('input', calculateEMI);
        interestRateRange.addEventListener('input', calculateEMI);
        loanTenureRange.addEventListener('input', calculateEMI);

        // Initial Calculation
        calculateEMI();
    }

    // 5. Scroll-Triggered Enquiry Popup Modal Handler
    const scrollModalEl = document.getElementById('scrollEnquiryModal');
    if (scrollModalEl && typeof bootstrap !== 'undefined') {
        const enquiryModal = new bootstrap.Modal(scrollModalEl);
        let hasShownModal = sessionStorage.getItem('enquiryModalShown') === 'true';
        let scrollCount = 0;
        let lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;

        function checkScrollTrigger() {
            if (hasShownModal) return;

            const st = window.pageYOffset || document.documentElement.scrollTop;
            const viewportHeight = window.innerHeight;
            
            // Detect significant scroll movements (approx 2-3 scroll wheels / swipe distance, i.e. 500px+)
            if (st > 500 || Math.abs(st - lastScrollTop) > 300) {
                scrollCount++;
                if (st > 600) {
                    enquiryModal.show();
                    hasShownModal = true;
                    sessionStorage.setItem('enquiryModalShown', 'true');
                    window.removeEventListener('scroll', checkScrollTrigger);
                }
            }
            lastScrollTop = st <= 0 ? 0 : st;
        }

        window.addEventListener('scroll', checkScrollTrigger, { passive: true });
    }

});

