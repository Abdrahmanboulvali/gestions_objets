document.getElementById('longin-form').addEventListener('submit', function(event) {
    var tel = document.getElementById('tel').value;
    var password = document.getElementById('password').value;
    if (!tel || !password ) {
        alert("يجب أن تملأ كلتا الخانتين");
        event.preventDefault();
    }else if (!validatetel(tel)) {
        alert("رقم الهاتف غير صحيح");
        event.preventDefault();
    }
});

// Fonction de validation d'un tel
function validatetel(tel) {
    // التحقق باستخدام تعبير منتظم
    var regex = /^[234]\d{7}$/;
    return regex.test(tel);
}

