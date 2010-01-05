
var AJAX_REQUESTS = 0;
var checkOutstandingRequests = function () {
	if (AJAX_REQUESTS > 0)
		return "Det ser ut til at noen endringer ikke har blitt lagret.";
}

var setInvoiced = function (field, change_id) {
	AJAX_REQUESTS++;
	$.post("/ajaxupdate/change/setinvoiced/"+change_id+"/", {
		invoiced: field.checked,
	}, function(data) {	
		if (data == "OK") {
			AJAX_REQUESTS--;
			$(field).successFlash();
		}
		else
			alert("Feil under lagring: "+data);
	});
}

var setStatus = function (fields, sender, change_id) {
	data = {}
	if (!sender)
		sender = fields[0]
	for (var i = 0; i < fields.length; i++) {
		f = $(fields[i]);
		var name = f.attr("name");
		var value = f.val();
		if (f.attr("type") == "checkbox")
			value = fields[i].checked;
		data[name] = value;
	}
	AJAX_REQUESTS++;
	$.post("/ajaxupdate/change/setstatus/"+change_id+"/", data, function(data) {
		if (data == "OK") {
			AJAX_REQUESTS--;
			$(sender).successFlash();
		} else {
			alert("Feil under lagring: "+data);
		}
	});
}
