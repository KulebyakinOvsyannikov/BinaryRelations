/**
 * Created by ilyakulebyakin on 5/31/15.
 */

var matrixElement;
var matrixElementsCount;
var matrixGraphHandle = undefined;

function matrixInitiateScripts() {
    matrixElement = document.getElementById("matrix_table");
    matrixElementsCount = matrixElement.children[0].childElementCount - 1;
}

function matrixElementClicked(element) {
    element.value = (element.value == '1' ? '0' : '1');
    if (typeof (matrixGraphHandle) == "function" ) {
        matrixGraphHandle(element);
    }
}

function matrixToAnswersString() {
    var resString = '';
    var checkedChildren = matrixElement.children[0];
    for (var i = 1; i < checkedChildren.childElementCount; ++i) {
        var row = checkedChildren.children[i];
        for (var j = 1; j < row.childElementCount; ++j) {
                resString += row.children[j].children[0].value;
        }
        resString += (i == checkedChildren.childElementCount-1 ? '' : ' ');
    }
    return resString;
}

function matrixDeactivate() {
    for (var i = 0; i < matrixElementsCount; ++i) {
        for (var j = 0; j < matrixElementsCount; ++j) {
            matrixGetInputFor(i,j).disabled = true;
        }
    }
}

function matrixSetPrimaryMatrix(containerName) {
    matrixElement = document.getElementById(containerName).children[0];
}

function matrixGetInputFor(i,j) {
    return matrixElement.children[0].children[i+1].children[j+1].children[0]
}

function matrixHighlightErrors(correctSolve) {
    correctSolve = correctSolve.split(' ');
    for (var i = 0; i < correctSolve.length; ++i) {
        for (var j = 0; j < correctSolve[i].length; ++j) {
            var elem = matrixGetInputFor(i,j);
            if (elem.value != correctSolve[i][j]) {
                elem.style.backgroundColor = "red";
            }
        }
    }
}

function matrixFromAnswersString(answers) {
    answers = answers.split(' ');
    for (var i = 0; i < answers.length; ++i) {
        for (var j = 0; j < answers[i].length; ++j) {
            var elem = matrixGetInputFor(i,j);
            elem.value = (answers[i][j] == '1' ? '1' : '0');
            if (elem.value == '1') {
                if (typeof(matrixGraphHandle) == "function"){
                    matrixGraphHandle(elem);
                }
            }
        }
    }
}

function matrixPrepareForDemo() {
    var children = matrixElement.children[0].children;
    for (var i = 1; i < children.length; ++i) {
        for (var j =1; j < children[i].childElementCount; ++j) {
            children[i].children[j].children[0].onclick = matrixDemoClick;
        }
    }
}

function matrixSetCell(row, column, value, disabled) {
    var elem = matrixElement.children[0].children[row+1].children[column+1].children[0];
    elem.disabled = false;
    if (elem.value != value) {
        matrixElementClicked(elem);
        elem.value = value;
    }
    elem.disabled = disabled;
}

function matrixDemoClick(event) {
    var elem = event.target;
    if (elem.value == '0') {
        elem.value = '1';
        if (demoMatrixSolve[elem.name.substr(0,1)][elem.name.substr(2,1)] == '0') {
            elem.style.backgroundColor = 'red';
            setTimeout(function(){
                elem.value = '0';
                elem.style.backgroundColor = '';
            }, 1000)
        } else {
            elem.style.backgroundColor = 'green';
            setTimeout(function(){
                elem.style.backgroundColor = '';
            }, 1000)
        }
    }
}