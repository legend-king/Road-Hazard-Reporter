let openSidebarEl = document.getElementById("open-sidebar")
const sidebarEl = document.getElementById("sidebar")
const closeSidebarEl = document.getElementById("close-sidebar")
const check = document.getElementById("check")

openSidebarEl.addEventListener("click",()=>{
    sidebarEl.style.transform = "translate(0px)";
    check.style.display="none";
})
closeSidebarEl.addEventListener("click",()=>{
    sidebarEl.style.transform = "translate(-260px)";
    check.style.display = "";
})