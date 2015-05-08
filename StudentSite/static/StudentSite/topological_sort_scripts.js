/**
 * Created by ilyakulebyakin on 5/8/15.
 */
var elementsArray;
var partialSolveTable;

var currentLabel = 0;

function fillTaskTable() {
    for (var i = 0; i < partialSolveTable.length; ++i) {
        for (var j = 0; j < partialSolveTable[i].length; ++j) {
            document.getElementById('checkbox'+i+'-'+j).checked = (partialSolveTable[i][j] == '+');
        }
    }
}

function fillPartial(partialSolve){
    partialSolve = partialSolve.split(' ');
    for (var i = 0; i < partialSolve.length; ++i) {
        document.getElementById('elem-'+partialSolve[i]).click()
    }
}

function initiateScripts(taskObject) {
    elementsArray = taskObject['elements'];
    partialSolveTable = taskObject['table_solve'].split('$');
    if (taskObject.hasOwnProperty('partial_solve_sort')) {
        fillPartial(taskObject['partial_solve_sort'])
    }

    for (var i = 0; i < partialSolveTable.length; ++i) {
        partialSolveTable[i] = partialSolveTable[i].split(' ');
    }
    fillTaskTable();
}

function elementClicked(element) {
    var clickedId = parseInt(element.id.substring(5, 6));
    element.style.visibility = "hidden";
    element.style.pointerEvents = "none";
    document.getElementById("submit_element-" + currentLabel).value = clickedId;
    document.getElementById("submit_span_label-" + currentLabel).innerHTML = elementsArray[clickedId];
    currentLabel++;
}

function formLabelClicked(element) {
    var clickedId = parseInt(element.id.substring(18, 19));
    var inputValue = element.previousElementSibling.value;
    if (inputValue != "") {
        currentLabel--;
        document.getElementById("elem-" + inputValue).style.visibility = "";
        document.getElementById("elem-" + inputValue).style.pointerEvents = "auto";
        document.getElementById("submit_element-" + clickedId).value = "";
        document.getElementById("submit_span_label-" + clickedId).innerHTML = "";
        for (var i = clickedId; i < elementsArray.length - 1; ++i) {
            console.log(document.getElementById("submit_element-" + (i + 1)));
            document.getElementById("submit_element-" + i).value = document.getElementById("submit_element-" + (i + 1)).value;
            document.getElementById("submit_span_label-" + i).innerHTML = document.getElementById("submit_span_label-" + (i + 1)).innerHTML;
        }
        document.getElementById("submit_element-" + (elementsArray.length-1)).value = "";
        document.getElementById("submit_span_label-" + (elementsArray.length -1)).innerHTML = "";
    }
}

function highlightErrors(error) {
    for (var i = error; i < elementsArray.length; ++i) {
        var element = document.getElementById('submit_span_label-' + i);
        element.style.outline = "1px dashed red";
    }
    setTimeout(function (){
        for (var i = error; i < elementsArray.length; ++i) {
            var element = document.getElementById('submit_span_label-' + i);
            element.style.outline = "";
        }
    }, 4000)
}