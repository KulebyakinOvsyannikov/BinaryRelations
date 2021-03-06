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
var demoTopologicalSteps = 0;

var demoNextButton;
var demoPreviousButton;


function demoInitiateScripts(jsonData) {
    demoMatrixSolve = jsonData['matrixAnswers'].split(' ');
    warshallsInitialAnswers = demoMatrixSolve;
    demoPropertiesSolve = jsonData['propertiesAnswers'].split(' ');

    demoMatrixSteps = demoMatrixSolve.length * demoMatrixSolve.length;
    demoPropertiesSteps = demoMatrixSteps + (demoPropertiesSolve[7].split('=')[1] == 'of-order' ? 10 : 8);
    demoWarshallsSteps = demoPropertiesSteps + demoMatrixSolve.length;

    if (demoPropertiesSolve[7].split('=')[1] == 'of-order') {
        demoTopologicalSteps = demoWarshallsSteps + demoMatrixSolve.length;
    } else {
        demoTopologicalSteps = demoWarshallsSteps;
    }

    demoTips = jsonData['tips'];
    demoHighlights = jsonData['tipsHighlights'];

    demoWarshallAnswers = jsonData['warshallAnswers'].split('@');

    demoTopologicalAnswers = jsonData['topologicalAnswers'];

    demoTipsContainer = document.getElementById('tips_container');
    document.getElementById("ts_cross_button").style.display="none";

    demoNextButton = document.getElementById("demo_next_button");
    demoPreviousButton = document.getElementById("demo_previous_button");
}

function demoNextStep() {
    demoPreviousButton.style.visibility = "";
    if (demoStep < demoMatrixSteps) {
        nextStepMatrix();
    } else if (demoStep < demoPropertiesSteps) {
        if (demoStep == demoMatrixSteps) {
            propertiesChangeVisibility(true);
        }
        demoNextStepProperties();
    } else if (demoStep < demoWarshallsSteps ) {
        if (demoStep == demoPropertiesSteps) {
            matrixClearHighlights();
            matrixSetPrimaryMatrix("warshalls_primary_matrix");
            document.getElementById("warshalls_block").style.display = "block";
        }
        nextStepWarshalls()
    } else if (demoStep < demoTopologicalSteps) {
        if (demoStep == demoWarshallsSteps) {
            matrixGraphHandle = undefined;
            document.getElementById("topological_block").style.display = "block";
            document.getElementById("warshalls_block").style.display = "none";
            tsMatrixFromString(demoMatrixSolve.join(' '));
        }
        nextStepTopological();
    } else {
        demoStep--;
    }

    if (demoStep == demoTopologicalSteps - 1) {
        demoNextButton.style.visibility = "hidden";
    }

    demoTipsContainer.innerHTML = demoTips[demoStep];
    if (demoStep < demoPropertiesSteps) {
        document.getElementById("warshalls_block").style.display = "none";
    }
    demoStep++;
}

function demoPreviousStep() {
    demoNextButton.style.visibility = "";

    var shouldNotGoForward = false;
    var topDone = false;
    for (var i = 0; i < 2 && topDone != true; ++i) {
        if (demoStep > 0) {
            demoStep--;
            if (demoStep < demoMatrixSteps) {
                demoPreviousStepMatrix();
            } else if (demoStep < demoPropertiesSteps) {
                demoPreviousStepProperties();
            } else if (demoStep < demoWarshallsSteps) {
                demoPreviousStepWarshalls();
            } else if (demoStep < demoTopologicalSteps) {
                demoPreviousStepTopological();
                topDone = true;
            }
        } else {
            shouldNotGoForward = true;
        }
    }
    if (demoStep < demoMatrixSteps) {
        propertiesChangeVisibility(false);
    }

    if (demoStep < demoPropertiesSteps && demoStep >= demoMatrixSteps) {
        document.getElementById("warshalls_block").style.display = "none";
    }

    if (demoStep < demoWarshallsSteps && demoStep >= demoPropertiesSteps) {
        document.getElementById("topological_block").style.display = "none";
        document.getElementById("warshalls_block").style.display = "block";
    }

    if (demoStep == 0) {
        demoPreviousButton.style.visibility = "hidden";
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
        matrixClearHighlights();
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
    warshallsRowFromAnswersString(step, demoWarshallAnswers[step]);
}

function nextStepTopological() {
    var step = demoStep - demoWarshallsSteps;
    tsSelectElement(demoTopologicalAnswers[step]);
    for (var i = 0; i < demoMatrixSolve.length; ++i) {
        if (i != demoTopologicalAnswers[step]) {
            var elem = tsGetElement(i, demoTopologicalAnswers[step]);
            if (!elem.disabled && elem.value == '0') {
                elem.click();
            }
        }
    }
    tsCrossElement();

}

function demoPreviousStepTopological() {
    if (demoStep == demoWarshallsSteps) {
        demoStep--;
    } else {
        demoStep = demoWarshallsSteps - 1;
    }

    tsMatrixFromString(demoMatrixSolve.join(' '));
    for (var i = 0; i < demoMatrixSolve.length; ++i) {
        if (tsGetElement(i,i).disabled) {
            tsSelectElement(i);
            tsCrossElement();
        }
    }
    tsSelectElement(-1);
    demoNextStep();
}

function demoPreviousStepWarshalls(){
    if (demoStep == demoPropertiesSteps) {
        matrixElement = document.getElementById("matrix_table");
        document.getElementById("warshalls_block").style.display = "none";
    }
}