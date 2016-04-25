// SEARCH BY TERM DATA

// DEMOCRAT NAMES
var dem_names = ["clinton", "sanders", "o'malley", "chafee", "webb"];

// REPUBLICAN NAMES
var rep_names = ["cruz", "kasich", "trump", "rubio", "bush", "christie", "fiorina", "santorum", "paul", "huckabee", "pataki", "graham", "jindal", "walker", "perry", "carson"];

// MAKE WORD CLOUD
/* w is top words by that candidate, frequencies is number of times each word in w is used by candidate */
function makeWordCloud(candidate, w, frequencies) {
    var frequency_list = [];
    for (var i=0; i<w.length; i++) {
        frequency_list.push({
            'text': w[i],
            'size': frequencies[i]
        });
    }

    // custom color scale domain values
    var max_freq = Math.max.apply(Math, frequencies); 
    var min_freq = Math.min.apply(Math, frequencies); 
    var domain_values = [];
    var num_steps = 10;
    var fraction = (max_freq - min_freq)/num_steps;
    for (var i=1; i<num_steps+1; i++) {
        domain_values.push(Math.round(fraction*i)); // whole number
    }

    //var colors = ["#B3B3B3", "#868686", "#595959", "#2C2C2C", "#000000"];
    //console.log(domain_values);

    // COLOR SCALE FOR WORDS
    var color = d3.scale.linear()
            // .domain([0,10,20,30,40,50,60,100,150,300,400]) // domain for non-tfidf values
            .domain([0.10, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.20, 0.22, 0.30]) // for tfidf values
            //.domain([0,10,30,40,60,100,150,300,400])
            //.domain(domain_values)
            .range(["#ddd", "#ccc", "#bbb", "#aaa", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);
            //.range(colors);

    var scale_value = 150; // make size of words smaller

    d3.layout.cloud().size([850, 350])
            .words(frequency_list)
            //.rotate(function() { return ~~(Math.random()*2) * 90;}) // 0 or 90deg - from https://www.pubnub.com/blog/2014-10-09-quick-word-cloud-from-a-chatroom-with-d3js/
            .rotate(0)
            //.fontSize(function(d) { return d.size; })
            .fontSize(function(d) { return d.size*scale_value; }) // need to make text bigger
            .on("end", draw)
            .start();

    

    function draw(words) {
        var width = 700,
            height = 350;
        var svg = d3.select(".candidate_viz").append("svg")
                .attr("width", width)
                .attr("height", height)
                .attr("class", "wordcloud");
        var grouping = svg.append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(320,200)")
        var text = grouping.selectAll("text")
                .data(words)
                .enter().append("text").attr("class", "wordcloud_text")
                .style("font-size", function(d) { return d.size + "px"; })
                //.style("fill", function(d, i) { return color(i); })
                //.style("fill", function(d, i) { return color(i); }) // COLOR SCALE
                .style("fill", "#000000")
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                //.attr("transform", "translate(320,200)") // transform text
                .text(function(d) { return d.text; })
                .on("mouseover", function() {
                    d3.select(this).style("fill", "#4285F4")
                        .style("font-size", "50px");
                })
                .on("mouseout", function() {
                    d3.select(this).style("fill", "#000000")
                        .style("font-size", function(d) { return d.size + "px"; });
                })
                .on("click",function(d){
                    wordClick(d.text,candidate);
                });
        svg.append("text")
            .attr("x", width / 2 )
            .attr("y", 50)
            .style("text-anchor", "middle")
            .style("text-decoration", "underline")
            .style("font-weight", "bold")
            .text("Top Words Used by " + candidate.toUpperCase());

    }
}

/* A function to display text including the word clicked on */
function wordClick(word,candidate){
    //found on stack overflow
    function getAllIndices(arr, val) {
        var indexes = [], i = -1;
        while ((i = arr.indexOf(val, i+1)) != -1){
            indexes.push(i);
        }
        return indexes;
    }

    var text = all_text_dict[candidate].split(" ");
    var indices = getAllIndices(text, word, false);
    var span = 15;
    for (var i = 0; i < indices.length; i++) {
        if(indices[i]>span && indices[i] < text.length - span){
            console.log(text.slice(indices[i] - span,indices[i] + span))
        }
    }   
}


/* A function to check if a file exists on the servor. In this case, we want to pull images if they exist for candidates.*/
function imageExists(image_url){

    var http = new XMLHttpRequest();

    http.open('HEAD', image_url, false);
    http.send();

    return http.status != 404;

}

// MAKE BAR GRAPH 
/* x_values are labels for bar graphs, category is "candidate" or "debate"
    bar plot help from https://bl.ocks.org/mbostock/3885304
*/
function makeBarGraph(x_values, y_values, category) {
    // make json array
    var data = [];
    if (category == "candidate"){
        var tmp = [];
        for (var i = 0; i < x_values.length; i++) {
            tmp.push([x_values[i],y_values[i]]);
        }
        tmp.sort();
        for (var i = 0; i < tmp.length; i++) {
            data.push({'x':tmp[i][0],'y':tmp[i][1]});
        }
    }
    else{
        var months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
        var tmp = []
        for (var i = 0; i < x_values.length; i++) {
            var date_parts = x_values[i].split(" ");
            var date = new Date(parseInt(date_parts[2]),months.indexOf(date_parts[0]),parseInt(date_parts[1].replace(/,/g, "")));
            tmp.push([date,x_values[i],y_values[i]]);
        }
        tmp.sort(function(a,b){
            return new Date(a[0]) - new Date(b[0]);
        })
        for (var i = 0; i < tmp.length; i++) {
            data.push({'x':tmp[i][1],'y':tmp[i][2]});
        }
    }

    var margin = {top: 40, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    var formatPercent = d3.format(".0%");

    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    // var xAxis = d3.svg.axis()
    //     .scale(x)
    //     .orient("bottom");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var tip = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, -50])
        .html(function(d) {
            // if candidate is a democrat
            if (dem_names.indexOf(d.x) != -1){
                var color = "#4285F4";
            }
            // if candidate is a republican
            else if (rep_names.indexOf(d.x) != -1) {
                var color = "#d93232";
            }
            // if it's a debate date and location
            else {
                var color = "red";
            }
            var tool_text = "<strong>" + d.x.toUpperCase() + "</strong><br><span style='color:" + color + "'>" + d.y + "</span>";
            return tool_text;
        });

    var svg = d3.select("body")
                .append("div")
                .attr("class","svg_div")
                .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    svg.call(tip);

    x.domain(data.map(function(d) { return d.x; }));
    y.domain([0, d3.max(data, function(d) { return d.y; })]);

    // svg.append("g")
    //     .attr("class", "x axis")
    //     .attr("transform", "translate(0," + height + ")")
    //     .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Number of Mentions");

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        // set class, in main.css make color of bar accordingly
        .attr("class", function(d) {
            // if candidate is a democrat
            if (dem_names.indexOf(d.x) != -1){
                class_text = "bar-dem";
            }
            // if candidate is a republican
            else if (rep_names.indexOf(d.x) != -1) {
                class_text = "bar-rep";
            }
            // if it's a debate date and location
            else {
                class_text = "bar";
            }
            return class_text;
        })
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y); })
        .attr("height", function(d) {
            // if height not 0
            if (d.y != 0) {
                return height - y(d.y);
            }
            // if height is 0, we still want users to be able to see the data
            else {
                return 5;
            }
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);

    // get query
    var q = document.getElementsByTagName('h5')[0].innerText.split(" ")[3];
    var query = q.substring(1, q.length-1).toUpperCase();
    
    // set graph title
    if (category == 'candidate') {
        svg.append("text")
            .attr("x", width / 2 )
            .attr("y", -5)
            .style("text-anchor", "middle")
            .style("text-decoration", "underline")
            .style("font-weight", "bold")
            .text("Number of Times Each CANDIDATE Mentions " + query);
    }
    else if (category == 'debate') {
        svg.append("text")
            .attr("x", width / 2 )
            .attr("y", -5)
            .style("text-anchor", "middle")
            .style("text-decoration", "underline")
            .style("font-weight", "bold")
            .text("Number of Times Each DEBATE Mentions " + query);
    }
    
    d3.select("body").append("br");
    d3.select("body").append("br");

}


