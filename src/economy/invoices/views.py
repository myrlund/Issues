# -*- coding: utf8 -*-

from economy.invoices.models import *
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.db.models import Max
from economy.contract.models import Contract
from economy.contract.helpers import *
from django.shortcuts import render_to_response

def form(request, project_id, contract_code, model, form_class, number=None):
    project = load_project(project_id)
    contract = load_contract(contract_code, project)
    print contract
    dateform = None
    if request.REQUEST.has_key("next"):
        next = request.REQUEST["next"]
    else:
        next = None
    if number:
        try:
            instance = model.objects.get(contract=contract, id=int(number))
        except model.DoesNotExist:
            raise Http404()
    else:
        contract = load_contract(contract_code)
        if not contract:
            raise Http404()
        instance = model(contract=contract)
    
    error = False
    if request.method == "POST":
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            if request.POST.has_key("status"):
                new = form.save(int(request.POST["status"]))
            else:
                new = form.save()
            if model == Change:
                dateform = ChangeStatusDateForm(request.POST, instance=new.status_date())
                if dateform.is_valid():
                    dateform.save()
                else:
                    print dateform.errors
                    error = True
            modelname = model.__name__.lower()
            next = new.contract.get_absolute_url()+"?highlight="+modelname+"_"+str(new.id)+"#"+modelname+"s"
            if not error:
                return HttpResponseRedirect(next)
    else:
        form = form_class(instance=instance)
        if model == Change:
            dateform = ChangeStatusDateForm(instance=instance.status_date()) 
    return render_contract_response(get_template_dir(model)+"form.html", contract_code, project_id, {
        "instance": instance,
        "dateform": dateform, 
        "form": form,
        "next": next,
    }, request)

def list(request, project_id, contract_code, model):
    objects = model.objects.filter(project_id=project_id, contract__code=contract_code)
    return render_contract_response(get_template_dir(model)+"list.html", contract_code, {
        "objects": objects,
    }, request)

def show(request, project_id, contract_code, cls, number):
    project = load_project(project_id)
    model = cls.objects.get(contract__project__id=project_id, contract__code=contract_code, number=number)
    return render_contract_response(get_template_dir(cls)+"show.html", contract_code, {cls.__name__.lower(): model}, request)


def show_changes(request, project_id, contract_code):
    return show(request, project_id, contract_code, Change)
def show_invoices(request, project_id, contract_code):
    return show(request, project_id, contract_code, Invoice)

def show_change(request, project_id, contract_code, number):
    return show(request, project_id, contract_code, Change, number)
def show_invoice(request, project_id, contract_code, number):
    return show(request, project_id, contract_code, Invoice, number)

def edit_change(request, project_id, contract_code, number):
    return form(request, project_id, contract_code, Change, ChangeForm, number)
def edit_invoice(request, project_id, contract_code, number):
    return form(request, project_id, contract_code, Invoice, InvoiceForm, number)

def new_change(request, project_id, contract_code):
    return form(request, project_id, contract_code, Change, ChangeForm)
def new_invoice(request, project_id, contract_code):
    return form(request, project_id, contract_code, Invoice, InvoiceForm)

def get_change(change_id):
    try:
        return Change.objects.get(id=change_id)
    except Change.DoesNotExist, ChangeStatus.DoesNotExist:
        raise Http404()

def getstatusdate(request, change_id, status):
    change = get_change(change_id)
    try:
        status = ChangeStatus.objects.get(id=int(status))
    except ChangeStatus.DoesNotExist:
        raise Http404()
    try:
        return HttpResponse(datetime.strftime(change.status_date(status).date, "%Y-%m-%d"))
    except Exception as e:
        return HttpResponse("En intern feil oppsto: %s" % e)

def getchangenumber(request, contract_id):
    try:
        contract = Contract.objects.get(id=contract_id)
    except:
        raise Http404()
    try:
        numbers = Change.objects.filter(contract=contract).aggregate(max=Max("number"))
        print numbers
        n = (numbers["max"] or 0) + 1
    except Exception as e:
        print e
        n = 1
    return HttpResponse(n)

def set_invoiced(request, change_id):
    change = get_change(change_id)
    if request.REQUEST.has_key("invoiced"):
        change.invoiced = request.REQUEST["invoiced"] == "true"
        change.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("FEIL")
        
def set_status(request, change_id):
    change = get_change(change_id)
    try:
        status_id = request.REQUEST["status_id"]
        raw_date = request.REQUEST["status_date"]
    except:
        return HttpResponse("Nøkkel mangler!")
    
    try:
        status = ChangeStatus.objects.get(id=status_id)
        change.status = status
        change.save()
        
        date = datetime.strptime(raw_date, "%Y-%m-%d").date()
        sd = change.status_date()
        sd.date = date
        sd.save()
    except Exception as e:
        return HttpResponse(e)
    
    return HttpResponse("OK")
