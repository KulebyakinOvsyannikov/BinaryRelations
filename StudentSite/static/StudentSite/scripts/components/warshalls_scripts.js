/**
 * Created by ilyakulebyakin on 6/2/15.
 */

var warshallsOperatedMatrix;
var warshallsResultingMatrix;
var warshallsElements;
var warshallAnswerStrings = [];
var warshallsStep = -1;
var warshallsInitialAnswers;

var warshallsIsTraining = false;
var warshallsCorrectAnswers = [];

function warshallsGetElementByIJ(i,j,getOperated) {
    return (getOperated ? warshallsOperatedMatrix : warshallsResultingMatrix).children[0].children[i+1].children[j+1].children[0]
}

function warshallsInitiateScripts(elements, initialSolve) {

    warshallsOperatedMatrix = document.getElementById("warhsalls_operated_matrix");
    warshallsResultingMatrix = document.getElementById("warshalls_resulting_matrix");
    warshallsElements = elements;

    warshallAnswerStrings = [];
    if (typeof(initialSolve) != "undefined") {
        for (var i = 0; i < warshallsElements.length; ++i) {
            warshallAnswerStrings.push(("" + initialSolve).split(' '));
        }
        warshallsInitialAnswers = initialSolve.split(' ');
    }

}

function warshallsRowSelected(row) {
    for (var i = 0; i < warshallsElements.length; ++i) {
        for (var j = 0; j < warshallsElements.length; ++j) {
            var elem = warshallsGetElementByIJ(i,j,true);
            elem.value = warshallAnswerStrings[warshallsStep][i][j];
            if (warshallsIsTraining) {
                if (elem.value != warshallsCorrectAnswers[warshallsStep][i][j]) {
                    elem.style.backgroundColor = "red";
                } else {
                    elem.style.backgroundColor = "";
                }
            }
            if (warshallsStep == 0) {
                matrixSetCell(i,j,warshallsInitialAnswers[i][j],true);
            } else {
                matrixSetCell(i,j,warshallAnswerStrings[warshallsStep-1][i][j], true);
            }
            if (i == row) {
                elem.style.outline = "1px dashed green";
                elem.disabled = true;
            } else if (j == row) {
                elem.style.outline = "1px dashed green";
                elem.disabled = true;
            } else {
                elem.style.outline = "";
                elem.disabled = false;
            }
        }
    }
}

function warshallsElementClicked(element) {
    element.value = (element.value == '1' ? '0' : '1');
    var i = parseInt(element.id.substr(1,1));
    var j = parseInt(element.id.substr(3,1));
    //warshallAnswerStrings[warshallsStep][i][j] = element.value;
    for (var w = warshallsStep; w < warshallsElements.length; ++w) {
        var str = warshallAnswerStrings[w][i];
        warshallAnswerStrings[w][i] = str.slice(0, j) + element.value + str.slice(j + 1, str.length);
    }
}

function warshallsNextElement(button){
    if (warshallsStep < warshallsElements.length - 1) {
        warshallsStep++;
        warshallsRowSelected(warshallsStep);
    }
}

function warshallsPreviousElement(button) {
    if (warshallsStep > 0) {
        warshallsStep--;
        warshallsRowSelected(warshallsStep);
    }
}

function warshallsComposeSolveResponse() {
    var response = [];
    for (var i = 0; i < warshallAnswerStrings.length; ++i) {
        response.push(warshallAnswerStrings[i].join(' '));
    }
    return response.join('@');
}

function warshallsFromAnswersString(answers) {
    answers = answers.split('@');
    warshallAnswerStrings = [];
    for (var i = 0; i < answers.length; ++i) {
        warshallAnswerStrings.push(answers[i].split(' '));
    }
}

function warshallsPrepareForDemo() {
    document.getElementById("warhsalls_prev_button").style.display="none";
    document.getElementById("warhsalls_next_button").style.display="none";
}

function warshallsRowFromAnswersString(row, answers) {
    warshallAnswerStrings[row] = answers.split(' ');
    warshallsStep = row;
    warshallsRowSelected(row);
}

function warshallsHighlightErrors(correctSolve) {
    warshallsIsTraining = true;
    warshallsCorrectAnswers = correctSolve.split('@');
    for (var i = 0; i < warshallsCorrectAnswers.length; ++i) {
        warshallsCorrectAnswers[i] = warshallsCorrectAnswers[i].split(' ');
    }
}
