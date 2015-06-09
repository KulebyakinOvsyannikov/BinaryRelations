var propertiesBlock;
var propertiesOptionalOrderBlock;

function propertiesInitiateScripts(name) {
    propertiesBlock = document.getElementById(name);
    propertiesOptionalOrderBlock = document.getElementById("optional_order_properties")
}

function propertiesOrderChanged(isOfOrder) {
    if (isOfOrder) {
        propertiesOptionalOrderBlock.style.display = '';
    } else {
        propertiesOptionalOrderBlock.style.display = 'none';
    }
}

function propertiesChangeVisibility(setVisible) {
    propertiesBlock.style.visibility = (setVisible ? '' : 'collapse')
}

function propertiesSetValue(valueString) {
    console.log("setting" + valueString);
    //valueString содержит имя свойтсва и значение. Пример: reflexivity=reflexive
    //Необходимо установить соответсвтующее значение у блока с этим свойством.
    var inputs =  propertiesBlock.getElementsByTagName("input");
    valueString=valueString.split("=");
    for (var i = 0;i<inputs.length;++i)
    {
        if (inputs[i].name==valueString[0]&&inputs[i].value==valueString[1])
        {
            inputs[i].checked=true;
            break;
        }
    }
}

function propertiesUnsetValue(valueString) {
    console.log("unsetting" + valueString);
    //То же, что и сверху, но необходимо убрать отметку, где бы она ни стояла.
    valueString=valueString.split("=");
    var inputs = propertiesBlock.getElementsByTagName("input");
    for (var i = 0;i < inputs.length;++i)
    {
        if (valueString[0]==inputs[i].name) {
            inputs[i].checked = false;
        }
    }
}

function propertiesHighlightErrors(correctSolve) {
    console.log("correct:" + correctSolve);
    correctSolve = correctSolve.split(" ");
    var propParts,userProps;
    for (var i=0;i<correctSolve.length;++i){
        propParts=correctSolve.split("=");
        userProps=propertiesBlock.getElementsByName(propParts[0]);
        for (var j=0;j<userProps.length;++j){
            if (userProps[j].checked && userProps[j].value!=propParts[1]){
                propertiesBlock.getElementById("properties-"+propParts[0]).style.backgroundColor = "red";
            }
        }
    }
}

function propertiesFromAnswersString(partialSolve) {
    console.log("partial:" + partialSolve);
    partialSolve = partialSolve.split(" ");
    var propParts, propToChange;
    for (var i=0;i<partialSolve.length;++i){
        propParts = partialSolve[i].split("=");
        propToChange = propertiesBlock.getElementsByName(propParts[0]);
        for (var j=0;j<propToChange.length;++j){
            if (propToChange[j].value==propParts[1]){
                propToChange[j].checked = true;
            }
        }
    }
}

function propertiesToAnswersString() {
    var propNames = ["properties-reflexivity",
                    "properties-anti-reflexivity",
                    "properties-symmetry",
                    "properties-asymmetry",
                    "properties-antisymmetry",
                    "properties-transitivity",
                    "properties-equivalency",
                    "properties-order",
                    "properties-order-strict",
                    "properties-order-linearity"];
    for (var i=0;i<propNames.length;++i){
        var input = propertiesBlock.getElementById(propNames[i]);
        if (input.children[0].children[0].checked){
            propNames[i]=[propNames[i],input.children[0].children[0].value];
        }
        else if (input.children[1].children[0].checked){
            propNames[i]=[propNames[i],input.children[1].children[0].value];
        }
        else if (i<=7){return undefined}
        else if (propNames[7]!="properties-order=of-order"){
            propNames[i]=[propNames[i],"none"];
        }
        else {return undefined}
        propNames[i].join("=");
    }
    return propNames.join(" ");
}