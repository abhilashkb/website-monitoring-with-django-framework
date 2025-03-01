import re
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from models import Domain, DomainStatus, DomainHistory
import requests
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def index(request):
    domains = DomainStatus.objects.select_related('domain').filter(domain__user=request.user)
    return render(request, 'monitoring/index.html', {'domains': domains})
@login_required
def add_domain(request):
    if request.method == 'POST':
        domain_name = request.POST['name'].strip()
        if not domain_name:
            return render(request, 'monitoring/add_domain.html', {'error': 'Domain name cannot be empty'})
        if not re.match(r'^[a-zA-Z0-9.-]+$', domain_name):
            return render(request, 'monitoring/add_domain.html', {'error': 'Domain name contains invalid characters'})
        domain = Domain(user=request.user, name=domain_name)
        domain.save()
        return redirect('index')
    return render(request, 'monitoring/add_domain.html')
@login_required
def delete_domain(request, domain_id):
    domain = get_object_or_404(Domain, pk=domain_id)
    if domain:
        domain.delete()
    return redirect('index')


def check_domain_status(domain):
    try:
        status_code = str(requests.head(f'http://{domain}', headers={'User-Agent': 'Foo bar'}, allow_redirects=True).status_code)
        return status_code
    except requests.RequestException:
        logger.exception(f"Failed to check status for domain: {domain}")
        return None