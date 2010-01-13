# -*- coding: utf8 -*-

from django.http import HttpResponseRedirect, Http404, HttpResponse
    
import re
import datetime

from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from economy.contract.models import * #@UnusedWildImport
from economy.invoices.models import Invoice, Change
from economy.contract.helpers import render_project_response, load_project,\
    load_contract

def project_overview(request):
    projects = Project.objects.all()
    return render_to_response("root.html", {"projects": projects}, RequestContext(request))

def list_contracts(request, project_id):
    project = load_project(project_id)
    data = project.calculate_category_sums()
    data["pagetitle"] = "Sammenstilling og overordnet budsjett - sluttprognose"
    return render_project_response("overview.html", project_id, data, request)

def report(request, project_id):
    project = load_project(project_id)
    date_query = Q()
    if request.REQUEST.has_key("from_date"): # and request.REQUEST["from_date_enabled"]: # _enabled
        date = datetime.datetime.strptime(request.REQUEST["from_date"], "%Y-%m-%d")
        date_query = date_query & Q(invoice__date__gte=date)
    if request.REQUEST.has_key("to_date"): # and request.REQUEST["to_date_enabled"]: # _enabled
        date = datetime.datetime.strptime(request.REQUEST["to_date"], "%Y-%m-%d")
        date_query = date_query & Q(invoice__date__lte=date)
    if request.REQUEST.has_key("type") and request.REQUEST["type"] == "ns":
        return ns_report(request, project, date_query)
    else:
        return normal_report(request, project, date_query)

def ns_report(request, project, date_query=None):
    # Hent gruppert på første tegn
    data = project.calculate_ns_sums()
    return render_to_response("report/ns.html", data, RequestContext(request))

def normal_report(request, project, date_query=None):
    #@todo: Datofiltrering funker ikke skikkelig
    data = project.calculate_category_sums(date_query=date_query)
    # data = {"categories": categories, "total": total}
    return render_to_response("report/normal.html", data, RequestContext(request))

def show_contract(request, project_id, contract_code):
    project = load_project(project_id)
    contract = load_contract(contract_code, project)
    
    csortby = None
    isortby = None
    if request.GET.has_key("csortby") and len(request.GET["csortby"]):
        csortby = request.GET["csortby"]
    if request.GET.has_key("isortby") and len(request.GET["isortby"]):
        isortby = request.GET["isortby"]
    highlight = None
    if request.GET.has_key("highlight"):
        highlight = request.GET["highlight"]
    
    if isortby in Invoice.get_sort_fields():
        invoices = contract.invoice_set.order_by(isortby)
    else:
        invoices = contract.invoice_set.all()
    if csortby in Change.get_sort_fields():
        changes = contract.change_set.order_by(csortby)
    else:
        changes = contract.change_set.all()
    
    # Search through sorted elements
    if request.GET.has_key("iq"):
        iq = get_query(request.GET["iq"], Invoice.get_search_fields())
        invoices = invoices.filter(iq)
    if request.GET.has_key("cq"):
        cq = get_query(request.GET["cq"], Change.get_search_fields())
        changes = changes.filter(cq)
    
    tpl = "contract/show.html"
    if request.GET.has_key("ajax"): # request.is_ajax() or 
        model = request.GET["model"]
        tpl = "%s/ajax.html" % model
    
    cdata = changes.aggregate(amount=Sum("amount"), timediff=Sum("timediff"))
    cdata.update(changes.filter(~Q(status__short=settings.ACCEPTED_SHORT)).aggregate(pending=Sum("amount")))
    cdata.update(changes.filter(status__short=settings.ACCEPTED_SHORT).aggregate(accepted=Sum("amount")))
    idata = invoices.aggregate(amount=Sum("amount"))
    
    return render_project_response(tpl, project_id, {
        "contract": contract,
        "invoices": invoices,
        "changes": changes,
        "pagetitle": "%s: %s" % (contract.code, contract.company),
        "quickedit": request.GET.has_key('quickedit'),
        "highlight": highlight,
        "isortby": isortby,
        "csortby": csortby,
        "cdata": cdata,
        "idata": idata,
    }, request)

def contract_form(request, project_id, contract_code=None):
    project = load_project(project_id)
    contract = None
    if contract_code:
        contract = Contract.objects.get(project=project, code=contract_code)
    else:
        contract = Contract(project=project)
    if request.method == "POST":
        form = ContractForm(request.POST, instance=contract)
        if form.is_valid():
            new_contract = form.save()
            return HttpResponseRedirect(new_contract.get_absolute_url())
    else:
        form = ContractForm(instance=contract)
    return render_project_response("contract/form.html", project_id, {
        "form": form,
        "contract": contract,
        "pagetitle": "Ny kontrakt",
    }, request)

def new_contract(request, project_id):
    return contract_form(request, project_id)
def edit_contract(request, project_id, contract_code):
    return contract_form(request, project_id, contract_code)

def edit_project(request, project_id):
    project = load_project(project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            project = form.save()
            return HttpResponseRedirect(project.get_absolute_url())
    else:
        form = ProjectForm(instance=project)
    return render_to_response("project/form.html", {
        "project": project,
        "form": form,
    }, RequestContext(request))

def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):
    ''' Splits the query string in invidual keywords, getting rid of unecessary spaces
        and grouping quoted words together.
        Example:
        
        >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    
    '''
    return [normspace(' ', (t[0] or t[1]).strip()) for t in findterms(query_string)] 

def get_query(query_string, search_fields):
    ''' Returns a query, that is a combination of Q objects. That combination
        aims to search keywords within a model by testing the given search fields.
    
    '''
    query = None # Query to search for every search term        
    terms = normalize_query(query_string)
    for term in terms:
        or_query = None # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query
    return query
