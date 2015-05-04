/**
 * Created by ilyakulebyakin on 5/3/15.
 */
step = -1;
var content = getCookie('partial_solve').split('$');
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
    console.log(table_array);
    var table = document.getElementById('task_table');
    for (var i = 0; i < table_array.length; ++i) {
        table_array[i] = table_array[i].split(' ');
        for (var j = 0; j < table_array[i].length; ++j) {
            if (table_array[i][j] == '+') {
                console.log('checkbox'+i+'-'+j);
                document.getElementById('checkbox'+i+'-'+j).checked = true;
            }
        }
    }
}

function fillForm() {
    fillTable(content);
    var res = '';
    var partial_solve_warshall = getCookie('partial_solve_warshall');
    for (var i = 0; i < content.length; ++i) {
        for (var j = 0; j < content.length; ++j) {
            res += '-';
            document.getElementById('warshall_checkbox_' + i + '-' + j).onchange = checkboxChanged
        }
    }
    if (partial_solve_warshall != "") {
        partial_solve_warshall = partial_solve_warshall.split(' ');
        for (i = 0; i < content.length; ++i) {
            document.getElementById('warshall_check_' + i).value = partial_solve_warshall[i];
        }
    } else {
        for (i = 0; i < content.length; ++i) {
            document.getElementById('warshall_check_' + i).value = res;
        }
    }
}

function checkboxChanged(event) {
    var element = event.target;
    var ids = element.id.substring(18, 21).split('-');
    document.getElementById('checkbox'+ids[0]+'-'+ids[1]).checked = element.checked || (content[ids[0]][ids[1]]=='+');
    var elem  = document.getElementById('warshall_check_'+step);
    var res = "";
    for (var i = 0; i < content.length; ++i) {
        for (var j = 0; j < content.length; ++j) {
            res += document.getElementById('warshall_checkbox_' + i + '-' + j).checked && !(step==i) && !(step==j) ? '+' : '-' ;
        }
    }

    elem.value = res;
    console.log(res);
}

function nextStep() {
    if (step < content.length - 1) {
        step++;
        document.getElementById('start-continue-button').innerHTML = 'Продолжить';
        if (step > 0) {
            console.log('unhiding');
            document.getElementById('previous-step-button').style.display = "";
        }
    } else {
        return;
    }
    var answers_array = document.getElementById('warshall_check_'+step).value;
    console.log(answers_array);
    for (var i = 0; i < content.length; ++i) {
        for (var j = 0; j < content.length; ++j) {
            document.getElementById('warshall_checkbox_'+ i + '-' + j).style.outline = "";
            document.getElementById('warshall_checkbox_'+ i + '-' + j).checked = answers_array[i*content.length+j] == '+';
            document.getElementById('warshall_checkbox_'+ i + '-' + j).disabled = false;
        }
    }
    for (i = 0; i < content.length; ++i) {
        var elem1 = document.getElementById('warshall_checkbox_'+i+'-'+step);
        var elem2 = document.getElementById('warshall_checkbox_'+step+'-'+i);
        elem1.disabled = true;
        elem2.disabled = true;
        elem1.style.outline = "1px dashed blue";
        elem2.style.outline = "1px dashed blue";
        elem1.checked = content[i][step] == '+';
        elem2.checked = content[step][i] == '+';
    }
}

function previousStep(elem) {
    if (step > 0) {
        step--;
        step--;
        if (step == -1) {
            console.log(elem);
            elem.style.display = "none";
        }
        nextStep();
    }
}