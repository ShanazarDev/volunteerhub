from django.utils import timezone
from django.conf import settings

def common_variables(request):
    """
    Context processor to add common variables to all templates.
    """
    current_year = timezone.now().year
    site_url = f"{request.scheme}://{request.get_host()}"
    
    return {
        'current_year': current_year,
        'site_name': 'VolunteerHub',
        'site_url': site_url,
    }