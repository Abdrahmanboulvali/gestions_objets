document.getElementById('objet-form').addEventListener('submit', function(event) {
    var destribition = document.getElementById('destribition').value;
    var statu = document.getElementById('statu').value;
    if (!destribition ) {
        alert("Il faut entrer un destribition");
        event.preventDefault();
    }
    if (!statu ) {
        alert("Il faut choisir le statu de l'objet");
        event.preventDefault();
    }
});