$(function(){ // on dom ready

$('#cy').cytoscape({
  layout: {
    name: 'breadthfirst',
    padding: 10
  },
  
  style: cytoscape.stylesheet()
    .selector('node')
      .css({
        'shape': 'data(faveShape)',
        'width': 'mapData(weight, 40, 80, 20, 60)',
        'content': 'data(name)',
        'text-valign': 'center',
        'text-outline-width': 2,
        'text-outline-color': 'data(faveColor)',
        'background-color': 'data(faveColor)',
        'color': '#fff'
      })
    .selector(':selected')
      .css({
        'border-width': 3,
        'border-color': '#333'
      })
    .selector('edge')
      .css({
        'opacity': 0.666,
        'width': 'mapData(strength, 70, 100, 2, 6)',
        'target-arrow-shape': 'triangle',
        'source-arrow-shape': 'circle',
        'line-color': 'data(faveColor)',
        'source-arrow-color': 'data(faveColor)',
        'target-arrow-color': 'data(faveColor)'
      })
    .selector('edge.questionable')
      .css({
        'line-style': 'dotted',
        'target-arrow-shape': 'diamond'
      })
    .selector('.faded')
      .css({
        'opacity': 0.25,
        'text-opacity': 0
      }),
  
  elements: {
    nodes: [
      { data: { id: 'j', name: 'server.voga360.com', weight: 45, faveColor: '#6FB1FC', faveShape: 'triangle' } },
      { data: { id: 'e', name: 'mobo-www-1397542487.ap-southeast-1.elb.amazonaws.com', weight: 45, faveColor: '#EDA1ED', faveShape: 'ellipse' } },
      { data: { id: 'k', name: 'nginx:54.255.147.17', weight: 45, faveColor: '#86B342', faveShape: 'octagon' } },
      { data: { id: 'g', name: 'nginx:54.255.147.18', weight: 45, faveColor: '#F5A45D', faveShape: 'rectangle' } }
    ],
    edges: [
      { data: { source: 'j', target: 'e', faveColor: '#6FB1FC', strength: 70 } },
      { data: { source: 'e', target: 'g', faveColor: '#6FB1FC', strength: 70 } },
     
      { data: { source: 'e', target: 'k', faveColor: '#EDA1ED', strength: 70 } },

    ]
  },
  
  ready: function(){
    window.cy = this;
    
    // giddy up
  }
});

}); // on dom ready