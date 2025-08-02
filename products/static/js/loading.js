// document.addEventListener('DOMContentLoaded', function() {
//   const loaderWrapper = document.getElementById('loader-wrapper');
//   loaderWrapper.classList.add('hidden');
// });
window.addEventListener('load', function() {
     const loadingElement = document.getElementById('loader-wrapper');
     if (loadingElement) {
       loadingElement.classList.add('hidden')
     }
   });