const headSalade= document.querySelector('.salade-head');
const headSandwich= document.querySelector('.sandwich-head');
const headVanoiserie= document.querySelector('.vanoiserie-head');

headSalade.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-salade';
});
headSandwich.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-sandwich';
});
headVanoiserie.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-vanoiserie';
});