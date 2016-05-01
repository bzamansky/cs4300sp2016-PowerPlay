// SEARCH BY TERM DATA

// DEMOCRAT NAMES
var dem_names = ["clinton", "sanders", "o'malley", "chafee", "webb"];

// REPUBLICAN NAMES
var rep_names = ["cruz", "kasich", "trump", "rubio", "bush", "christie", "fiorina", "santorum", "paul", "huckabee", "pataki", "graham", "jindal", "walker", "perry", "carson"];

// MAKE WORD CLOUD
/* w is top words by that candidate, frequencies is number of times each word in w is used by candidate */
function makeWordCloud(candidate, w) {
    var frequency_list = []; 
    var w_keys = Object.keys(w);
    for (var i=0; i<w_keys.length; i++) {
        frequency_list.push({
            'text': w_keys[i],
            'size': w[w_keys[i]]
        });
    }

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
        var svg = d3.select("#word_cloud").append("svg")
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
                .on("mouseover", function(d) {
                    text.style("fill","gray")
                        .style('opacity',0.5);
                    d3.select(this).style("fill", "purple")
                        .style("font-size", "50px")
                        .style("opacity",1);
                    wordHover(d.text,candidate);
                })
                .on("mouseout", function() {
                    text.style("fill","black")
                        .style("opacity",1);
                    d3.select(this).style("fill", "#000000")
                        .style("font-size", function(d) { return d.size + "px"; });
                    //my_close();
                })
                .on("click",function(d){   
                    var destination = "http://" + window.location.hostname + ":" + window.location.port + window.location.pathname + "?search=" + d.text + "&search_option=term"
                    window.location.href = (destination);
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

/* A function to display text including the word hovered over */
function wordHover(word,candidate){
    my_close();

    var outputs = all_text_dict[candidate][word];
    document.getElementById("word").innerHTML = word;
    // var destination = "http://" + window.location.hostname + ":" + window.location.port + window.location.pathname + "?search=" + word + "&search_option=term"
    // document.getElementById("word_tag").href=destination;

    var used_words_list = document.getElementById("used_words_list");
    for (var i = 0; i < outputs.length; i++) {
        var list = document.createElement("li");
        var node = document.createTextNode(outputs[i]);
        list.appendChild(node);
        used_words_list.appendChild(list);
    }
    var used_words = document.getElementById("used_words");
    used_words.style.visibility='visible';
}

function my_close(){
    used_words.style.visibility="hidden";
    used_words_list.innerHTML="";
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
    can_num_debates is dict of candidates and number of debates they speak in
*/
function makeBarGraph(x_values, y_values, category) {
    // construct candidate_num_debates dict
    // var candidate_num_debates = {};
    // for (var i=0; i<can_num_debates_names.length; i++) {
    //     var name = can_num_debates_names[i];
    //     var value = can_num_debates_values[i].length;
    //     candidate_num_debates[name] = value;
    // }

    // make json array
    var data = [];
    var norm = 1; // default normalization
    var norm_text = "";
    var cla = "svg_div"
    if (category == "candidate"){
        cla += " candidate_bars"
        var tmp = [];
        for (var i = 0; i < x_values.length; i++) {
            var cand_name = x_values[i];
            // if dict not empty, then we want to normalize
            
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
        .offset([-10, 0])
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
                .attr("class",cla)
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
        .text("Number of Mentions" + norm_text);

    svg.selectAll(".bar")
        .data(data)
        .enter().append("rect")
        // set class, in main.css make color of bar accordingly
        .attr("class", function(d) {
            name = d.x;
            split_name = name.split(" ");
            name_len = split_name.length
            // if candidate is a democrat
            if (dem_names.indexOf(name) != -1 || split_name[name_len-1] == "D"){
                class_text = "bar-dem";
            }
            // if candidate is a republican
            else if (rep_names.indexOf(name) != -1 || split_name[name_len-1] == "R") {
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
        // show tooltip when hover over bar
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)
        // bring to candidate page when bar is clicked
        .on("click",function(d){
            if (category == 'candidate') {
                var destination = "http://" + window.location.hostname + ":" + window.location.port + window.location.pathname + "?search=" + d.x + "&search_option=candidate";
                window.location.href = (destination);
            }
        });

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

    var svg = d3.select(".force_graph")
        .append("svg")
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
        // set class to be dem-node, rep-node, or node - use this to color node by political party
        .attr("class", function(d) {
            var name = d.name;
            var split_name = name.split(" ");
            var name_len = split_name.length;
            var class_text = "node"; // default
            // if candidate is a democrat
            if (dem_names.indexOf(name) != -1 || split_name[name_len-1] == "D"){
                class_text = "node-dem";
            }
            // if candidate is a republican
            else if (rep_names.indexOf(name) != -1 || split_name[name_len-1] == "R") {
                class_text = "node-rep";
            }
            // if it's a debate date and location
            else {
                class_text = "node";
            }
            return class_text;
        })
        // make center node bigger
        .attr("r", function(d) {
            if (d.name == candidate) {
                return 12;
            }
            else {
                return 7;
            }
        });
        //.call(force.drag);

    // create tooltip for node
    var tip_node = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            var tool_text = "<strong>" + d.name.toUpperCase() + "</strong>";
            return tool_text;
        });

    // create tooltip for link
    var tip_link = d3.tip()
        .attr('class', 'd3-tip')
        .offset([-10, 0])
        .html(function(d) {
            var tool_text = "<strong>" + d.weight + "</strong> responses";
            return tool_text;
        });

    // call tooltips
    node.on('mouseover', tip_node.show)
        .on('mouseout', tip_node.hide)
        // bring to candidate page when node is clicked
        .on("click",function(d){
            // don't reload page if click center node
            if (d.name != candidate) {
                var destination = "http://" + window.location.hostname + ":" + window.location.port + window.location.pathname + "?search=" + d.name + "&search_option=candidate";
                window.location.href = (destination);
            }
        });
    link.on('mouseover', tip_link.show)
        .on('mouseout', tip_link.hide);
    svg.call(tip_node);
    svg.call(tip_link);
    
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




