/**
 * Created by ilyakulebyakin on 5/8/15.
 */

function validateRegistration(elem) {

    var pass = document.getElementById('password_field');
    var repPass = document.getElementById('password_repeat');
    var username = document.getElementById('username_field');
    var name = document.getElementById('first_name_field');

    if (username.value.length < 3) {
        alert("Длина имени пользователя должна быть минимум 3 символа")
        return false;
    }

    if (name.value.length < 1) {
        alert("Имя должно быть введено");
        return false;
    }

    if (pass.value.length < 5) {
        alert("Длина пароля должна быть минимум 5 символов");
        return false;
    }
    if (pass.value != repPass.value) {
        alert("Пароли не совпадают");
        return false;
    }
    return true;
}