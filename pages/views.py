import os.path

from django.http import HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponse, HttpResponseServerError
from django.shortcuts import render
from django.conf import settings

from turf.models import *
from .utils import pdf_generator

# Create your views here.

def index(request):
    """
    Simple view that shows form for selecitng the type of turf to show user

    :param request:
    :return:
    """
    return render(request, 'pages/index.html')

def result(request):
    """
    Handles results from the search feature on the homepage
    Calls pdf_generator to generate the pdf packet

    :param request: request from browser
    :return:
    """
    if request.method == 'POST':
        form_data = request.POST.dict()
        session_key = request.session.session_key
    else:
        return HttpResponseNotAllowed

    if not form_data.get('userCategory'):
        return HttpResponseBadRequest


    results= TurfType.objects.filter(category__name=form_data.get('userCategory'))[:3]

    if form_data.get("petFriendly"):
        results.exclude(pet_friendly=False)
    elif form_data.get("sportsField"):
        results.exclude(sports_field=False)

    context = {"results": results}

    if not pdf_generator(request, results, session_key):
        return HttpResponseServerError

    return render(request, 'pages/results.html', context)


def download_packet(request):
    """
    Pulls session key from browser cookies and uses that to find the right packet to give to the user.
    Then downloads the packet for the user.
    """


    session_key = request.session.session_key
    packet_path = os.path.join(settings.BASE_DIR, "media", f"packet__{session_key}.pdf")

    with open(packet_path, "rb") as f:
        response = HttpResponse(f, content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="packet.pdf"'
    return response
