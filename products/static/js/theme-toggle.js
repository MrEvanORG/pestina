document.addEventListener("DOMContentLoaded", function () {
    const themeButton = document.getElementById("themeButton");
    const themeSelectors = document.querySelectorAll(".theme-selector");
    const themeStylesheet = document.getElementById("themeStylesheet");

    const defaultTheme = themeStylesheet.getAttribute("href");
    const defaultThemeText = "تم روشن";

    function applySavedTheme() {
        const savedTheme = localStorage.getItem("selectedTheme");
        const savedThemeText = localStorage.getItem("selectedThemeText");

        if (savedTheme) {
            themeStylesheet.setAttribute("href", savedTheme);
            themeButton.innerText = savedThemeText || defaultThemeText;
        }
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
        });
    });
});