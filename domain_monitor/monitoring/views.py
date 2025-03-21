import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Domain, DomainStatus, DomainHistory
from .forms import DomainForm
import requests
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def dashboard(request):
    """
    View to display the dashboard with the list of domains and their statuses.
    Only accessible to logged-in users.
    """
    domains = DomainStatus.objects.select_related('domain').filter(domain__user=request.user)
    return render(request, 'monitoring/dashboard.html', {'domains': domains})

@login_required
def add_domain(request):
    """
    View to handle adding a new domain.
    Displays a form for adding a domain and processes the form submission.
    Only accessible to logged-in users.
    """
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save(commit=False)
            domain.user = request.user
            domain.save()
            return redirect('dashboard')
    else:
        form = DomainForm()
    return render(request, 'add_domain.html', {'form': form})

@login_required
def delete_domain(request, domain_id):
    """
    View to handle deleting a domain.
    Deletes the specified domain and redirects to the index page.
    Only accessible to logged-in users.
    """
    domain = get_object_or_404(Domain, pk=domain_id)
    if domain:
        domain.delete()
    return redirect('index')

def check_domain_status(domain):
    """
    Function to check the status of a domain.
    Sends a HEAD request to the domain and returns the status code.
    Logs an exception if the request fails.
    """
    try:
        status_code = str(requests.head(f'http://{domain}', headers={'User-Agent': 'Foo bar'}, allow_redirects=True).status_code)
        return status_code
    except requests.RequestException:
        logger.exception(f"Failed to check status for domain: {domain}")
        return None