// MAKE RESPONSE GRAPH
/* names is names of candidates respond to, counts is num times query candidate responds to each candidate */
function makeResponseGraph(candidate, names, counts) {
    // SET UP NODES AND LINKS
    // nodes array
    var nodes = [];
    var can_group = "";
    if (dem_names.indexOf(candidate) != 0) {
        can_group = 'dem';
    }
    else if (rep_names.indexOf(candidate) != 0) {
        can_group = 'rep';
    }
    nodes.push(
        {
            'name': candidate,
            'responses': 0,
            'neighbors': [],
            'group': can_group
        });
    for (var i=0; i<names.length; i++) {
        var group = "";
        if (dem_names.indexOf(names[i]) != 0) {
            group = 'dem';
        }
        else if (rep_names.indexOf(names[i]) != 0) {
            group = 'rep';
        }
        nodes.push(
        {
            'name': names[i],
            'responses': counts[i],
            'neighbors': [],
            'group': group
        });
    }

    // links array
    var links = [];

    // save nodes and links to graph
    var graph = {
        'nodes': nodes,
        'links': links
    };

    // make links
    for (var i = 0; i < counts.length; i++) {
        var target_node = graph.nodes[i+1]; // exclude the first node, which is the query candidate
        var source_node = graph.nodes[0]; // first node is query candidate
        source_node.neighbors.push(target_node);
        links.push({
            'source': source_node,
            'target': target_node,
            'weight': counts[i]
        });
    };

    // MAKE GRAPH
    var width = 960,
        height = 500;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(90)
        .size([width, height]);

    var svg = d3.select("body").append("svg")
        .attr("width", width)
        .attr("height", height);

    force.nodes(graph.nodes)
        .links(graph.links)
        .start();

    var link = svg.selectAll(".link")
        .data(graph.links)
        .enter().append("line")
        .attr("class", "link")
        .style("stroke-width", function(d) {
            return Math.sqrt(d.weight);
        })
        .style("stroke", "gray");

    var node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        //.attr("r", 9)
        .attr("r", function(d) {
            if (d.name == candidate) {
                return 12;
            }
            else {
                return 7;
            }
        })
        // .style("fill", function(d) { 
        //     if (d.group == 'dem') {
        //         return "blue";
        //     }
        //     else if (d.group == 'rep') {
        //         return "red";
        //     }
        // }) // color by political party
        .call(force.drag);

    // shows candidate name when hover over node
    node.append("title")
        .text(function(d) { return d.name; });
    
    // always show candidate names
    node.append("text")
        // .attr("x", function(d) { return d.x+8; })
        // .attr("y", function(d) { return d.y-8; })
        .attr("dx", 12)
        .attr("dy", "35em")
        .text(function(d) { return d.name; })
        .attr("fill", "black");

    // shows # responses when hover over link
    link.append("title")
        .text(function(d) { return "Responses: " + d.weight; });

    // title for network graph
    svg.append("text")
        .attr("x", width / 2 )
        .attr("y", 100)
        .style("text-anchor", "middle")
        .style("text-decoration", "underline")
        .style("font-weight", "bold")
        .text("Number of Times " + candidate.toUpperCase() + " Responds to Other Candidates");

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });
}




