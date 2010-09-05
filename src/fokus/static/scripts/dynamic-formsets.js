function updateElementIndex(el, prefix, ndx) {
	var id_regex = new RegExp('(' + prefix + '-\\d+)');
	var replacement = prefix + '-' + ndx;
	if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
	if (el.id) el.id = el.id.replace(id_regex, replacement);
	if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    var row = $('.dynamic-form:last').clone(true).get(0);
    $(row).removeAttr('id').insertAfter($('.dynamic-form:last')).children('.hidden').removeClass('hidden');
    $(row).find(':input').each(function() {
	    updateElementIndex(this, prefix, formCount);
	    $(this).val('');
    });
    $(row).find('.delete-row').click(function() {
	    deleteForm(this, prefix);
    });
    $('#id_' + prefix + '-TOTAL_FORMS').val(formCount + 1);
    return false;
}

function deleteForm(btn, prefix, i) {
	var sure = confirm("Er du sikker på at du ønsker å slette dette bildet?");
	if (sure) {
		var parent = $(btn).closest('.dynamic-form, .imageform');
		parent.find("#id_" + prefix + "-" + i + "-DELETE").val("on");
		parent.hide();
	}
	return false;
}

