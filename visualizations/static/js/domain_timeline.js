function drawTimeline(dataset) {
  var m = [40, 40, 80, 40],
    w = 640 - m[1] - m[3],
    h = 480 - m[0] - m[2],
    h_mini = 120;

  var SIX_HOURS = 21600000;

  var dragSelector = d3.behavior.drag().on("drag", dragMoveSelector);
  var dragLeftEdge = d3.behavior.drag().on("drag", dragMoveLeftEdge);
  var dragRightEdge = d3.behavior.drag().on("drag", dragMoveRightEdge);
  var data;

  var x = d3.time.scale().range([0,w]),
      y = d3.scale.linear().range([h,0]),
      x_mini = d3.time.scale().range([0,w]),
      y_mini = d3.scale.linear().range([h_mini,0]),
      xAxis     = d3.svg.axis()
                    .scale(x)
                    .ticks(d3.time.day, 1)
                    .orient("bottom")
                    .tickSize(-h, 0)
                    .tickPadding(6),
      yAxis     = d3.svg.axis()
                    .scale(y)
                    .orient("right")
                    .tickSize(-w)
                    .tickPadding(6),
      xAxisMini = d3.svg.axis()
                    .scale(x_mini)
                    .ticks(d3.time.day, 1)
                    .orient("bottom")
                    .tickSize(-h_mini, 0)
                    .tickPadding(6),
      yAxisMini = d3.svg.axis()
                    .scale(y_mini)
                    .orient("right")
                    .tickSize(-w)
                    .tickPadding(6),
      parse = d3.time.format("%a, %d %b %Y %H:%M:%S").parse;

  var svg = buildMainCanvas();
  var mini_map = buildMiniMap();
  var bars;

  d3.json(dataset, function(error, json) {
    data = json.queries;
    $.each(data, function(index, element) {
      element.date = element.date.replace(" GMT", "");
    });
    update(data);
  });

  drawSelector(0, w);

  function setMainChartXDomain(xmin, xmax) {
      x.domain([x_mini.invert(xmin),x_mini.invert(xmax)]);
      svg.select("g.x.axis").call(xAxis);
    }

  function setMainChartXDomainByDate(xmin, xmax) {
    x.domain([xmin,xmax]);
    svg.select("g.x.axis").call(xAxis);
  }

  function update(data) {

    var dateMin = new Date(d3.min(data, function(d) { return parse(d.date); }).getTime() - SIX_HOURS),
        dateMax = new Date(d3.max(data, function(d) { return parse(d.date); }).getTime() + SIX_HOURS);

    setMainChartXDomainByDate(dateMin, dateMax);
    y.domain([0, d3.max(data, function(d) { return d.count;})]);
    svg.select("g.y.axis").call(yAxis);

    x_mini.domain([dateMin, dateMax]);
    y_mini.domain([0, d3.max(data, function(d) { return d.count;})]);

    mini_map.select("g.x.axis.mini").call(xAxisMini);
    mini_map.select("g.y.axis.mini").call(yAxisMini);

    draw();

    mini_map.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x_mini(parse(d.date)); })
      .attr("y", function(d){ return y_mini(d.count); })
      .attr("width", "10px")
      .attr("height", function(d) { return h_mini - y_mini(d.count); });
  }


  function draw() {
    var bars = svg.selectAll(".bar").data(data);

    // Entering new data
    bars.enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(parse(d.date)); })
      .attr("y", function(d) { return y(d.count); })
      .attr("width", "10px")
      .attr("height", function(d) { return h - y(d.count); });

    // Updating existing bars
    bars
      .attr("x", function(d) { return x(parse(d.date)); })
      .attr("y", function(d) { return y(d.count); })
      .attr("height", function(d) { return h - y(d.count); });
  }

  function buildMiniMap() {
    var mini_map = d3.select("#mini-timeline").append("svg:svg")
      .attr("width", w + m[1] + m[3])
      .attr("height", h_mini + m[0] + m[2])
    .append("svg:g")
      .attr("transform", "translate(" + m[3] + ",0)")
      .attr("class", "minimap");

    mini_map.append("svg:g")
      .attr("class", "x axis mini")
      .attr("transform", "translate(0," + h_mini + ")");

    mini_map.append("svg:g")
      .attr("class", "y axis mini")
      .attr("transform", "translate(" + w + ",0)");

    return mini_map;
  }

  function buildMainCanvas() {
    var svg = d3.select("#timeline").append("svg:svg")
      .attr("width", w + m[1] + m[3])
      .attr("height", h + m[0] + m[2])
    .append("svg:g")
      .attr("transform", "translate(" + m[3] + "," + m[0] + ")");

  svg.append("svg:g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + h + ")");

  svg.append("svg:g")
      .attr("class", "y axis")
      .attr("transform", "translate(" + w + ",0)");

    return svg;
  }

  function dragMoveSelector(d) {
    var offset = this.getBBox().width / 2;
    var edge_width = d3.select("#selector-left-edge").node().getBBox().width;
    var left_boundary = d3.max([0, d3.event.x - offset]);
    var right_boundary = d3.min([d3.event.x + offset, w]);
    var width = right_boundary - left_boundary;
    d3.select(this)
      .attr("x", left_boundary).attr("width", width);
    d3.select("#selector-left-edge")
      .attr("x1", left_boundary - edge_width)
      .attr("x2", left_boundary - edge_width);
    d3.select("#selector-right-edge")
      .attr("x1", right_boundary + edge_width)
      .attr("x2", right_boundary + edge_width);

    setMainChartXDomain(d3.event.x - offset, d3.event.x + offset);
    draw();

  }

  function dragMoveLeftEdge(d) {
    var right_boundary = d3.select("#selector-right-edge").node().getBBox().x;
    var left_boundary = d3.max([0, d3.min([d3.event.x, right_boundary])]);
    d3.select(this).attr("x1", left_boundary).attr("x2", left_boundary);
    updateSelector(left_boundary, right_boundary);
    updateMainChart(left_boundary, right_boundary);
  }

  function dragMoveRightEdge(d) {
    var left_boundary = d3.select("#selector-left-edge").node().getBBox().x;
    var right_boundary = d3.min([d3.max([left_boundary, d3.event.x]), w]);
    d3.select(this).attr("x1", right_boundary).attr("x2", right_boundary);
    updateSelector(left_boundary, right_boundary);
    updateMainChart(left_boundary, right_boundary);

  }

  function updateMainChart(xmin, xmax) {
    setMainChartXDomain(xmin, xmax);
    draw();
  }

  function updateSelector(x1, x2) {
    d3.select("#selector").attr("width", x2 - x1).attr("x", x1);
  }

  function drawSelector(x1, x2) {
    mini_map.append("svg:rect")
      .attr("width", x2 - x1)
      .attr("height", h_mini)
      .attr("x", x1)
      .attr("y", 0)
      .attr("id", "selector")
      .call(dragSelector);

    mini_map.append("svg:line")
      .attr("id", "selector-left-edge")
      .attr("class", "selector-edge")
      .attr("x1", x1)
      .attr("x2", x1)
      .attr("y1", 0)
      .attr("y2", h_mini)
      .call(dragLeftEdge);

    mini_map.append("svg:line")
      .attr("id", "selector-right-edge")
      .attr("class", "selector-edge")
      .attr("x1", x2)
      .attr("x2", x2)
      .attr("y1", 0)
      .attr("y2", h_mini)
      .call(dragRightEdge);
  }
}