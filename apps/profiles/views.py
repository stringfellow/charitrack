from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from profiles.models import Profile
from tracker.models import Charity


@login_required
def profile_home(request):

    profile = request.user.get_profile()
    donations = request.user.donations.all().select_related('charity')
    charities = Charity.objects.filter(donation__in=donations).distinct()
    tags = {}

    for charity in charities:
        for tag in charity.tags.all():
            tags[tag] = tags.setdefault(tag, 0) + 1

    tag_max = 0
    tag_max_name = ""
    tag_range = set([])
    for tag, value in tags.items():
        if value > tag_max:
            tag_max = value
            tag_max_name = tag
        tag_range.add(value)

    return render_to_response(
        "profiles_home.html",
        {
            'profile': profile,
            'tags': tags,
            'tag_range': len(tag_range),
            'tag_max_name': tag_max_name,
        },
        context_instance=RequestContext(request)
    )


