document.addEventListener('DOMContentLoaded', function() {
    // عناصر اصلی
    const filterToggleBtn = document.querySelector('.filter-toggle-btn');
    const filterContainer = document.querySelector('.filter-container');
    
    // عناصر فیلتر
    const pestinaToggle = document.querySelector('input[name="is_pestina_product"]');
    const freeShippingToggle = document.querySelector('input[name="free_shipping"]');
    const kindSelect = document.getElementById('kind');
    const statusSelect = document.getElementById('status');
    const qualitySelect = document.getElementById('quality');
    const clearFiltersButton = document.querySelector('.clear-filters');
    const sortButtons = document.querySelectorAll('.sort-btn');
    
    // پارامترهای URL فعلی
    const urlParams = new URLSearchParams(window.location.search);
    
    // مقداردهی اولیه فیلترها از URL
    function initializeFiltersFromUrl() {
        if (urlParams.has('is_pestina_product')) {
            pestinaToggle.checked = urlParams.get('is_pestina_product') === 'true';
        }
        
        if (urlParams.has('free_shipping')) {
            freeShippingToggle.checked = urlParams.get('free_shipping') === 'true';
        }
        
        if (urlParams.has('kind')) {
            kindSelect.value = urlParams.get('kind');
        }
        
        if (urlParams.has('status')) {
            statusSelect.value = urlParams.get('status');
        }
        
        if (urlParams.has('quality')) {
            qualitySelect.value = urlParams.get('quality');
        }
        
        if (urlParams.has('sort')) {
            const sortValue = urlParams.get('sort');
            sortButtons.forEach(btn => {
                if (btn.dataset.sort === sortValue) {
                    btn.classList.add('active');
                }
            });
        }
    }
    
    initializeFiltersFromUrl();
    
    // تابع toggle فیلترها در موبایل
    if (filterToggleBtn) {
        filterToggleBtn.addEventListener('click', function() {
            const isExpanded = this.getAttribute('aria-expanded') === 'true';
            this.setAttribute('aria-expanded', !isExpanded);
            filterContainer.classList.toggle('open');
            
            // استفاده از انیمیشن همبرگر موجود
            this.classList.toggle('collapsed');
        });
    }
    
    // اعمال فیلترها هنگام تغییر
    [pestinaToggle, freeShippingToggle, kindSelect, statusSelect, qualitySelect].forEach(element => {
        element.addEventListener('change', applyFilters);
    });
    
    // مرتب‌سازی
    sortButtons.forEach(button => {
        button.addEventListener('click', function() {
            sortButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            applyFilters();
        });
    });
    
    // پاک کردن فیلترها
    clearFiltersButton.addEventListener('click', function() {
        pestinaToggle.checked = false;
        freeShippingToggle.checked = false;
        kindSelect.value = '';
        statusSelect.value = '';
        qualitySelect.value = '';
        sortButtons.forEach(btn => btn.classList.remove('active'));
        applyFilters();
    });
    
    // تابع اعمال فیلترها و مرتب‌سازی
    function applyFilters() {
        const params = new URLSearchParams();
        
        // افزودن فیلترها به پارامترها
        if (pestinaToggle.checked) {
            params.append('is_pestina_product', 'true');
        }
        
        if (freeShippingToggle.checked) {
            params.append('free_shipping', 'true');
        }
        
        if (kindSelect.value) {
            params.append('kind', kindSelect.value);
        }
        
        if (statusSelect.value) {
            params.append('status', statusSelect.value);
        }
        
        if (qualitySelect.value) {
            params.append('quality', qualitySelect.value);
        }
        
        // افزودن مرتب‌سازی
        const activeSortBtn = document.querySelector('.sort-btn.active');
        if (activeSortBtn) {
            params.append('sort', activeSortBtn.dataset.sort);
        }
        
        // نگه داشتن پارامتر صفحه‌بندی اگر وجود دارد
        if (urlParams.has('page')) {
            params.append('page', urlParams.get('page'));
        }
        
        // هدایت به URL جدید با پارامترهای فیلتر
        window.location.search = params.toString();
    }
});