from datetime import timedelta, datetime
import re

from django.db.models import Sum
from django.template import Node, Variable, Library, TemplateSyntaxError
from django.contrib.auth.models import User

from tracker.models import Charity, Donation

register = Library()


class UserCharityDonationsNode(Node):
    """Get all the donations for a user, charity in range."""

    def __init__(self, user, charity, day_range, context_var_name):
        self.user = Variable(user)
        self.charity = Variable(charity)
        self.day_range = day_range
        self.context_var_name = context_var_name

    def render(self, context):
        user = self.user.resolve(context)
        charity = self.charity.resolve(context)
        delta = datetime.now() - timedelta(int(self.day_range))

        donations = Donation.objects.filter(
            user=user,
            charity=charity,
            date__gte=delta,
        )

        total = donations.aggregate(Sum('amount'))['amount__sum']

        context[self.context_var_name] = {
            'donations': donations,
            'total': "%s%s" % (
                user.get_profile().currency,
                total,
            )
        }

        return ''

@register.tag
def user_charity_donations(parser, token):
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError(
            "%r tag requires arguments" % token.contents.split()[0])
    m = re.search(r'(.*?) (.*?) (.*?) as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError(
            "%r tag requires all arguments "
            "(user charity day_range as var_name)" % tag_name)
    user, charity, date_range, var_name = m.groups()
    #if not (
    #    date_range[0] == date_range[-1] and
    #    date_range[0] in
    #    ('"', "'")):
    #    raise TemplateSyntaxError(
    #        "%r tag's date_range argument should be in quotes" % tag_name)
    return UserCharityDonationsNode(user, charity, date_range[1:-1], var_name)






