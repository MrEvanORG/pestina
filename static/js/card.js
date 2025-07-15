function toggleDetails(button) {
    const card = button.closest('.product-card');
    const detailsContent = card.querySelector('.details-content');
    const ribens = card.querySelector('.ribbon-container');

    // بستن همه‌ی کارت‌ها و ریست دکمه‌ها
    document.querySelectorAll('.product-card').forEach(otherCard => {
        const otherDetails = otherCard.querySelector('.details-content');
        const otherRibbon = otherCard.querySelector('.ribbon-container');
        const otherButton = otherCard.querySelector('.details-btn');

        if (otherDetails !== detailsContent) {
            otherDetails.classList.remove('active');
        }
        if (otherRibbon !== ribens) {
            otherRibbon.classList.remove('active');
        }
        if (otherButton !== button) {
            otherButton.textContent = 'جزئیات ▼';
        }
    });

    // تغییر وضعیت کارت فعلی
    detailsContent.classList.toggle('active');
    ribens.classList.toggle('active');

    // متن دکمه فعلی
    if (detailsContent.classList.contains('active')) {
        button.textContent = '➜';
    } else {
        button.textContent = 'جزئیات ▼';
    }
}