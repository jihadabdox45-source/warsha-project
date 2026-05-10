// دارك مود
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}

// بحث بسيط (فلترة بالكلاينت)
function searchCrafts() {
    let input = document.getElementById("searchInput").value.toLowerCase();
    let cards = document.getElementsByClassName("card");

    for (let i = 0; i < cards.length; i++) {
        let title = cards[i].getElementsByTagName("h3")[0];

        if (title.innerHTML.toLowerCase().includes(input)) {
            cards[i].style.display = "block";
        } else {
            cards[i].style.display = "none";
        }
    }
}