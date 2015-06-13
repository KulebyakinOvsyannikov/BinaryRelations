/**
 * Created by ilyakulebyakin on 5/29/15.
 */

var graph;
var elements = [];
var noRefresh = false;

function initiateGraph(elementsArray) {
    elements = elementsArray;
    var nodes = [];
    for (var i = 0; i < elements.length; ++i) {
        var node = {id: String(elements[i]),
                    label: String(elements[i]),
                    x: Math.sin(i*2*Math.PI/elements.length),
                    y: Math.cos(i*2*Math.PI/elements.length),
                    size:20
        };
        nodes.push(node);
    }

    var graphData = {
        nodes : nodes,
        edges : []
    };

    document.getElementById('graph_container').style.margin = '25px';
    document.getElementById('graph_container').style.margin.overflow = 'visible';

    graph = new sigma({
        graph: graphData,
        renderer: {
            container: document.getElementById('graph_container'),
            type: 'canvas'
        },
        settings: {
            doubleClickEnabled: false,
            minArrowSize : 10,
            enableEdgeHovering: true,
            edgeHoverColor: 'edge',
            defaultEdgeHoverColor: '#000',
            edgeHoverSizeRatio: 1,
            edgeHoverExtremities: true,
            labelThreshold: 0
        }
    });

    graph.camera.goTo({
        ratio: 1.25
    });

    graph.refresh();
}

function addRelationIndices(fromElement, toElement) {
    addRelation(elements[fromElement], elements[toElement]);
}

function removeRelationIndices(fromElement, toElement) {
    removeRelation(elements[fromElement], elements[toElement]);
}

function changeRelationOnClick(element){
    if (element.checked == false) {
        removeRelationForTableElement(element);
    } else {
        addRelationForTableElement(element);
    }
}

function addRelationForTableElement(element) {
    var inds = element.name.split('-');
    addRelationIndices(parseInt(inds[0]), parseInt(inds[1]));
}

function removeRelationForTableElement(element) {
    var inds = element.name.split('-');
    removeRelationIndices(parseInt(inds[0]), parseInt(inds[1]));
}

function removeRelation(fromElement, toElement) {

    try {
        graph.graph.dropEdge(String(fromElement) + '->' + String(toElement));
        if (noRefresh == false) {
            graph.refresh();
        }
    } catch(except) {
    }
}

function addRelation(fromElement, toElement) {
    try {
        var edge = {
            id: String(fromElement) + '->' + String(toElement),
            source: String(fromElement),
            target: String(toElement),
            type: (fromElement == toElement ? 'curve' : 'arrow')
        };
        graph.graph.addEdge(edge);
        if (noRefresh == false) {
            graph.refresh();
        }
    } catch (except) {
    }
}

function partialGraph(partSolve) {
    noRefresh = true;
    for (var i = 0; i < partSolve.length; ++i) {
        partSolve[i] = partSolve[i].split(' ');
        for (var j = 0; j < partSolve[i].length; ++j) {
            if (partSolve[i][j] == '+') {
                addRelationIndices(i, j);
            }
        }
    }
    graph.refresh();
    noRefresh = false;
}