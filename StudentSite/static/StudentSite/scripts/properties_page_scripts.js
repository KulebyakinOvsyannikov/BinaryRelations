/**
 * Created by ilyakulebyakin on 6/2/15.
 */

function propertiesPageIsReadyToSubmit(form) {
    var answer_str = propertiesToAnswersString();
    if (answer_str==undefined){
        alert("Все свойства должны быть заполнены.");
        return false;
    }
    document.getElementById("properties_to_server").value=answer_str;
    return true;
}