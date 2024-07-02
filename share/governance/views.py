from django.shortcuts import render
from django.http import JsonResponse 
from web3 import Web3, HTTPProvider
import json
import os
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from borrow.web3 import get_list_end_proposals, get_list_active_proposals

def load_contract_abi():
    abi_path = os.path.join(settings.STATICFILES_DIRS[0], 'abi', 'ShareTokenABI.json')
    with open(abi_path, 'r') as file:
        contract_abi = json.load(file)
    return contract_abi

def create_proposal(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        deadline = request.POST.get('deadline')
        return HttpResponseRedirect(reverse('admin_dashboard'))
    return render(request, 'governance/create_proposal.html')

def admin_show_all_proposal(request):
    end_proposals = get_list_end_proposals()
    active_proposals = get_list_active_proposals()
    return render(request, 'governance/admin_proposal_list.html', {'end_proposals': end_proposals, 'active_proposals': active_proposals})

def user_proposals_list(request, filter):
    if filter == 'active':
        proposals = get_list_active_proposals()
    elif filter == 'ended':
        proposals = get_list_end_proposals()
    else:
        proposals = []

    context = {
        'proposals': proposals,
        'filter': filter,
    }

    return render(request, 'governance/user_proposal_list.html', context)