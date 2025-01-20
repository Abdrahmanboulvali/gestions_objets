// login.js

document.getElementById('login-form').addEventListener('submit', function(event) {
    var tel = document.getElementById('tel').value;
    var password = document.getElementById('password').value;
    var a_password = document.getElementById('a_password').value;
    var nome = document.getElementById('nome').value;
    var prenome = document.getElementById('prenome').value;
    // Validation de l'email et du mot de passe
    if (!tel || !password || !nome || !prenome || !a_password) {
        alert("يجب أن تملأ جميع الخانات");
        event.preventDefault(); // Empêche l'envoi du formulaire si les champs sont vides
    }else if (password != a_password){
        alert("تأكد من كلمة السر")
        event.preventDefault();
    }
});

//} else if (!validatetel(tel)) {
//        alert("رقم الهاتف غير صحيح");
//        event.preventDefault(); // Empêche l'envoi du formulaire si l'email n'est pas valide
//

// Fonction de validation d'un tel
//function validatetel(tel) {
//    // التحقق باستخدام تعبير منتظم
//    var regex = /^[234]\d{7}$/;
//    return regex.test(tel);
//}
//
//// مثال على الاستخدام
//var phone1 = "23456789"; // صالح
//var phone2 = "12345678"; // غير صالح
//var phone3 = "45678901"; // صالح

function togglePassword() {
    var passwordField = document.getElementById("password");
    if (passwordField.type === "password") {
        passwordField.type = "text";
    } else {
        passwordField.type = "password";
    }
}