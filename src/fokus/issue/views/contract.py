from fokus.issue.helpers import get_project, project_tools, project_tabs,\
    render_project_response, get_contract, tab, render_contract_response


def contract_list(request, project_number, project_slug=None):
    project = get_project(project_number)
    pagetitle = u"Kontrakter"
    
    contracts = project.contract_set.all()
    for contract in contracts:
        contract.my_issues = contract.get_all_issues(request.user)
        contract.my_issues_url = contract.get_my_issues_url(request.user)
    tools = project_tools(project)
    tabs = project_tabs(project)
    tabs[1]["active"] = True
    return render_project_response(request, 'contract/list.html', project_number, locals())

def contract_home(request, project_number, code, project_slug=None):
    contract = get_contract(project_number, code)
    pagetitle = contract
    
    my_open_issues = contract.get_open_issues(request.user)
    my_issues = contract.get_all_issues(request.user)
    tools = [
        tab('edit contract', 'Rediger kontrakt', contract.get_edit_url()),
        tab('new issue', 'Ny sak', contract.get_new_issue_url()),
    ]
    return render_contract_response(request, 'contract/home.html', project_number, code, locals())

def contract_edit(request):
    pass

def contract_delete(request):
    pass

def contract_new(request):
    pass
