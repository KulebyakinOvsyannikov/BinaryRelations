var graphHandle;
var graphContainer;
var graphElements = [];

function graphInitiate(json_data) {
    graphElements = json_data;
    graphContainer = document.getElementById("graph_container");

    var nodes = [];

    for (var i = 0; i < graphElements.length; ++i) {
        var node = {id: String(graphElements[i]),
                    label: String(graphElements[i]),
                    x: Math.sin(i*2*Math.PI/graphElements.length),
                    y: Math.cos(i*2*Math.PI/graphElements.length),
                    size:20
        };
        nodes.push(node);
    }

    var graphData = {
        nodes : nodes,
        edges : []
    };

    graphHandle = new sigma({
        graph: graphData,
        renderer: {
            container: graphContainer,
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
            labelThreshold: 0,
            touchEnabled: false,
            mouseEnabled: false,
            mouseWheelEnabled: false,
            eventsEnabled: false
        }
    });

    graphHandle.camera.goTo({
        ratio: 1.25
    });

}

function graphAddRelation(relationName) {
    var edge = {
            id: relationName,
            source: graphElements[parseInt(relationName.substr(0,1))],
            target: graphElements[parseInt(relationName.substr(2,1))],
            type: (relationName.substr(0,1) == relationName.substr(2,1) ? 'curve' : 'arrow')
        };
    try {
        graphHandle.graph.addEdge(edge);
    } catch (except) {
        console.log(except);
    }

    graphHandle.refresh();
}

function graphRemoveRelation(relationName) {
    try {
        graphHandle.graph.dropEdge(relationName);
        graphHandle.refresh();
    } catch (except) {
        console.log(except);
    }


}

function graphRelationChanged(element) {
    switch (element.value) {
        case '1':
            graphAddRelation(element.name);
            break;
        case '0':
            graphRemoveRelation(element.name);
            break;
    }
}

function graphFillFromString(answersString) {
    answersString = answersString.split('$');
    var edges = [];
    for (var i = 0; i < answersString.length; ++i) {
        for (var j = 0; j < answersString[i].length; ++j) {
            if (answersString[i][j] == '1') {
                edges.push({
                    id: String(i) + '-' + String(j),
                    source: graphElements[i],
                    target: graphElements[j],
                    type: (i == j ? 'curve' : 'arrow')
                })
            }

        }
    }
}