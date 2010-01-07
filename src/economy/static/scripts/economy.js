jQuery.fn.flash = function(color, duration) {
	var current = this.css( 'backgroundColor' );
	// this.animate( { backgroundColor: 'rgb(' + color + ')' }, duration / 8);
	this.css( 'backgroundColor', 'rgb(' + color + ')' );
	this.animate( { backgroundColor: current }, duration, null );
}
jQuery.fn.successFlash = function() {
	el = this;
	el.attr("disabled", true);
	el.parent("td").flash("0,255,0", 500);
	setTimeout(function(){
		el.removeAttr("disabled");
	}, 500);
}

$(document).ready(function() {
	$(".tabarea").tabs();
	bindStatusFormFields();
	formatDateFields();
});

var ajaxSearch = function(sender, model, sortBy, quickedit) {
	var q = $(sender).val();
	var prefix = model.substring(0, 1);
	var url = "?model="+model+"&"+prefix+"sortby="+sortBy+"&ajax";
	if (quickedit == "True")
		url += "&quickedit";
	var target = $("#"+model+"_list");
	if (q.length > 0)
		url += "&"+prefix+"q="+q;
	
	target.load(url);
}

var highlight = function(el, color) {
	$(el).css("backgroundColor", color);
}

var bindStatusFormFields = function() {
	$(".statuspicker").find("select").change(function(){
		var target = $(this).closest("td, div, p").find(".datepicker, .date input");
		var change_id = $('#change_id').val();
		updateFieldValue(this, target, change_id);
	});
}

var popup = function(url) {
	window.open(url,"Homepage","resizable=no,status=yes,scrollbars=yes,width=260,height=500");
}

var toggleEnabled = function(target, sender) {
	sender.checked = false
	alert("Ikke implementert ennå.");
	return;
	
	// Working version
	state = sender.checked
	$(target).attr("disabled", !state);
	if (state) $(target).removeClass("disabled");
	else $(target).addClass("disabled");
}

var formatDateFields = function() {
	var els = $("input.datepicker, .date input, form #id_date");
	els.datepicker({
		showOn: "button",
		dateFormat: "yy-mm-dd",
		firstDay: 1,
		defaultDate: 0,
		monthNames: ["Januar", "Februar", "Mars", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober", "November", "Desember"],
		dayNamesMin: ["Sø", "Ma", "Ti", "On", "To", "Fr", "Lø"],
		nextText: "Neste",
		prevText: "Forrige",
		currentText: "I dag",
		closeText: "Lukk",
		showButtonPanel: true,
		buttonImage: "/static/gfx/calendar.png",
		buttonImageOnly: true,
		buttonText: "Velg"
	});
};

var nextChangeNumber = function (contract_id, target) {
	url = "/ajaxinfo/changenumber/"+contract_id+"/";
	$.get(url, function(data){
		if (data != "ERROR") {
			$(target).val(data);
		}
	});
}

var updateFieldValue = function (field, target, change_id) {
	var status = $(field).val();
	url = "/ajaxinfo/statusdate/"+change_id+"/"+status+"/";
	$.get(url, function(data){
		$(target).attr("value", data);
	});
}
