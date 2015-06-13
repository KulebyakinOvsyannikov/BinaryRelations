var propertiesBlock;
var propertiesOptionalOrderBlock;
var propertiesIsNotDemo = true;

function propertiesInitiateScripts(name) {
    propertiesBlock = document.getElementById(name);
    propertiesOptionalOrderBlock = document.getElementById("optional_order_properties")
}

function propertiesPrepareForDemo() {
    propertiesIsNotDemo = false;
}

function propertiesOrderChanged(isOfOrder) {
    if (isOfOrder) {
        propertiesOptionalOrderBlock.style.display = '';
    } else {
        propertiesOptionalOrderBlock.style.display = 'none';
    }
    propertiesOptionalOrderBlock.children[0].children[0].children[0].checked = false;
    propertiesOptionalOrderBlock.children[0].children[1].children[0].checked = false;

    propertiesOptionalOrderBlock.children[1].children[0].children[0].checked = false;
    propertiesOptionalOrderBlock.children[1].children[1].children[0].checked = false;

}

function propertiesChangeVisibility(setVisible) {
    propertiesBlock.style.visibility = (setVisible ? '' : 'collapse');

}

function propertiesSetValue(valueString) {
    //valueString содержит имя свойтсва и значение. Пример: reflexivity=reflexive
    //Необходимо установить соответсвтующее значение у блока с этим свойством.
    var inputs =  propertiesBlock.getElementsByTagName("input");
    valueString=valueString.split("=");
    if (valueString[0] == 'order') {
        propertiesOrderChanged(valueString[1] == "of-order");
    }
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
    valueString=valueString.split("=");
    var inputs = propertiesBlock.getElementsByTagName("input");
    if (valueString[0] == "order") {
        propertiesOrderChanged(false);
    }
    for (var i = 0;i < inputs.length;++i)
    {
        if (valueString[0]==inputs[i].name) {
            inputs[i].checked = false;
        }
    }
}

function propertiesHighlightErrors(correctSolve) {
    correctSolve = correctSolve.split(" ");
    var propParts,userProps;
    for (var i=0;i<correctSolve.length;++i){
        propParts=correctSolve[i].split("=");
        userProps=document.getElementById("properties-"+propParts[0]);
        for (var j=0;j<userProps.childElementCount;++j){
            if (userProps.children[j].children[0].checked && userProps.children[j].children[0].value!=propParts[1]){
                document.getElementById("properties-"+propParts[0]).style.backgroundColor = "red";
            }
        }
    }
}

function propertiesFromAnswersString(partialSolve) {
    partialSolve = partialSolve.split(" ");
    var propParts, propToChange;
    for (var i=0;i<partialSolve.length;++i){
        propParts = partialSolve[i].split("=");
        propToChange = document.getElementById("properties-"+propParts[0]);
        for (var j=0;j<propToChange.childElementCount;++j){
            if (propToChange.children[j].children[0].value==propParts[1]){
                if (i == 7 && j == 0) {
                    propertiesOrderChanged(true);
                }
                propToChange.children[j].children[0].checked = true;
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
        var input = document.getElementById(propNames[i]);
        if (input.children[0].children[0].checked){
            propNames[i]=[input.children[0].children[0].name,input.children[0].children[0].value];
        }
        else if (input.children[1].children[0].checked){
            propNames[i]=[input.children[1].children[0].name,input.children[1].children[0].value];
        }
        else if (i<=7){return undefined}
        else if (propNames[7]!="order=of-order"){
            propNames[i]=[input.children[1].children[0].name,"none"];
        }
        else {return undefined}
        propNames[i] = propNames[i].join("=");
    }
    return propNames.join(" ");
}