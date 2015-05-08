/**
 * Created by ilyakulebyakin on 5/1/15.
 */

function getCookie(cname){
    var name = cname + '=';
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; ++i) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1);
        if (c.indexOf(name) == 0) {
            return c.substring(name.length+1, c.length-1);
        }
    }
    return ""
}

function fillTable(table_array) {
    //table_array[0] = table_array[0].substring(1);
    var table = document.getElementById('task_table');
    for (var i = 0; i < table_array.length; ++i) {
        table_array[i] = table_array[i].split(' ');
        for (var j = 0; j < table_array[i].length; ++j) {
            if (table_array[i][j] == '+') {
                table.children[0].children[i+1].children[j+1].children[0].checked = true
            }
        }
    }
}

function fillRadios(radios_array) {
    //radios_array[radios_array.length - 1] = radios_array[radios_array.length - 1].substring(0,radios_array[radios_array.length - 1].length-1);
    for (var i = 0; i < radios_array.length; ++i) {
        radios_array[i] = radios_array[i].split('=');
    }

    function find(radio_name) {
        for (var i = 0; i < radios_array.length; ++i) {
            if (radios_array[i][0] == radio_name) {
                return radios_array[i][1];
            }
        }
    }

    var radio_blocks = document.getElementsByClassName("radio-input");
    for (i = 0; i < radio_blocks.length; ++i) {
        var inputs = radio_blocks[i].getElementsByTagName('input');
        var result = find(inputs[0].name);
        for (var j = 0; j < inputs.length; ++j) {
            if (inputs[j].value == result) {
                inputs[j].checked = true;
                if (inputs[0].name == "order" && result == "of-order") {
                    orderChecked(true);
                }
            }
        }
    }
}

function fillForm() {

    var content = getCookie('partial_solve').split('@');
    fillTable(content[0].split('$'));
    fillRadios(content[1].split('$'));
}

function orderChecked(on) {
    if (on === true){
        document.getElementById('radio-order-strict').style.display = 'block';
        document.getElementById('radio-order-linearity').style.display = 'block';
    } else {
        var order_block = document.getElementById('radio-order-strict');
        order_block.style.display = 'none';
        var inputs = order_block.getElementsByTagName('input');
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].checked = false;
        }
        order_block = document.getElementById('radio-order-linearity');
        order_block.style.display = 'none';
        inputs = order_block.getElementsByTagName('input');
        for (i = 0; i < inputs.length; ++i) {
            inputs[i].checked = false;
        }
    }
}

function validateForm() {
    var form = document.getElementById("answers-form");
    for (var i = 0; i < form.children.length; ++i) {
        var child = form.children[i];
        if (child.className === "radio-input" && child.style.display !== "none") {
            var checked = false;
            var radios = child.getElementsByTagName('input');
            for (var j = 0; j < radios.length && !checked; ++j) {
                if (radios[j].checked) checked = true;
            }
            if (!checked) {
                alert("Сначала необходимо заполнить все поля");
                return false;
            }
        }
    }
    return true;
}

function highlightErrors() {
    var user_solve_cookie = getCookie('partial_solve').split('@');
    var user_solve_table = user_solve_cookie[0];
    var correct_table = getCookie('correct_solve_table');
    user_solve_table = user_solve_table.split('$');
    correct_table = correct_table.split('$');
    for (var i = 0; i < user_solve_table.length; ++i) {
        user_solve_table[i] = user_solve_table[i].split(' ');
        correct_table[i] = correct_table[i].split(' ');
        for (var j = 0; j < user_solve_table[i].length; ++j) {
            if (user_solve_table[i][j] != correct_table[i][j]) {
                var elemId = 'checkbox'+i+'-'+j;
                document.getElementById(elemId).style.outline = "2px dashed red"
            }
        }
    }

    var user_solve_properties = user_solve_cookie[1].split('$');
    var correct_solve_props = getCookie('correct_solve_props').split('$');

    for (i = 0; i < correct_solve_props.length; ++i) {
        //console.log(user_solve_properties[i], correct_solve_props[i]);
        if (user_solve_properties[i] != correct_solve_props[i]) {
            var name_value = user_solve_properties[i].split('=');
            var radio_block = document.getElementById('radio-'+name_value[0]);
            var inputs = radio_block.getElementsByTagName('input');
            for (j = 0; j < inputs.length; ++j) {
                if (inputs[j].value == name_value[1]) {
                    inputs[j].style.outline = "2px dashed red";
                    break;
                }
            }
        }
    }
}