var demoTipsContainer;
var demoStep = 0;

var demoMatrixSolve;
var demoPropertiesSolve;
var demoTips;
var demoHighlights;
var demoWarshallAnswers;
var demoTopologicalAnswers;

var demoMatrixSteps = 0;
var demoPropertiesSteps = 0;
var demoWarshallsSteps = 0;


function demoInitiateScripts(jsonData) {
    console.log(jsonData);
    demoMatrixSolve = jsonData['matrixAnswers'].split(' ');
    warshallsInitialAnswers = demoMatrixSolve;
    demoPropertiesSolve = jsonData['propertiesAnswers'].split(' ');

    demoMatrixSteps = demoMatrixSolve.length * demoMatrixSolve.length;
    demoPropertiesSteps = demoMatrixSteps + (demoPropertiesSolve[7].split('=')[1] == 'of-order' ? 10 : 8);
    demoWarshallsSteps = demoPropertiesSteps + demoMatrixSolve.length;

    demoTips = jsonData['tips'];
    demoHighlights = jsonData['tipsHighlights'];

    demoWarshallAnswers = jsonData['warshallAnswers'].split('@');
    console.log(demoWarshallAnswers);

    demoTopologicalAnswers = jsonData['topologicalAnswers'];

    demoTipsContainer = document.getElementById('tips_container');
}

function demoNextStep() {
    if (demoStep < demoMatrixSteps) {
        nextStepMatrix();
    } else if (demoStep < demoPropertiesSteps) {
        if (demoStep == demoMatrixSteps) {
            propertiesChangeVisibility(true);
        }
        demoNextStepProperties();
    } else if (demoStep < demoWarshallsSteps ) {
        if (demoStep == demoPropertiesSteps) {
            matrixSetPrimaryMatrix("warshalls_primary_matrix");
            document.getElementById("warshalls_block").style.display = "block";
        }
        nextStepWarshalls()
    } else {
        demoStep--;
    }
    demoTipsContainer.innerHTML = demoTips[demoStep];
    demoStep++;
}

function demoPreviousStep() {
    var shouldNotGoForward = false;
    for (var i = 0; i < 2; ++i) {
        if (demoStep > 0) {
            demoStep--;
            if (demoStep < demoMatrixSteps) {
                demoPreviousStepMatrix();
            } else if (demoStep < demoPropertiesSteps) {
                demoPreviousStepProperties();
            } else if (demoStep < demoWarshallsSteps) {
                demoPreviousStepWarshalls();
            }
        } else {
            shouldNotGoForward = true;
        }
    }
    if (demoStep < demoMatrixSteps) {
        propertiesChangeVisibility(false);
    }
    if (shouldNotGoForward) {
        demoStep = 0;
        demoTipsContainer.innerHTML = "";
    } else {
        demoNextStep();
    }
}

function demoPreviousStepMatrix() {
    var row = Math.floor(demoStep/demoMatrixSolve.length);
    var column = demoStep % demoMatrixSolve.length;
    matrixSetCell(row, column, '0', false);
}

function demoPreviousStepProperties() {
    if (demoStep == demoMatrixSteps) {
        propertiesChangeVisibility(false);
    }
    propertiesUnsetValue(demoPropertiesSolve[demoStep-demoMatrixSteps]);
}

function nextStepMatrix() {
    var row = Math.floor(demoStep/demoMatrixSolve.length);
    var column = demoStep % demoMatrixSolve.length;
    matrixSetCell(row, column, demoMatrixSolve[row][column], true);
}

function demoNextStepProperties() {
    propertiesSetValue(demoPropertiesSolve[demoStep - demoMatrixSteps]);
    if ((demoStep - demoMatrixSteps) < demoHighlights.length) {
        matrixHighlightProperties(demoHighlights[demoStep - demoMatrixSteps]);
    }
    else {
        matrixHighlightProperties(undefined);
    }
}

function nextStepWarshalls() {
    var step = demoStep - demoPropertiesSteps;
    console.log(step);
    console.log(demoWarshallAnswers);
    warshallsRowFromAnswersString(step, demoWarshallAnswers[step]);
}

function demoPreviousStepWarshalls(){
    if (demoStep == demoPropertiesSteps) {
        matrixElement = document.getElementById("matrix_table");
        document.getElementById("warshalls_block").style.display = "none";
    }

}