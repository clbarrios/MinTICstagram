

function openTab(id) {
    var i, tabcontents, tabs, activeTab;
    tabcontents = document.getElementsByClassName("tab-content");

    for (i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }

    tabs = document.getElementsByClassName("tab")
    for (i = 0; i < tabs.length; i++) {
        tabs[i].className = tabs[i].className.replace(" active", "");
    }

    console.log(id+"-content");
    activeTab = document.getElementById(id + "-content");
    activeTab.style.display = "block";

    console.log(id+"-tab");
    activeTab = document.getElementById(id + "-tab");
    activeTab.className += " active";
}

