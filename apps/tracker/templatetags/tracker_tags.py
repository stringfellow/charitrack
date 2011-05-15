from datetime import timedelta, datetime

from django.db.models import Sum
from django.template import taglibrary, Node, Variable
from django.contrib.auth.models import User

from tracker.models import Charity, Donation



class UserCharityDonationsNode(Node):
    """Get all the donations for a user, charity in range."""

    def __init__(self, user, charity, date_range, context_var_name):
        self.user = Variable(user)
        self.charity = Variable(charity)
        self.date_range = date_range
        self.context_var_name = context_var_name

    def render(self, context):
        user = self.user.resolve(context)
        charity = self.charity.resolve(context)

        delta = datetime.now() - timedelta(self.date_range)


        donations = Donation.objects.filter(
            user=user,
            charity=charity,
            date__gte=delta,
        )

        total = donations.aggregate(Sum('amount'))

        context[self.context_var_name] = {
            'donations': donations,
            'total': total,
        }

        return ''






