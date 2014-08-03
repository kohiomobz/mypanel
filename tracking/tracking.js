/* Event Tracking Library */

var local = window.localStorage;

/* Tracking Object */
function Tracking () {

	this.queued = false;

}


Tracking.prototype.track = function(eventName) {
	if (!eventName || !eventName.toString) {

		console.log('Please insert a String Value as the event name');
		return false;

	}

	var eventObject = {};
	eventObject['event'] = eventName;
	eventObject['time'] = new Date().toISOSTring();
	
	if (this.queued){
		local.setItem('event' + '_' + eventObject['time'], JSON.stringify(eventObject));
	}

	this.send(eventObject);

}

Tracking.prototype.send = function(events) {
	
	var req = new XMLHTTPRequest();

	var url = '';

	// req.open('POS)

}

Tracking.prototype.dequeue = function() {
	var eventDict = {};

	if (local.length){

		var keys = Object.keys(local);
		for (var i=0; i < keys.length; i++){

			this.send(local[i]);
			
			/* Remove the Item from Local Storage */

			local.removeItem(i);

		}

	}
}

