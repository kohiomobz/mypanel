/* Event Tracking Library */

var local = window.localStorage;

/* Tracking Object */
function Tracking () {

	this.queued = false;
	this.trackURL = window.location.hostname != '162.243.131.44:8000' ? 'http://162.243.131.44:8000' : '';

};


Tracking.prototype.track = function(eventName) {
	if (!eventName || !eventName.toString) {

		console.log('Please insert a String Value as the event name');
		return false;

	}

	var eventObject = {};
	eventObject['event'] = eventName;
	eventObject['time'] = new Date().toISOString();
	
	if (this.queued){
		local.setItem('event' + '_' + eventObject['time'], JSON.stringify(eventObject));
	  return;
  }

	this.send(eventObject);

};

Tracking.prototype.send = function(events) {
	
	var req = new XMLHttpRequest();
	console.log(events)

	var data = events;

	var url = this.trackURL + '/track?' + 'data=' + JSON.stringify(data);

	console.log(url);

	req.open('GET', url, true);
	
	req.send();

};

Tracking.prototype.dequeue = function() {
	var eventDict = {};

	if (local.length){

		var keys = Object.keys(local);
		for (var i=0; i < keys.length; i++){

			this.send(JSON.parse(local[keys[i]]));
			
			/* Remove the Item from Local Storage */

			local.removeItem(keys[i]);

		}

	}
};
