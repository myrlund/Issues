from django.http import HttpResponseRedirect

from economy.contract.models import Contract, ContractForm
from economy.contract.helpers import render_project_response, load_project

def list_contracts(request, project_id):
    pagetitle = "Sammenstilling og overordnet budsjett - sluttprognose"
    return render_project_response("overview.html", project_id, {"pagetitle": pagetitle}, request)

def show_contract(request, project_id, contract_code):
    contract = Contract.objects.get(code=contract_code)
    return render_project_response("contract/show.html", project_id, {
        "contract": contract,
        "pagetitle": "%s: %s" % (contract.code, contract.company),
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
