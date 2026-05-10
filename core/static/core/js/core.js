// تبديل الوضع بين الداكن والفاتح
function toggleMode() {
    const body = document.body;
    const modeIcon = document.querySelector('.mode-btn .mode-icon i');
    
    body.classList.toggle("light");
    
    // تغيير الأيقونة
    if (body.classList.contains("light")) {
        modeIcon.className = "fas fa-sun";
        localStorage.setItem('theme', 'light');
    } else {
        modeIcon.className = "fas fa-moon";
        localStorage.setItem('theme', 'dark');
    }
}

// تحميل الوضع المحفوظ عند فتح الصفحة
document.addEventListener('DOMContentLoaded', function() {
    const savedTheme = localStorage.getItem('theme');
    const modeIcon = document.querySelector('.mode-btn .mode-icon i');
    
    if (savedTheme === 'light') {
        document.body.classList.add('light');
        if (modeIcon) modeIcon.className = "fas fa-sun";
    } else {
        if (modeIcon) modeIcon.className = "fas fa-moon";
    }
});