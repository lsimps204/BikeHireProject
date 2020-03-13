from collections import namedtuple
from datetime import datetime
import random

from django.db.models import F
from django.utils import timezone
import pytz
import geopy.distance

from .cost_calculator import CostCalculator
from .models import *
from reports.models import LocationBikeCount

def return_bike(hire, end_station, user_discount_code):
    hire.end_station = end_station
    hire.date_returned = timezone.now()
    model = Discounts.objects.filter(code=user_discount_code)
    if model.exists():
        model = model.get()
        hire.discount_applied = model
        discount_model = UserDiscounts(user=hire.user, discounts=model, date_used=timezone.now())
    charges, discount = CostCalculator(hire).calculate_cost()
    if hire.discount_applied is not None:
        discount_model.amount_saved = discount
        discount_model.save()
    hire.charges = charges
    hire.save()

    # nullify user's current hire
    hire.user.current_hire = None
    hire.user.add_charges(charges)
    hire.user.save()

    # set bike location
    bike = hire.bike
    bike.location = hire.end_station
    bike.save()

    return hire

def move_bike(bike, new_station):
    
    # set bike location
    old = bike.location
    bike.location = new_station
    
    # update location bike count table for old and new stations
    count = LocationBikeCount.objects.filter(location=old).last().count
    LocationBikeCount.objects.create(
        location=old, datetime=timezone.now(), count=count - 1
    )
    # add 1 to new bike station's count
    count = LocationBikeCount.objects.filter(location=new_station).last().count
    LocationBikeCount.objects.create(
        location=new_station, datetime=timezone.now(), count=count + 1
    )

    bike.save()
    return bike

def repair_bike(bike):
    # change the status of the bike to repaired
    bike.status = 1
    # generate repair "cost" - between 2 and 40 with values <= 30 more likely
    cost = random.randint(2, 40)
    if cost > 30 and random.random() < .5:
        cost = cost // 2
    bike.save()
    return cost

def ride_distance(hire):
    """ Calculates a ride's distance between the start and end stations
        Uses geopy.distance.distance [an implementation of geodesic distance]
        returns namedtuple of distance attributes: kilometres, miles and feet for the distance 
    """
    start, end = hire.start_station, hire.end_station
    Distance = namedtuple('Distance', 'km miles feet')
    if end is not None:
        # extract latitude and longitudes for the start and end stations
        start = start.latitude, start.longitude
        end   = end.latitude, end.longitude
        dist = geopy.distance.distance(start, end) # calculate geodesic distance
        return Distance(km=dist.km, miles=dist.miles, feet=dist.feet)
    return 0 # if end is None

def parse_dates(date_from, date_to):
    """ Creates timezone aware datetime objects from string parameters """
    day_from, month_from, year_from = date_from.split("-")
    day_to, month_to, year_to = date_to.split("-")
    
    _from = datetime(
        year=int(year_from), month=int(month_from), day=int(day_from), tzinfo=pytz.UTC
    )
    _to = datetime(
        year=int(year_to), month=int(month_to), day=int(day_to), tzinfo=pytz.UTC
    )

    return _from, _to