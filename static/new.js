const sidebarToggle = document.getElementById("sidebarToggle");
const sidebar = document.getElementById("accordionSidebar");
const contentWrapper = document.getElementById("content-wrapper");

sidebarToggle.addEventListener("click", () => {
    // إضافة/إزالة الصف "hidden" لإخفاء الشريط الجانبي
    sidebar.classList.toggle("hidden");

    // توسيع المحتوى الرئيسي عند إخفاء الشريط الجانبي
    contentWrapper.classList.toggle("fullwidth");
});

