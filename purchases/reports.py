''' Reporting module for Purchases '''
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone

from xhtml2pdf import pisa


from .models import Purchase, PurchaseDetail


def link_callback(uri):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    s_url = settings.STATIC_URL      # /static/
    s_root = settings.STATIC_ROOT    # /home/userX/project_static/
    m_url = settings.MEDIA_URL       # /static/media/
    m_root = settings.MEDIA_ROOT     # /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(m_url):
        path = os.path.join(m_root, uri.replace(m_url, ""))
    elif uri.startswith(s_url):
        path = os.path.join(s_root, uri.replace(s_url, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (s_url, m_url)
        )
    return path


def report_purchases(request):
    ''' Generate a pdf with all purchases '''
    template_path = 'purchases/purchases_print_all.html'
    today = timezone.now()

    purchases = Purchase.objects.all()
    context = {
        'obj': purchases,
        'today': today,
        'request': request
        }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


def report_purchase(request, purchase_pk):
    ''' Generate a pdf with a purchase passing a pk '''
    template_path = 'purchases/purchase_print_one.html'
    today = timezone.now()
    purchase = Purchase.objects.filter(pk=purchase_pk).first()
    if purchase:
        detail = PurchaseDetail.objects.filter(purchase=purchase)
    else:
        detail = {}

    context = {
        'detail': detail,
        'purchase': purchase,
        'today': today,
        'request': request
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="report.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # to alow to save the file pdf instead of show it

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response, link_callback=link_callback)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
