from datetime import datetime, date, timedelta

from django.contrib import admin

from tracker.models import Charity, Pledge, Donation


RESOLUTION = {
    'WEEKLY' : 7,
    'MONTHLY': 28,
    'YEARLY' : 365,
    }

class CharityAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        obj.scrape(save=False)
        obj.save()


class DonationAdmin(admin.ModelAdmin):
    list_display = ('user','charity','amount','date')



class PledgeAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        donations = obj.donations.all()

        today = date.today()

        if obj.start_date < today:
            delta = today - obj.start_date

            resolution = RESOLUTION[obj.period]

            if obj.repetitions > 0 or obj.indefinite or obj.end_date > today:
                count = 1 + delta.days / resolution

            elif obj.end_date < today:
                delta = obj.end_date - obj.start_date
                count = 1 + delta.days / resolution

            if count != len(donations):
                for d in range(count):
                    donation = Donation.objects.create(
                                    user=obj.user,
                                    charity=obj.charity,
                                    amount=obj.amount,
                                    date=obj.start_date+timedelta(days=d*resolution)
                                )
                    obj.donations.add(donation)

        obj.save()


admin.site.register(Charity, CharityAdmin)
admin.site.register(Pledge, PledgeAdmin)
admin.site.register(Donation, DonationAdmin)