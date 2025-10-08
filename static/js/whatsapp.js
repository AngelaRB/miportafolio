function sendToWhatsapp(){
    let number = "3043730932";

    let name = document.getElementById('name').value;
    let email = document.getElementById('email').value;

    var url = "https://wa.me/" + number + "?text="
    + "Nombre : " +name+ "%0a"
    + "Correo : " +email+ "%0a%0a";

    window.open(url, '_blank').focus();
}