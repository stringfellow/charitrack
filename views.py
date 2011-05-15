# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.models import User

from tracker.models import Charity, Donation, Pledge


def home(request):

    donations = Donation.objects.all()

    return render_to_response(
        "homepage.html",
        {
            "donations": donations,
        },
        context_instance=RequestContext(request)
    )
