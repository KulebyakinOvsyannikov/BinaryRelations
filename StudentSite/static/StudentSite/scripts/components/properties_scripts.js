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
    //Необходимо установить соответсвтующее значение у блока с этим свойтсвом.
}

function propertiesUnsetValue(valueString) {
    console.log("unsetting" + valueString);
    //То же, что и сверху, но необходимо убрать отметку, где бы она не стояла.
}