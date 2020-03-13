""" This file will contain choices for the Django Model fields.
    These are very simple classes with attributes representing each possible option for a given field
"""

class UserType:
    CUSTOMER = 1
    OPERATOR = 2
    MANAGER = 3

    """ 
    This CHOICES field below is what is passed to the User.user_type model field. Each tuple has 2 values.
        1. Value that's stored in the database - this is an integer, set to the variables above (1,2,3)
        2. The user-friendly text name that's shown in the HTML templates
    """
    CHOICES = (
        (CUSTOMER, "Customer"),
        (OPERATOR, "Operator"),
        (MANAGER, "Manager")
    )

    @classmethod
    def get_choice(cls, key):
        for choice in cls.CHOICES:
            if choice[0] == key:
                return choice[1]
        return None

class BikeStatus:
    AVAILABLE = 1
    ON_HIRE = 2
    BEING_REPAIRED = 3

    CHOICES = (
        (AVAILABLE, "Available"),
        (ON_HIRE, "Out on hire"),
        (BEING_REPAIRED, "Being repaired")
    )

class MembershipType:
    STANDARD = 1
    STUDENT = 2
    PENSIONER = 3
    STAFF = 4

    CHOICES = (
        (STANDARD, "Standard"),
        (STUDENT, "Student"),
        (PENSIONER, "Pensioner"),
        (STAFF, "Staff")
    )

    @classmethod
    def get_choice(cls, key):
        for choice in cls.CHOICES:
            if choice[0] == key:
                return choice[1]
        return None