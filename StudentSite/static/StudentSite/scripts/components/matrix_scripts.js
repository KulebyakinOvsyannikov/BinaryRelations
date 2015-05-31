/**
 * Created by ilyakulebyakin on 5/31/15.
 */

var matrixElement;

function matrixInitiateScripts(name) {
    matrixElement = document.getElementById(name);
}

function matrixElementClicked(element) {
    element.value = (element.value == '1' ? '0' : '1');
    if (typeof (graphRelationChanged) == "function" ) {
        graphRelationChanged(element);
    }
    matrixFromAnswersString(matrixToAnswersString());
}

function matrixToAnswersString() {
    var resString = '';
    var checkedChildren = matrixElement.children[0];
    for (var i = 1; i < checkedChildren.childElementCount; ++i) {
        var row = checkedChildren.children[i];
        for (var j = 1; j < row.childElementCount; ++j) {
                resString += row.children[j].children[0].value;
        }
        resString += (i == checkedChildren.length-1 ? '' : '$');
    }
    return resString;
}

function matrixFromAnswersString(answers) {
    answers = answers.split('$');
    var operatedChildren = matrixElement.children[0].children;
    for (var i = 0; i < answers.length; ++i) {
        var childrenRow = operatedChildren[i+1];
        for (var j = 0; j < answers[i].length; ++j) {
            childrenRow.children[j+1].children[0].value = (answers[i][j] == '1' ? '1' : '0')
        }
    }
}

function matrixPrepareForDemo() {

}

function matrixSetCell(row, column, value) {
    var elem = matrixElement.children[0].children[row+1].children[column+1].children[0];
    if (elem.value != value) {
        elem.click();
    }
}