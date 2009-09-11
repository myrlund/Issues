from economy.invoices.models import *
from django.http import Http404, HttpResponseRedirect
from economy.contract.models import Contract
from economy.contract.helpers import *

def form(request, project_id, contract_code, form_class, model, number=None):
    contract = load_contract(contract_code)
    if number:
        instance = model.objects.get(number=int(number), contract=contract)
        cancel = instance.get_absolute_url()
    else:
        if not contract:
            raise Http404()
        instance = model(contract=contract)
        cancel = contract.get_absolute_url()
        
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            new = form.save()
#            print form.status
            return HttpResponseRedirect(new.get_absolute_url())
    else:
        form = form_class(instance=instance) 
    return render_contract_response(get_template_dir(model)+"form.html", contract_code, {
        "form": form,
        "cancel": cancel,
    }, request)

def list(request, project_id, contract_code, model):
    objects = model.objects.filter(contract__code=contract_code)
    classname = model.__name__.lower()
    return render_contract_response(get_template_dir(model)+"list.html", contract_code, {
        model.__name__.lower()+"s": objects,
    }, request)

def show(request, project_id, contract_code, model, number):
    contract = load_contract(contract_code)
    instance = model.objects.get(contract=contract, number=int(number))
    return render_contract_response(get_template_dir(model)+"show.html", contract_code, {
        model.__name__.lower(): instance,
    }, request)

def show_invoice(request, project_id, contract_code):
    return Http404()

def invoice_form(request, project_id, contract_code):
    return Http404()
