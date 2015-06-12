function tsPageGetReadyToSubmit(elem) {
    elem.children[1].value = tsComposeAnswersString();
    return true;
}