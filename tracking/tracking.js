/* Event Tracking Library */

var local = window.localStorage;
var queued = false;

/* Tracking Object */
function Tracking () {

}


Tracking.prototype.track = function(eventName) {

	var eventObject = {};
	eventObject['event'] = eventName;
	eventObject['time'] = new Date().toISOSTring();
	
	if (queued){
		local.setItem('event' + '_' + eventObject['time'], JSON.stringify(eventObject));
	}

	this.send(eventObject);

}

Tracking.prototype.send = function() {
	
	var req = new XMLHTTPRequest();

	var url = '';

	// req.open('POS)

}


