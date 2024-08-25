/*
    Filename: script.js
    Description: Adds a navbar class to the navbar when the page is scrolled down more than 50 pixels
    Author: Linhao Wang, Yuxiang Zou, Joshua Yu Xuan Soo
    Email: lwan0191@student.monash.edu, yzou0027@student.monash.edu, jsoo0027@student.monash.edu
    Date: 25/08/2024
*/

window.addEventListener('scroll', function () {
    var navbar = document.getElementById('navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});