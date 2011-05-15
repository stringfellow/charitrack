from django.forms import ModelForm

from tracker.models import Donation


class CharityDonationForm(ModelForm):

    class Meta:
        model = Donation
        fields = ('date', 'amount')
