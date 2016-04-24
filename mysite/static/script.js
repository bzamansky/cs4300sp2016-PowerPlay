// SEARCH BY TERM DATA
var candidate_names = {{candidate_names|safe}}; // array of candidate names
var mentions_by_candidate = {{mentions_by_candidate}}; // array of ints, which are the number of times each candidate mentions the query
var debate_titles = {{debate_titles|safe}};
var mentions_by_debate = {{mentions_by_debate}}; // array of ints, which are the number of times each query is mentioned in each debate
var interactions = {{interactions}};

// SEARCH BY CANDIDATE DATA
var top_ten_words = {{ten_words|safe}}; // actual words
var top_ten_words_counts = {{ten_words_counts}}; // num times each of top 10 words is said by that candidate
var respond_to_names = {{respond_names|safe}}; // names of people that candidate responds to (or doesn't)
var respond_to_counts = {{respond_values}};

//console.log(ten_words_counts);

// MAKE WORD CLOUD
function makeWordCloud(w, frequencies) {
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
        d3.select("body").append("svg")
        var svg = d3.select("body").append("svg")
                .attr("width", 700)
                .attr("height", 350)
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
                        .style("font-size", "75px");
                })
                .on("mouseout", function() {
                    d3.select(this).style("fill", "#000000")
                        .style("font-size", function(d) { return d.size + "px"; });
                });
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
/* x_values are labels for bar graphs, category is "Candidate mentions of" or "Debate mentions of"
    bar plot help from https://bl.ocks.org/mbostock/3885304
*/
function makeBarGraph(x_values, y_values, category) {
    // make json array
    var data = [];
    for (var i = 0; i < x_values.length; i++) {
        data.push({'x':x_values[i],'y':y_values[i]});
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
        return "<strong>" + d.x.toUpperCase() + "</strong><br><span style='color:red'>" + d.y + "</span>";
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
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.x); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.y); })
        .attr("height", function(d) { return height - y(d.y); })
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
    nodes.push(
        {
            'name': candidate,
            'responses': 0
        });
    for (var i=0; i<names.length; i++) {
        nodes.push(
        {
            'name': names[i],
            'responses': counts[i]
        });
    }

    // links array
    var links = [];
    for (var i=0; i<names.length; i++) {
        links.push(
        {
            'source': candidate,
            'target': names[i]
        });
    }

    // save nodes and links to graph
    var graph = {
        'nodes': nodes,
        'links': links
    };

    // MAKE GRAPH
    var width = 960,
        height = 500;

    var color = d3.scale.category20();

    var force = d3.layout.force()
        .charge(-120)
        .linkDistance(30)
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
        .style("stroke-width", function(d) { return Math.sqrt(d.responses); }); // make this constant line thickness, possibly?

    var node = svg.selectAll(".node")
        .data(graph.nodes)
        .enter().append("circle")
        .attr("class", "node")
        .attr("r", 5)
        //.style("fill", function(d) { return color(d.group); }) // color by political party?
        .call(force.drag);

    node.append("title")
        .text(function(d) { return d.name; });

    force.on("tick", function() {
        link.attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node.attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
        });
}

var search_option = document.getElementsByTagName('h5')[0].innerText.split(" ")[2];


// IF SEARCH BY TERM
if (search_option == 'terms:') {
    {% if mentions_by_debate %}
        // query mentions by candidate
        makeBarGraph(candidate_names, mentions_by_candidate, "candidate"); // candidate mentions of...
        // query mentions by debate
        makeBarGraph(debate_titles, mentions_by_debate, "debate"); // debate mentions of...
    {% endif %}
}
// IF SEARCH BY CANDIDATE
else if (search_option == 'candidates:') {

	//add a picture of the candidate
	var can = document.getElementsByTagName('h5')[0].innerText.split(" ")[3];
	var candidate = can.substring(1, can.length-1);
	
	var imageurl = "/static/Images/" + candidate + ".jpg";
	// console.log(imageurl);
	// console.log(imageExists(imageurl));
	
    if(imageExists(imageurl)){
		var img = document.createElement("img");
		img.className = "img-circle";
		img.src = imageurl;
		var src = document.getElementById("selfie");
        if(imageurl.split("/")[3].split(".")[0] == 'trump'){
            var a = document.createElement("a");
            a.href = 'http://trumpdonald.org/';
            a.target = "_blank";
            a.appendChild(img)
            src.appendChild(a);
        }
        else{
            src.appendChild(img);
        }
	}
	
	// make response graph
    //console.log(candidate, respond_to_names, respond_to_counts);
    //makeResponseGraph(candidate, respond_to_names, respond_to_counts);

    // make top 10 word cloud for candidate
    makeWordCloud(top_ten_words, top_ten_words_counts);
}