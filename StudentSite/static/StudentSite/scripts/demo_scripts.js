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


function demoInitiateScripts(jsonData) {
    demoMatrixSolve = jsonData['matrixAnswers'].split(' ');
    demoPropertiesSolve = jsonData['propertiesAnswers'].split(' ');

    demoMatrixSteps = demoMatrixSolve.length * demoMatrixSolve.length;
    demoPropertiesSteps = demoMatrixSteps + (demoPropertiesSolve[7].split('=')[1] == 'of-order' ? 10 : 8);


    demoTips = jsonData['tips'];
    demoHighlights = jsonData['tipsHighlights'];
    demoWarshallAnswers = jsonData['warshallAnswers'];
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