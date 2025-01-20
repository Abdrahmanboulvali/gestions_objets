
$(document).ready(function () {
    if (!$.fn.DataTable.isDataTable('#dataTable')) {
        $('#dataTable').DataTable({
            responsive: true,
            language: {
                search: "بحث:",
                lengthMenu: "عرض _MENU_ سجل",
                info: "عرض _START_ إلى _END_ من أصل _TOTAL_ سجل",
                paginate: {
                    previous: "السابق",
                    next: "التالي",
                },
            },
        });
    }
});
$(document).ready(function () {
    // تدمير الجدول إذا كان مهيئًا مسبقًا
    if ($.fn.DataTable.isDataTable('#dataTable')) {
        $('#dataTable').DataTable().destroy();
    }

    // إعادة التهيئة
    $('#dataTable').DataTable({
        responsive: true,
        language: {
            search: "بحث:",
            lengthMenu: "عرض _MENU_ سجل",
            info: "عرض _START_ إلى _END_ من أصل _TOTAL_ سجل",
            paginate: {
                previous: "السابق",
                next: "التالي",
            },
        },
    });
});
$('#dataTable').DataTable().columns.adjust().responsive.recalc();
if (!$.fn.DataTable.isDataTable('#dataTable')) { ... }
$('#dataTable').DataTable().destroy();
