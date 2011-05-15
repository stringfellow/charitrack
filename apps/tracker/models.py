import os

from django.db import models
from django.contrib.auth.models import User
from django.utils import safestring
from django.core.urlresolvers import reverse

from tagging.models import Tag, TaggedItem
from tagging.utils import parse_tag_input

from tracker.utils import find_info
# Create your models here.


PERIODS = (
            ('YEARLY', "Yearly"),
            ('MONTHLY', "Monthly"),
            ('WEEKLY', "Weekly"),
        )


class Charity(models.Model):

    name = models.CharField(max_length=200)
    site = models.URLField(null=True, blank=True)
    description = models.TextField(default="")
    twitter = models.CharField(null=True, blank=True, max_length=40)
    facebook = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    number = models.PositiveIntegerField(null=True, blank=True)
    number_other = models.PositiveIntegerField(null=True, blank=True)
    logo = models.CharField(max_length=254, null=True, blank=True)

    def get_donators(self):
        donations = Donation.objects.filter(charity=self).select_related('user')
        users = User.objects.filter(donations__in=donations).distinct()
        return users

    def _get_tags(self):
        return Tag.objects.get_for_object(self)

    def _set_tags(self, tag_list):
        Tag.objects.update_tags(self, tag_list)

    def get_tag_list(self):
        return parse_tag_input(self.tags)

    tags = property(_get_tags, _set_tags)

    @property
    def related(self):
        return TaggedItem.objects.get_related(self, Charity)

    def __unicode__(self):
        return unicode(self.name)

    def scrape(self, save=True):
        if self.site:
            try:
                links, number, logo = find_info(self.site)
                self.number = number
                self.twitter = links['twitter']
                self.facebook = links['facebook']
                self.logo = logo

                if save:
                    self.save()
            except Exception, e:
                print e


    class Meta:
        verbose_name_plural="Charities"


class Donation(models.Model):
    """
    a one-time donation.
    together, these make a pledge
    """
    user = models.ForeignKey(User, related_name="donations")
    charity = models.ForeignKey(Charity)
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        ordering = ('-date',)

    def __unicode__(self):
        return unicode("%s donated %s%s to %s" % (self.user.username.title(), self.user.get_profile().currency, self.amount, self.charity))

    def full_link_str(self):
        template = """
        <a href="%s">%s</a> donated %s%s to <a href="%s">%s</a>
        """ % (
                reverse('pledger', args=[self.user]), self.user.username.title(),
                self.user.get_profile().currency, self.amount,
                reverse('charity', args=[self.charity]), self.charity
            )

        return safestring.mark_safe(template)


    def no_charity_link_str(self):

        template = """
        <a href="%s">%s</a> donated %s%s
        """ % (
                reverse('pledger', args=[self.user]), self.user.username.title(),
                self.user.get_profile().currency, self.amount,
            )

        return safestring.mark_safe(template)

    def no_donator_link_str(self):

        template = """
         %s%s to <a href="%s">%s</a>
        """ % (
                self.user.get_profile().currency, self.amount,
                reverse('charity', args=[self.charity]), self.charity
            )

        return safestring.mark_safe(template)



class Pledge(models.Model):
    """
    A set of Donations..
    """

    user = models.ForeignKey(User)
    charity = models.ForeignKey(Charity)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    repetitions = models.PositiveIntegerField(null=True, blank=True)
    period = models.CharField(choices=PERIODS, max_length=25)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    indefinite = models.BooleanField(default=True)
    donations = models.ManyToManyField(Donation, null=True, blank=True)

    def __unicode__(self):
        return unicode("%s pledges %s%s to %s" % (self.user, self.user.get_profile().currency,  self.amount, self.charity))