/**
 * Created by ilyakulebyakin on 6/2/15.
 */

function matrixPageGetReadyToSubmit (form) {
    form.children[1].value = matrixToAnswersString();
    return true;
}