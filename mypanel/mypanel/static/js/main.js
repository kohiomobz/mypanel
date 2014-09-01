/* Request Data from the Dom */
window.onload = function() {
    /* Submit a Date Query */
    var fromInput = document.getElementsByName('from')[0];
    var toInput = document.getElementsByName('to')[0];
    var submit = document.getElementById('date-submit');
    var select = document.getElementsByClassName('events')[0];

    submit.onclick = function() {
        event.preventDefault();
        validDateQuery();

    }

    select.onchange = function(){
        makeDataRequest();

    }

    /* Set Default Date Range */

    /* Set To Date to Today's Date */
    toInput.value = new Date().toISOString().split('T')[0];

    /* Convert value to UTC and subtract 30 days in seconds for default value of from date */


    /* Populate the Event Dropdown */

    var populateEvents = function(list) {
        /* Add All to dropdown */

        var option = document.createElement('option');
        option.text = 'All';
        option.selected = true;
        select.add(option);

        for (var i=0; i< list.length; i++){

            var option = document.createElement('option');
            option.text = list[i];
            select.add(option);


        }
    }

    function validDateQuery() {
        if (!fromInput.value || !toInput.value) {
            alert('please enter a valid date range');
            return false;
        }
        makeDataRequest();
    }

    /* Build the Request URL */

    function buildRequestURL(){
        /* var dateRange = getDateRange(); */

        var queryString = '/query?';
        var fromDate = document.getElementsByName('from')[0].value;
        var toDate = document.getElementsByName('to')[0].value;
        var events = document.getElementsByClassName('events')[0].value;
        

        if (fromDate && toDate ) {
            queryString += 'from_date=' + fromDate + '&to_date=' + toDate;
            console.log(events);
        }

        if (events) {

            queryString += '&events=' + events;
        }

        return queryString;
    }

    /* Fire the XHR Request to mypanel servers */
    var makeDataRequest = function (){
        var req = new XMLHttpRequest();

        var url = buildRequestURL(); 

        req.open('GET', url, true);
        req.onload = function() {
            console.log(this.responseText);
            var data = JSON.parse(this.responseText);
            console.log(data);
            drawGraph(data, '');
            fillTable(data, '');
        }
        req.send();

    }

    /* Highcharts Graphing Function */
    var drawGraph = function(datums, dateRange){


        console.log(datums);
        var event_list = [];
        for (var i=0; i < datums.length; i++){
            if (datums[i]['name'] in event_list === false){
                event_list.push(datums[i]['name']);
            }
        }
        /* only once on page load */

        if (!select.length) { populateEvents(event_list) };

        var seriesList = [];

        var populateSeriesList = function(slist) {

            for (var i=0; i < datums.length; i++){
                var graphObject = {};
                graphObject['name'] = datums[i]['name'];

                /* Sum over the events in each bucket */
                graphObject['data'] = [0,1,2,3,4,5,6,7,8,9,10]
                seriesList.push(graphObject);

            }
        }

        /* categories list should be between whatever days you select in the range.  Default is 2014-08-01 to 2014-08-31 */

        /* If date range is longer than a month, sum over buckets for each month and plot if for that month */
        
        categories = [];

        populateSeriesList(seriesList);

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

        function fillTable(tableData, dateRange) {
            /* write a proper remove function at some point */
            removeTableRows();
            
            for (var i=0; i < tableData.length; i++) {
                var table = document.getElementsByClassName('main-table-body')[0];
                var element = document.createElement('tr');
                element.className = 'new-table-row';
                var html = '<td>' + tableData[i]['event_id'] + '</td><td>' + tableData[i]['name'] + '</td><td>' + tableData[i]['time'] + '</td>';

                element.innerHTML = html;
                table.appendChild(element);
            }

        }

        function removeTableRows() {
            var table = document.getElementsByClassName('main-table-body')[0];
            var length = table.getElementsByTagName('tr');

            for (var x = length.length-1; x > 0; x--) {
                table.removeChild(length[x]);

            }


        }

    /* Make the Request and Plot the Graph  */

    makeDataRequest();
}
