$(function() {
  var w = 500,
      h = 500,
      text_size = 20,
      root,
      texts,
      rects;

  var force = d3.layout.force()
    .on("tick", tick)
    .size([w, h])
    .charge(function(d) { return -10; })
    .linkDistance(function(d) { return d.target._children ? 10 : 10; })
    .size([w, h - 160]);

  var vis = d3.select("#clusters-force").append("svg:svg")
    .attr("width", w)
    .attr("height", h);

  d3.json("/static/data/force_layout.json", function(json) {
    root = json;
    root.fixed = true;
    root.x = w / 2;
    root.y = h / 2;
    update();
  });

  function update() {
    var nodes = flatten(root),
        links = d3.layout.tree().links(nodes),
        roots = [];
    var svg = d3.select("svg");

    force
      .nodes(nodes)
      .links(links)
      .start();

    nodes.forEach(function(o, i) { if (o.children) { roots.push(o); } });

    link = vis.selectAll("line.link")
      .data(links, function(d) { return d.target.id; });

    link.enter().insert("svg:line", ".node")
      .attr("class", "link")
      .attr("x1", function(d) { return d.source.x; })
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

    link.exit().remove();

    node = vis.selectAll("circle.node")
        .data(nodes, function(d) { return d.id; })
        .style("fill", color);

    node.enter().append("svg:circle")
        .attr("class", "node")
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; })
        .attr("r", function(d) { return d.children ? 2 : 3; })
        .style("fill", color)
        .on("click", click)
        .call(force.drag);

    node.exit().remove();

    rects = svg.selectAll("rect")
        .data(roots, function(d) { return d.id; })
        .enter().append("rect")
        .attr("x", function(d) { return d.x; })
        .attr("y", function(d) { return d.y - text_size; })
        .attr("width", 70)
        .attr("height", text_size + 5)
        .style("fill", "#2d2d2d")
        .style("stroke", "#666");

    texts = svg.selectAll("text")
                .data(roots, function(d) { return d.id; })
                .enter().append("text")
                .attr("fill", "white")
                .attr("font-size", text_size + "px")
                .text(function(d) { return d.name; });
  }

  function color(d) {
    return d._children ? "#3182bd" : d.children ? "#c6dbef" : "#fd8d3c";
  }

  function tick() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });

    texts.attr("transform", function(d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

    rects.attr("x", function(d) { return d.x; })
         .attr("y", function(d) { return (d.y - text_size); });
  }

  function click(d) {
  }

  function flatten(root) {
    var nodes = [], i = 0;

    function recurse(node) {
      if (node.children) node.size = node.children.reduce(function(p, v) { return p + recurse(v); }, 0);
      if (!node.id) node.id = ++i;
      nodes.push(node);
      return node.size;
    }

    root.size = recurse(root);
    return nodes;
  }
});