# -*- coding: utf8 -*-

from django.contrib.contenttypes.models import ContentType

from fokus.issue.helpers import render_project_response, get_project
from fokus.search.forms import SearchForm
from fokus.issue.helpers import project_tabs

def search(request, project_number):
    project = get_project(project_number)
    pagetitle = u"Søk"
    
    q = False
    types = None
    
    # Load tabs from project home
    tabs = project_tabs(project)
    tabs[2]["active"] = True
    
    categories = None
    
    if request.GET.has_key('q'):
        q = request.GET['q']
        form = SearchForm(request.GET)
        
        if form.is_valid():
            if request.GET.has_key('types'):
                types = ContentType.objects.filter(id__in=form.cleaned_data['types'])
            
            print "TYPES: %s" % types
            
            project = get_project(project_number)
            categories = project.index.search(q, types)
            
            hide_search = categories and q
            
            return render_project_response(request, 'search/results.html', project_number, locals())
    else:
        form = SearchForm()
    
    hide_search = categories and q
    
    return render_project_response(request, 'search/search.html', project_number, locals())
    