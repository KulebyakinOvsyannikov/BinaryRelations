/**
 * Created by ilyakulebyakin on 5/5/15.
 */
var numberOfElements = 0;
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

function fillForm() {
    var partialSolve = getCookie('partial_solve').split('$');
    numberOfElements = partialSolve.length;
    if (numberOfElements != 0){
        for (var i = 0; i < partialSolve.length; ++i) {
            partialSolve[i] = partialSolve[i].split(' ');
            for (var j = 0; j < partialSolve[i].length; ++j) {
                var elem = document.getElementById('checkbox'+i+'-'+j);
                elem.checked = partialSolve[i][j] == '+';
            }
        }
    }

    partialSolve = getCookie('partial_solve_warshall');
    if (partialSolve != ""){
        partialSolve = partialSolve.split('$');
        for (var i = 0; i < partialSolve.length; ++i) {
            partialSolve[i] = partialSolve[i].split(' ');
            console.log(partialSolve[i]);
            for (var j = 0; j < partialSolve[i].length; ++j) {
                var elem = document.getElementById('warshall_checkbox_'+i+'-'+j);
                elem.checked = partialSolve[i][j] == '+';
            }
        }
    }
}

function formPOST() {
    var resAr = [];
    for (var i = 0; i < numberOfElements; ++i) {
        var rowAr = [];
        for (var j = 0; j < numberOfElements; ++j) {
            var elem = document.getElementById('warshall_checkbox_'+i+'-'+j);
            rowAr.push(elem.checked ? '+' : '-');
        }
        resAr.push(rowAr.join(' '));
    }
    console.log(resAr.join('$'));
    document.getElementById('warshall_check').value = resAr.join('$')
}

function highlightErrors() {
    var correct = getCookie('correct_solve_warshall').split('$');
    var usersSolve = getCookie('partial_solve_warshall').split('$');
    console.log('inside');
    for (var i = 0; i < numberOfElements; ++i) {
        correct[i] = correct[i].split(' ');
        usersSolve[i] = usersSolve[i].split(' ');
        for (var j = 0; j < numberOfElements; ++j) {

            if (correct[i][j] != usersSolve[i][j]) {
                document.getElementById('warshall_checkbox_'+i+'-'+j).style.outline = "2px dashed red"
            }

        }
    }
}