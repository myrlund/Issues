from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.forms.models import modelformset_factory

from fokus.update.models import Update
from fokus.issue.models import Issue
from fokus.attachment.models import ImageResource
from fokus.attachment.forms import ImageResourceForm
from fokus.update.forms import UpdateForm

def update_save(request, project_number, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    
    form = UpdateForm(request.POST)
    
    if form.is_valid():
        update = form.save(commit=False)
        update.posted_by = request.user
        
        ImageFormset = modelformset_factory(ImageResource, form=ImageResourceForm, extra=1, can_delete=True)
        formset = ImageFormset(request.POST, request.FILES, prefix=update.parent.id)
        
        if formset.is_valid():
            update.save()
            
            images = formset.save(commit=False)
            for image in images:
                image.parent = update
                image.save()
            
            if update.notify:
                update.notify_subscribers()
            
            messages.success(request, "Oppdateringen ble lagret.")
            
            return HttpResponseRedirect(update.get_absolute_url())
    else:
        print "En feil oppsto. Feil: %s" % formset
        
        messages.error(request, "Det oppsto en feil under lagring av oppdateringen.")
        return HttpResponseRedirect(issue.get_absolute_url())

def update_delete(request, project_number, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    update = get_object_or_404(Update, id=request.REQUEST['update_id'])
    update.delete()
    
    messages.success(request, "Oppdateringen ble slettet.")
    
    return HttpResponseRedirect(issue.get_absolute_url() + "#oppdateringer")
