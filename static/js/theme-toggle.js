document.addEventListener("DOMContentLoaded", function () {
    const themeButton = document.getElementById("themeButton");
    const themeSelectors = document.querySelectorAll(".theme-selector");
    const themeStylesheet = document.getElementById("themeStylesheet");

    const defaultTheme = themeStylesheet.getAttribute("href");
    const defaultThemeText = "تم روشن";

    // تابع برای اعمال تم ذخیره‌شده و عکس‌ها
    function applySavedTheme() {
        const savedTheme = localStorage.getItem("selectedTheme");
        const savedThemeText = localStorage.getItem("selectedThemeText");

        if (savedTheme) {
            themeStylesheet.setAttribute("href", savedTheme);
            themeButton.innerText = savedThemeText || defaultThemeText;

            updateImagesBasedOnTheme(savedTheme);
        }
    }

    // تابع برای آپدیت عکس‌ها بر اساس تم
    function updateImagesBasedOnTheme(themeHref) {
        const allImages = document.querySelectorAll('.themed-image');

        let themeKey = "light";  // پیش‌فرض

        if (themeHref.includes("dark-root")) {
            themeKey = "dark";
        } else if (themeHref.includes("light-root-2")) {
            themeKey = "light2";
        }

        allImages.forEach(img => {
            const newSrc = img.getAttribute(`data-${themeKey}`);
            if (newSrc) {
                img.setAttribute("src", newSrc);
            }
        });
    }

    applySavedTheme();

    themeSelectors.forEach(button => {
        button.addEventListener("click", function () {
            const selectedTheme = this.getAttribute("data-theme");
            const selectedThemeText = this.innerText;

            themeStylesheet.setAttribute("href", selectedTheme);
            themeButton.innerText = selectedThemeText;

            localStorage.setItem("selectedTheme", selectedTheme);
            localStorage.setItem("selectedThemeText", selectedThemeText);

            updateImagesBasedOnTheme(selectedTheme);
        });
    });
});
