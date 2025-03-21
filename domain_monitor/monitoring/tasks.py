from celery import shared_task
from .models import Domain, DomainStatus
import requests

@shared_task
def check_domain_status():
    """
    Periodically checks the status of all domains.
    Updates the DomainStatus model with the response code and response time.
    """
    domains = Domain.objects.all()
    for domain in domains:
        try:
            response = requests.get(domain.name)
            status_code = response.status_code
            response_time = response.elapsed.total_seconds()
            DomainStatus.objects.update_or_create(
                domain=domain,
                defaults={
                    'status': 'OK' if status_code == 200 else 'DOWN',
                    'response_code': status_code,
                    'response_time': response_time,
                }
            )
        except requests.RequestException:
            DomainStatus.objects.update_or_create(
                domain=domain,
                defaults={
                    'status': 'DOWN',
                    'response_code': None,
                    'response_time': None,
                }
            )