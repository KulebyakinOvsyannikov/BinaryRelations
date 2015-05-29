/**
 * Created by ilyakulebyakin on 5/2/15.
 */
var elements;
var solveTable;
var solveProps;
var namedSolveProps = {};
var solveWarshalls;
var firstStepWarshalls;
var firstStepTopological;

var solveTopological;
var highlightTips = {};

var tips;

var step = 0;

var graph;

function initiate(jsonData) {
    elements = jsonData['elements'];

    initiateGraph(elements);

    solveTable = jsonData['table_answers'].split('$');
    for (var i = 0; i < solveTable.length; ++i) {
        solveTable[i] = solveTable[i].split(' ');
    }

    solveProps = jsonData['props_answers'].split('$');
    for (i = 0; i < solveProps.length; ++i) {
        var nameValue = solveProps[i].split('=');
        solveProps[i] = nameValue;
        namedSolveProps[nameValue[0]]=nameValue[1];
    }

    highlightTips = jsonData['tips_highlights'];
    if (namedSolveProps['order'] == 'not-of-order') {
        solveProps.pop();
        solveProps.pop();
    }

    solveWarshalls = jsonData['warshalls_answers'].split('$');
    for (i = 0; i < solveWarshalls.length; ++i) {
        solveWarshalls[i] = solveWarshalls[i].split(' ');
    }

    tips = jsonData['tips'];
    solveTopological = jsonData['topological_answers'];

    firstStepWarshalls = solveTable.length * solveTable.length + solveProps.length;
    firstStepTopological = firstStepWarshalls + solveTable.length * solveTable.length;

    var table = document.getElementById('task_table');
    var properties = document.getElementsByClassName('radio-input');
    document.getElementById('task-form-submit').parentElement.removeChild(document.getElementById('task-form-submit'));
    var table_inputs = table.getElementsByTagName('input');
    for (i = 0; i < properties.length; ++i) {
        var prop_inputs = properties[i].getElementsByTagName('input');
        for (var j = 0; j < prop_inputs.length; ++j) {
            prop_inputs[j].onchange = checkPropertyClick
        }
    }

    for (i = 0; i < table_inputs.length; ++i) {
        table_inputs[i].onchange = checkTableClick
    }

    var warshalls = document.getElementById('warshalls_table');
    warshalls = warshalls.getElementsByTagName('input');
    for (i = 0; i < warshalls.length; ++i) {
        warshalls[i].onchange = checkWarshallClick
    }

    var topological_sort = document.getElementById('topological_answers_form').children[0].children[0].children[0].children;
    for (i = 0; i < topological_sort.length; ++i) {
        topological_sort[i].firstElementChild.onclick = undefined;
    }
}

function nextMoveTable() {
    var ind1 = Math.floor((step / solveTable.length));
        var ind2 = step % solveTable.length;

        var elem = document.getElementById('checkbox'+ind1+'-'+ind2);

        if (elem.checked && solveTable[ind1][ind2] == '+') {
            step++;
            elem.disabled = true;
            nextMove();
            return;
        } else if (solveTable[ind1][ind2] == '-') {
            document.getElementById('demo-text-view').innerHTML = tips[step];
            elem.disabled = true;
        } else if (solveTable[ind1][ind2] == '+') {
            document.getElementById('demo-text-view').innerHTML = tips[step];
            elem.checked = true;
            addRelationForTableElement(elem);
            elem.disabled = true;
        }
        step++;
}

function nextMoveProperties() {
    for (var i = 0; i < solveTable.length; ++i) {
        for (var j = 0; j < solveTable.length; ++j) {
            document.getElementById('checkbox'+i+'-'+j).style.outline = "";
        }
    }

    var radio_step = step - (solveTable.length * solveTable.length);
    var name_value = solveProps[radio_step];
    var elem_block = document.getElementById('radio-'+name_value[0]);
    var inputs = elem_block.getElementsByTagName('input');
    var shouldSkip = false;
    if (radio_step < highlightTips.length) {
        for (var key in highlightTips[radio_step]) {
            var cell = document.getElementById('checkbox' + key);
            var color = (highlightTips[radio_step][key] ? 'green' : 'red');
            cell.style.outline = "2px dashed " + color;
        }
    }
    document.getElementById('demo-text-view').innerHTML = tips[step];
    for (i = 0; i < inputs.length; ++i) {
        if (inputs[i].value == name_value[1]) {
            if (inputs[i].checked == true && (name_value[1] != 'not-of-order' && name_value[0] != 'order-linearity')) {
                inputs[i].disabled = true;
                shouldSkip = true;
            }
            inputs[i].checked = true;
            if (inputs[i].value == "of-order") {
                orderChecked(true);
            }
        }
        inputs[i].disabled = true;
    }
    step++;
    if (shouldSkip) {
        nextMove();
    }
}

function nextMoveTopological() {
    document.getElementById('topological_sort_block').style.display = "block";
    var topologicalStep = step - firstStepTopological;
    if (topologicalStep < solveTable.length) {
        var index = solveTopological[topologicalStep];
        var labelElem = document.getElementById('elem-'+index);
        var inputLabel = document.getElementById('submit_span_label-'+topologicalStep);
        inputLabel.innerHTML = labelElem.innerHTML;
        labelElem.style.visibility = "hidden";
        document.getElementById('demo-text-view').innerHTML = tips[step];
        step++;
    }
}

