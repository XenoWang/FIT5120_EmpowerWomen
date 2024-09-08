// 显示/隐藏“Back to Top”按钮
window.onscroll = function() {
    const backToTop = document.getElementById("backToTop");
    if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTop.style.display = "block";
    } else {
        backToTop.style.display = "none";
    }
};

// 点击“Back to Top”按钮后平滑滚动到顶部
document.getElementById("backToTop").addEventListener("click", function(event) {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
});

