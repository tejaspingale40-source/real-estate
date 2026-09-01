from properties.models import SiteSettings

def site_settings(request):
    settings_obj = SiteSettings.objects.first()
    if not settings_obj:
        settings_obj = SiteSettings.objects.create(
            site_name="PERFECT HOMES",
            tagline="REAL ESTATE ADVISORY • RERA CERTIFIED",
            phone="+91 98765 43210",
            email="info@perfecthomes.com",
            address="101 Prime Plaza, VIP Road, Pune & Solapur, Maharashtra"
        )
    return {
        'site_settings': settings_obj
    }
