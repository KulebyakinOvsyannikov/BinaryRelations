/**
 * Created by ilyakulebyakin on 6/2/15.
 */

function matrixPageGetReadyToSubmit (form) {
    form.children[1].value = matrixToAnswersString();
    console.log(form.children[1].value);
    return true;
}