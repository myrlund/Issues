jQuery.fn.flash = function(color, duration) {
	var current = this.css( 'backgroundColor' );
	this.animate( { backgroundColor: 'rgb(' + color + ')' }, duration / 8);
	this.animate( { backgroundColor: current }, 7 * duration / 8, null );
}
jQuery.fn.successFlash = function() {
	el = this;
	el.attr("disabled", true);
	el.parent("td").flash("0,255,0", 2000);
	setTimeout(function(){
		el.removeAttr("disabled");
	}, 2200);
}

$(document).ready(function() {
	$(".tabarea").tabs();
	bindStatusFormFields();
	formatDateFields();
});

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

var formatDateFields = function() {
	var els = $(".datepicker, .date input, #id_date");
	if (els.length > 0) {
		var id = els[0].id;
		$("#"+id).datepicker({
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
	}
};

var updateFieldValue = function (field, target, change_id) {
	var status = $(field).val();
	url = "/ajaxinfo/statusdate/"+change_id+"/"+status+"/";
	$.get(url, function(data){
		$(target).attr("value", data);
	});
}