function nextMove() {
    if (step < solveTable.length * solveTable.length) {
        nextMoveTable();
    } else if (step < solveTable.length * solveTable.length + solveProps.length)  {
        nextMoveProperties();
    } else if (step < solveTable.length * solveTable.length * 2 + solveProps.length) {
        nextMoveWarshalls();
    } else if (namedSolveProps['order'] == 'of-order') {
        nextMoveTopological();
    }
}

function nextMoveWarshalls() {
    document.getElementById('warshalls_block').style.display = "block";
    var stepNum = step - firstStepWarshalls;
    var indi = Math.floor(stepNum/solveTable.length);
    var indj = stepNum % solveTable.length;
    document.getElementById('demo-text-view').innerHTML = tips[step];
    var shouldSkip = false;
    if (solveWarshalls[indi][indj] == '+') {
        if (document.getElementById('warshall_checkbox_'+indi+'-'+indj).checked) {
            shouldSkip = true;
        }
        document.getElementById('warshall_checkbox_'+indi+'-'+indj).checked = solveWarshalls[indi][indj] == '+';
    }

    document.getElementById('warshall_checkbox_'+indi+'-'+indj).disabled = true;
    step++;
    if (shouldSkip) {
        nextMoveWarshalls();
    }
}

function previousMove() {
    var shouldSkip = step == 1;
    var last = false;
    if (step > 0) {
        for (var i = 0; i < 2 && step > 0 ; ++i) {
            step--;
            if (step < solveTable.length * solveTable.length) {
                var ind1 = Math.floor((step / solveTable.length));
                var ind2 = step % solveTable.length;

                var elem = document.getElementById('checkbox' + ind1 + '-' + ind2);
                removeRelationForTableElement(elem);
                elem.checked = false;
                elem.disabled = false;
            } else if (step < solveTable.length * solveTable.length + solveProps.length) {
                var radio_step = step - (solveTable.length * solveTable.length);
                var name_value = solveProps[radio_step];
                var elem_block = document.getElementById('radio-'+name_value[0]);
                var inputs = elem_block.getElementsByTagName('input');
                for (var j = 0; j < inputs.length; ++j) {
                    inputs[j].disabled = false;
                    inputs[j].checked = false;
                    if (inputs[j].value == 'of-order') {
                        orderChecked(false);
                    }
                }
            } else if (step < firstStepWarshalls + solveTable.length * solveTable.length) {
                var warshallStep = step - (solveTable.length * solveTable.length + solveProps.length);
                var indi = Math.floor((warshallStep / solveTable.length));
                var indj = warshallStep % solveTable.length;

                var elemw = document.getElementById('warshall_checkbox_'+indi+'-'+indj);
                elemw.checked = false;
                elemw.disabled = false;
            } else {
                var topologicalStep = step - firstStepTopological;
                var inputElem = document.getElementById('submit_element-'+topologicalStep);
                var inputLabel = document.getElementById('submit_span_label-'+topologicalStep);
                document.getElementById('elem-'+solveTopological[topologicalStep]).style.visibility = "";
                inputLabel.innerHTML = "";
            }
            last = false;
        }
        if (!shouldSkip) {
            nextMove();
        }

    }

}

function checkTableClick(element) {
    var name = element.target.name;
    var ind1 = parseInt(name.substring(0,1));
    var ind2 = parseInt(name.substring(2,3));
    if (solveTable[ind1][ind2] == '-') {
        element.target.style.outline = '2px dashed red';
        setTimeout(function () {
            element.target.style.outline = '';
            element.target.checked = false;
            removeRelationForTableElement(element.target);
        }, 1000);
    } else {
        element.target.style.outline = '2px dashed green';
        setTimeout(function () {
            element.target.style.outline = '';
        }, 1000);
    }
}

function checkPropertyClick(element) {
    var correct_value = namedSolveProps[element.target.name];
    if (correct_value != element.target.value) {

        element.target.style.outline = '2px dashed red';
        setTimeout(function () {
            element.target.style.outline = '';
            element.target.checked = false;
            if (element.target.value == "of-order") {
                orderChecked(false);
            }
        }, 1000);
    } else {
        element.target.style.outline = '2px dashed green';
        setTimeout(function () {
            element.target.style.outline = '';
        }, 1000);
    }



}

function checkWarshallClick(element){
    var name = element.target.id;
    var ind1 = parseInt(name.substring(name.length-3,name.length-2));
    var ind2 = parseInt(name.substring(name.length-1,name.length));
    if (solveWarshalls[ind1][ind2] == '-') {
        element.target.style.outline = '2px dashed red';
        setTimeout(function () {
            element.target.style.outline = '';
            remove
        }, 1000);
    } else {
        element.target.style.outline = '2px dashed green';
        setTimeout(function () {
            element.target.style.outline = '';
        }, 1000);
    }
}

function orderChecked(on) {
    if (on === true){
        document.getElementById('radio-order-strict').style.display = 'block';
        document.getElementById('radio-order-linearity').style.display = 'block';
    } else {
        var order_block = document.getElementById('radio-order-strict');
        order_block.style.display = 'none';
        var inputs = order_block.getElementsByTagName('input');
        for (var i = 0; i < inputs.length; ++i) {
            inputs[i].checked = false;
        }
        order_block = document.getElementById('radio-order-linearity');
        order_block.style.display = 'none';
        inputs = order_block.getElementsByTagName('input');
        for (i = 0; i < inputs.length; ++i) {
            inputs[i].checked = false;
        }
    }
}