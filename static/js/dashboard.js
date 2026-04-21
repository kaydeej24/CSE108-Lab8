function showTab(tab) {
    const mine = document.getElementById("mine");
    const add = document.getElementById("add");

    const tabs = document.getElementsByClassName("tab");

    if (tab === "mine") {
        mine.classList.remove("hidden");
        add.classList.add("hidden");

        tabs[0].classList.add("active");
        tabs[0].classList.remove("inactive");

        tabs[1].classList.add("inactive");
        tabs[1].classList.remove("active");
    } else {
        add.classList.remove("hidden");
        mine.classList.add("hidden");

        tabs[1].classList.add("active");
        tabs[1].classList.remove("inactive");

        tabs[0].classList.add("inactive");
        tabs[0].classList.remove("active");
    }
}