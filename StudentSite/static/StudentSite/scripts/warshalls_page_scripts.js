/**
 * Created by ilyakulebyakin on 6/2/15.
 */

function warshallsGetReadyToSubmit(page) {
    if (warshallsStep + 1 != warshallsElements.length) {
        alert("Сначала Вам необходимо пройти все этапы алгоритма Уоршалла");
        return false;
    }
    page.children[1].value = warshallsComposeSolveResponse();
    return true;
}