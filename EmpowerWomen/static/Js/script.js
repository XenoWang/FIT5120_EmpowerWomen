// Show/hide the Back to Top button
window.onscroll = function() {
    const backToTop = document.getElementById("backToTop");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTop.style.display = "block";
    } else {
        backToTop.style.display = "none";
    }
};

// Click the "Back to Top" button and scroll smoothly to the top
document.getElementById("backToTop").addEventListener("click", function(event) {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

document.getElementById('search-button').addEventListener('click', function() {
    const query = document.getElementById('search-input').value;

    if (query.trim() !== '') {
        document.getElementById('search-results').innerHTML = `You searched for: "${query}"`;
    } else {
        document.getElementById('search-results').innerHTML = 'Please enter a search term.';
    }
});
