var tsElements;
var tsTable;
var tsSelectedElement;
var tsCrossButton;

function tsElementClicked(elem) {
    elem.value = (elem.value == '1' ? '0' : '1');
    graphRelationChanged(elem);
}

function tsGetElement(i,j) {
    return tsTable.children[0].children[i+1].children[j+1].children[0];
}

function tsSelectElement(index) {
    tsSelectedElement = index;
    for (var i = 0; i < tsElements.length; ++i) {
        for (var j = 0; j < tsElements.length; ++j) {
            tsGetElement(i, j).style.outline = (i == index || j == index ? '1px dashed green' : "");
        }
    }
    if (index != -1) {
        if (tsGetElement(index, index).disabled) {
            tsCrossButton.value = "Включить элемент"
        } else {
            tsCrossButton.value = "Исключить элемент"
        }
    }
}

function tsInitiateScripts(elements) {
    tsElements = elements;
    tsTable = document.getElementById('ts_table');
    tsCrossButton = document.getElementById("ts_cross_button");
}

function tsMatrixFromString(solveString) {
    solveString = solveString.split(' ');
    for (var i = 0; i < solveString.length; ++i) {
        for (var j = 0; j < solveString[i].length; ++j) {
            var elem = tsGetElement(i, j);
            elem.value = solveString[i][j];
            graphRelationChanged(elem);
        }
    }
}

function tsCrossElement() {
    var el = tsGetElement(tsSelectedElement, tsSelectedElement);
    el.disabled = !el.disabled;
    el.style.color = el.disabled ? "lightgray" : "black";
    for (var i = 0; i < tsElements.length; ++i) {
        var elem = tsGetElement(i, tsSelectedElement);
        elem.disabled = el.disabled;
        elem.style.color = el.style.color;
        elem = tsGetElement(tsSelectedElement, i);
        elem.disabled = el.disabled;
        elem.style.color = el.style.color;
    }
    tsCrossButton.value = el.disabled ? 'Включить элемент' : 'Исключить элемент';
}

function tsComposeAnswersString() {
    var resStr = [];
    for (var i = 0; i < tsElements.length; ++i) {
        var str = "";
        for (var j = 0; j < tsElements.length; ++j) {
            str += tsGetElement(i, j).value;
        }
        resStr.push(str);
    }
    return resStr.join(' ');
}

function tsHighlightErrors(correct) {
    correct = correct.split(' ');
    for (var i = 0; i < correct.length; ++i) {
        for (var j = 0; j < correct[i].length; ++j) {
            var elem = tsGetElement(i, j);
            if (elem.value != correct[i][j]) {
                elem.style.backgroundColor = "red";
            }
        }
    }
}