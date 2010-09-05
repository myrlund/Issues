
$(document).ready(function(){
	$.datepicker.setDefaults($.datepicker.regional['no']);
	$.datepicker.setDefaults({
		dateFormat: "yy-mm-dd",
		firstDay: 1
	});
	
	$(".date, .datepicker").datepicker();
	
	$("article.closed > section").hide();
});

var toggleSection = function(caller) {
	// We have a structure like:
	// <article> <- target
	//  <h3><caller/></h3>
	//  <section>
	
	var c = 'closed';
	
	// Slide up
	var section = $(caller).parent().next();
	var article = $(caller).closest('article');
	
	article.toggleClass('closed');
	section.slideToggle('normal');
}

var toggleUpdateForm = function(caller) {
	$(caller).parent().find('.update-form').toggle('slow');
}

jQuery(function($) {
    $("a[rel^='lightbox']").slimbox({
    	counterText: "Bilde {x} av {y}"
    }, function(el) {
            return [el.href, el.title + '<br /><a href="' + el.href + '">Last ned</a>'];
    }, function(el) {
            return (this == el) || ((this.rel.length > 8) && (this.rel == el.rel));
    });
});

var confirmClick = function(text){
	return confirm(text);
}

var submit = function(caller){
	$(caller).closest('form').submit();
}

var closeSelected = function(caller){
	setAction(caller, "close");
}
var openSelected = function(caller){
	setAction(caller, "open");
}
var setAction = function(caller, action){
	$(caller).closest("form").find(".action").val(action);
	submit(caller);
}


