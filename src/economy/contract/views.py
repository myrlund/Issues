from django.http import HttpResponseRedirect

from economy.contract.models import Contract, ContractForm, Project
from economy.contract.helpers import render_project_response, load_project
from django.shortcuts import render_to_response
from django.template.context import RequestContext

def project_overview(request):
    projects = Project.objects.all()
    return render_to_response("root.html", {"projects": projects}, RequestContext(request))

def list_contracts(request, project_id):
    pagetitle = "Sammenstilling og overordnet budsjett - sluttprognose"
    return render_project_response("overview.html", project_id, {"pagetitle": pagetitle}, request)

def show_contract(request, project_id, contract_code):
    contract = Contract.objects.get(code=contract_code)
    highlight = None
    if request.GET.has_key("highlight"):
        highlight = request.GET["highlight"]
    return render_project_response("contract/show.html", project_id, {
        "contract": contract,
        "invoices": contract.invoice_set.all(),
        "changes": contract.change_set.all(),
        "pagetitle": "%s: %s" % (contract.code, contract.company),
        "quickedit": request.GET.has_key('quickedit'),
        "highlight": highlight,
    }, request)

def contract_form(request, project_id, contract_code=None):
    project = load_project(project_id)
    contract = None
    if contract_code:
        contract = Contract.objects.get(code=contract_code)
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
        "pagetitle": "Ny kontrakt",
    }, request)

def new_contract(request, project_id):
    return contract_form(request, project_id)
def edit_contract(request, project_id, contract_code):
    return contract_form(request, project_id, contract_code)