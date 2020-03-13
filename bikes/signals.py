from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from .models import UserProfile, BikeHires
from reports.models import LocationBikeCount

@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """ Creates a UserProfile instance whenever a new User is created """
    if created:
        # The instance arg is the User instance that triggered the signal
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()

@receiver(pre_save, sender=BikeHires)
def create_bikecount(sender, instance, **kwargs):
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        last_count = LocationBikeCount.objects.filter(location=instance.start_station).last().count
        LocationBikeCount.objects.create(
            location=instance.start_station, datetime=instance.date_hired, count=last_count - 1
        )
        if instance.end_station is not None:
            last_count = LocationBikeCount.objects.filter(location=instance.end_station).last().count
            LocationBikeCount.objects.create(
                location=instance.end_station, datetime=instance.date_returned, count=last_count + 1
            )
    else:
        if not obj.end_station == instance.end_station:
            # TODO: test this
            last_count = LocationBikeCount.objects.filter(location=obj.start_station).last().count
            LocationBikeCount.objects.create(
                location=obj.start_station, datetime=obj.date_hired, count=last_count - 1
            )
            last_count = LocationBikeCount.objects.filter(location=instance.end_station).last().count
            LocationBikeCount.objects.create(
                location=instance.end_station, datetime=instance.date_returned, count=last_count + 1
            )
