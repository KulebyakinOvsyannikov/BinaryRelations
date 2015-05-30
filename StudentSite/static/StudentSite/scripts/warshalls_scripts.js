function fillWarshallsMatrix(partialSolve) {
    partialSolve = partialSolve.split('$');
    var table = document.getElementById('warshalls_table');
    for (var i = 0; i < partialSolve.length; ++i) {
        partialSolve[i] = partialSolve[i].split(' ');
        for (var j = 0; j < partialSolve[i].length; ++j) {
            if (partialSolve[i][i] == '+') {
                table.getElementById('warchall_checkbox_'+i+'-'+j).checked = true;
            }
        }
    }

}