# Create your views here.
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required

from tagging.models import TaggedItem, Tag

from tracker.models import Charity, Donation, Pledge
from tracker.forms import CharityDonationForm


def charities(request):

    return render_to_response(
        "charities.html",
        {
            "charities": Charity.objects.all(),
        },
        context_instance=RequestContext(request)
    )


def charity(request, charity_name):

    charity = get_object_or_404(Charity, name=charity_name)

    return render_to_response(
        "charity.html",
        {
            "charity": charity,
            "donations": charity.donation_set.all(),
        },
        context_instance=RequestContext(request)
    )


def charity_make_donation(request, charity_name):

    charity = get_object_or_404(Charity, name=charity_name)
    new_donation_form = CharityDonationForm()

    return render_to_response(
        "charity_make_donation.html",
        {
            "new_donation_form": new_donation_form,
            "charity": charity,
            "donations": charity.donation_set.filter(user=request.user),
        },
        context_instance=RequestContext(request)
    )


def charities_tag_user(request, tag_name, user_name):
    tag = Tag.objects.get(name=tag_name)
    pledger = get_object_or_404(User, username=user_name)
    donations = pledger.donations.all().select_related('charity')
    tagged_charities = TaggedItem.objects.get_union_by_model(
        Charity,
        [tag]
    )
    charities = Charity.objects.filter(
        donation__in=donations,
        pk__in=[ch.pk for ch in tagged_charities]
    ).distinct()

    return render_to_response(
        "charities_tag_user.html",
        {
            'charities': charities,
            'tag': tag,
        },
        context_instance=RequestContext(request)
    )


@staff_member_required
def charity_update_tags(request, charity_pk):

    charity = get_object_or_404(Charity, pk=charity_pk)

    if request.method == "POST":
        tags_str = request.POST.get("add_tags", "")

        charity.tags = tags_str
        charity.save()

    return HttpResponseRedirect(reverse("charity", args=[charity.name]))


def pledgers(request):
    pass


def pledger(request, pledger_name):

    pledger = get_object_or_404(User, username=pledger_name)

    donations = pledger.donations.all().select_related('charity')
    charities = Charity.objects.filter(donation__in=donations).distinct()

    return render_to_response(
        "pledger.html",
        {
            "pledger":pledger,
            "donations": donations,
            "charities": charities,
        },
        context_instance=RequestContext(request)
    )


def duplicate_donation(request, donation_pk):

    donation = get_object_or_404(Donation, pk=donation_pk)

    pass
