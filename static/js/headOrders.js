const headSalade= document.querySelector('.salade-head');
const headSandwich= document.querySelector('.sandwich-head');
const headviennoiseries= document.querySelector('.viennoiseries-head');

headSalade.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-orders-salade';
});
headSandwich.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-orders-sandwich';
});
headviennoiseries.addEventListener('click', () => {
    window.location.href = 'http://127.0.0.1:5000/main-orders-viennoiseries';
});