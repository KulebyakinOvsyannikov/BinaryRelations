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
}

function propertiesUnsetValue(valueString) {
    console.log("unsetting" + valueString);
    //То же, что и сверху, но необходимо убрать отметку, где бы она ни стояла.
}

function propertiesHighlightErrors(correctSolve) {
    console.log("correct:" + correctSolve);
}

function propertiesFromAnswersString(partialSolve) {
    // поступает строка вида
    // reflexivity=non-reflexive anti-reflexivity=anti-reflexive symmetry=non-symmetric asymmetry=asymmetric antisymmetry=antisymmetric transitivity=transitive equivalency=non-equivalent order=of-order order-strict=strict order-linearity=partial
    // на основании этой строки заполнить все свойства

    console.log("partial:" + partialSolve);
}

function propertiesToAnswersString() {
    // Составить строку вида, как в предыдущей функции, на основе заполненных элементов со свойствами.
}