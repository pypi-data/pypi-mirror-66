function draw_graph(server_graph, color, clickHandler) {
  var w = window.innerWidth;
  var h = window.innerHeight;

  var outline = false;

  var size = d3.scale.pow().exponent(1)
    .domain([1, 100])
    .range([8, 24]);

  var force = d3.layout.force()
    .linkDistance(60)
    .charge(-300)
    .size([w,h]);

  var default_node_color = "#ccc";
  //var default_node_color = "rgb(3,190,100)";
  var default_link_color = "brown";
  var nominal_stroke = .5;
  var max_stroke = 4.5;
  var min_zoom = 0.1;
  var max_zoom = 7;
  d3.select("#graph_div").selectAll("*").remove();
  svg = d3.select("#graph_div").append("svg");
  defs = svg.append("defs");
  defs.append("clipPath")
    .attr("id", "small-avatar-clip")
    .append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", small_r)
    .style("stroke-width", 3)
    .style('stroke', "red");

  defs.append("clipPath")
    .attr("id", "big-avatar-clip")
    .append("circle")
    .attr("cx", 0)
    .attr("cy", 0)
    .attr("r", big_r);
  zoom = d3.behavior.zoom().scaleExtent([min_zoom, max_zoom])
  var g = svg.append("g");
  svg.style("cursor", "move");
  graph = {
    'links': [],
    'nodes': server_graph.nodes
  };
  var nodes_map = {}
  for (var i = 0; i < server_graph.nodes.length; i++) {
    nodes_map[server_graph.nodes[i].id] = i
  }
  server_graph.edges.forEach(function(e) {
    graph.links.push({
      'source': nodes_map[e[0]],
      'target': nodes_map[e[1]]
    });
  });
  var linkedByIndex = {};
  graph.links.forEach(function(d) {
    linkedByIndex[d.source + "," + d.target] = true;
  });

  function isConnected(a, b) {
    return linkedByIndex[a.index + "," + b.index] || linkedByIndex[b.index + "," + a.index] || a.index == b.index;
  }

  function hasConnections(a) {
    for (var property in linkedByIndex) {
      s = property.split(",");
      if ((s[0] == a.index || s[1] == a.index) && linkedByIndex[property]) return true;
    }
    return false;
  }

  force
    .nodes(graph.nodes)
    .links(graph.links)
    .start();

  var link = g.selectAll(".link")
    .data(graph.links)
    .enter().append("line")
    .attr("class", "link")
    .style("stroke-width", nominal_stroke)
    .style("stroke", default_link_color)

  var node = g.selectAll(".node")
    .data(graph.nodes)
    .enter().append("g")
    .attr("class", "node")
    .call(force.drag)
  node.on("dblclick.zoom", function(d) {
    d3.event.stopPropagation();
    var dcx = (window.innerWidth / 2 - d.x * zoom.scale());
    var dcy = (window.innerHeight / 2 - d.y * zoom.scale());
    zoom.translate([dcx, dcy]);
    g.attr("transform", "translate(" + dcx + "," + dcy + ")scale(" + zoom.scale() + ")");
  });

  var tocolor = "fill";
  var towhite = "stroke";
  if (outline) {
    tocolor = "stroke"
    towhite = "fill"
  }
  var circle = node.append("path")
    .attr("d", d3.svg.symbol()
      .size(function(d) {
        return Math.PI * Math.pow(d.size, 2);
      })
      .type(function(d) {
        return d.type;
      }))
    .style(tocolor, function(d) {
      return color(d);
    })
    .attr("id", function (d) {
      return 'node_' + d.id;
    })

  node.on("click", clickHandler);
  node.on("mouseover", function(d) {
    svg.style("cursor", "pointer");
  }).on("mouseout", function(d) {
    svg.style("cursor", "move");
  });

  zoom.on("zoom", function() {
    var stroke = nominal_stroke;
    if (nominal_stroke * zoom.scale() > max_stroke) stroke = max_stroke / zoom.scale();
    link.style("stroke-width", stroke);
    // circle.style("stroke-width", stroke);
    circle.attr("d", d3.svg.symbol()
      .size(function(d) {
        return Math.PI * Math.pow(d.size, 2);
      })
      .type(function(d) {
        return d.type;
      }))


    g.attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
  });

  svg.call(zoom);

  resize();
  window.focus();
  d3.select(window).on("resize", resize);

  force.on("tick", function() {

    node.attr("transform", function(d) {
      return "translate(" + d.x + "," + d.y + ")";
    });

    link.attr("x1", function(d) {
        return d.source.x;
      })
      .attr("y1", function(d) {
        return d.source.y;
      })
      .attr("x2", function(d) {
        return d.target.x;
      })
      .attr("y2", function(d) {
        return d.target.y;
      });

    node.attr("cx", function(d) {
        return d.x;
      })
      .attr("cy", function(d) {
        return d.y;
      });
  });

  function resize() {
    var width = $("#graph_div").width(),
      height = $("#graph_div").height();
    svg.attr("width", width).attr("height", height);

    force.size([force.size()[0] + (width - w) / zoom.scale(), force.size()[1] + (height - h) / zoom.scale()]).resume();
  }

  function isNumber(n) {
    return !isNaN(parseFloat(n)) && isFinite(n);
  }
}
