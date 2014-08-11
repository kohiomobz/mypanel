

/* Request Data from the Dom */
window.onload = function() {
	
	/* Build the Request URL */
	function buildRequestURL(){
	    /* var dateRange = getDateRange(); */
	    	
	    return '/query';	
	}
	
	/* Fire the XHR Request to mypanel servers */
	var makeDataRequest = function (){
		var req = new XMLHttpRequest();

		var url = buildRequestURL(); 

		req.open('GET', url, true);
		req.onload = function() {
		    var data = JSON.parse(this.responseText);
		    drawGraph(data, '');
		    fillTable(data, '');
		}	
		req.send();
	
	}
	
	/* Highcharts Graphing Function */
        var drawGraph = function(datums, dateRange){
	
	var event_list = [];
	for (var i=0; i < datums.length; i++){
	    if (datums[i]['name'] in event_list === false){
		event_list.push(datums[i]['name']);
	    }
	}
	
	var seriesList = [];
	
	for (var i=0; i < datums.length; i++){
	    var graphObject = {};
	    graphObject['name'] = datums[i]['name'];

	    /* Sum over the events in each bucket */
	    graphObject['data'] = [0,1,2,3,4,5,6,7,8,9,10]
	    seriesList.push(graphObject);

	}	

	$('#container').highcharts({
            title: {
                text: 'Mypanel Trends',
                x: -20 //center
            },
            
            xAxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            },
            yAxis: {
                title: {
                    text: '# Of Events'
                },
                plotLines: [{
                    value: 0,
                    width: 1,
                    color: '#808080'
                }]
            },
            tooltip: {
                valueSuffix: ' Events'
            },
            legend: {
                layout: 'horizontal',
                align: 'center',
                verticalAlign: 'bottom',
                borderWidth: 1
            },
            series: seriesList
        	});

	
	    /* Remove Highcharts plug from the graph */
	
	    $('svg text:contains(Highcharts.com)').hide();
	
	    /* Remove the print menu in the top right corner of the graph */
	
	    $('g.highcharts-button').hide(); /* remove the export module instead */
	}		
	function fillTable(tableData, DateRange) {
	


	}	

	/* Make the Request and Plot the Graph  */
	
	makeDataRequest();
	
}
