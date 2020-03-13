from django.conf import settings
from django.utils import timezone
import datetime
import math

from .choices import MembershipType
from .models import BikeHires, UserDiscounts

class CostCalculator():
    """ This class is responsible for calculating the cost of a bike ride based on:
        1. User member type
        2. Duration of the bike ride
        3. Whether or not a discount was applied to the journey
    """
    
    def __init__(self, hire: BikeHires):
        self.hire = hire
        
    def calculate_cost(self):
        """ Main function. Calculates the cost of the bike ride for the user, after considering
            the duration of the ride, the user's membership type, and after applying any discounts
        """
        
        user = self.hire.user
        membership = user.membership_type
        basic_cost = self._get_basic_cost(membership)
        max_time = settings.STANDARD_CHARGE_TIME_MAX
        saved_with_discount = 0 # default saved via a discount
        duration = self.hire.get_duration()

        if duration <= max_time:
            return self.apply_discount(basic_cost)
        
        minutes_exceeded = duration - max_time
        additional_charges = self.calculate_penalty(minutes_exceeded)
        
        total = basic_cost + additional_charges
        
        # apply the discount if applicable
        return self.apply_discount(total)

    def apply_discount(self, total):
        discount = self.hire.discount_applied
        saved_with_discount = 0
        if discount is not None and timezone.now().date() <= discount.date_to:
            saved_with_discount = total - (total * discount.discount_amount)
            total *= discount.discount_amount
        return total, saved_with_discount

    def calculate_penalty(self, minutes_exceeded: datetime.datetime):
        """ Calculates additional charges if the duration of the hire exceeded 30 minutes.
            (30 minutes is the maximum standard ride time)
        """

        interval = settings.TIME_EXCEEDED_INTERVAL
        charge_per_interval = settings.CHARGE_PER_INTERVAL
        number_intervals  = math.ceil(minutes_exceeded / interval)
        return charge_per_interval * number_intervals

    def _get_basic_cost(self, membership: int):
        charges = settings.BASIC_CHARGES 
        if membership == MembershipType.STANDARD:
            return charges['standard']
        elif membership == MembershipType.STUDENT:
            return charges['student']
        elif membership == MembershipType.STAFF:
            return charges['staff']
        elif membership == MembershipType.PENSIONER:
            return charges['pensioner']