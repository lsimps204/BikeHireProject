from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from .choices import MembershipType, BikeStatus
from .models import UserProfile, Bikes,BikeRepairs, Location,Discounts

# For registering new users
class RegistrationForm(forms.ModelForm):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', 'Only alphanumeric characters are allowed.')

    username = forms.CharField(min_length=4, max_length=50, validators=[alphanumeric], widget=forms.TextInput(attrs={'autofocus':'true'}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput(), label="Confirm password")
    membership_type = forms.ChoiceField(choices=MembershipType.CHOICES) 

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).count() > 0:
            raise ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if User.objects.filter(email=email).count() > 0:
            raise ValidationError("Email already exists")
        return email
    
    def clean_password_confirm(self):
        pw1 = self.cleaned_data['password']
        pw2 = self.cleaned_data['password_confirm']

        if pw1 and not pw1 == pw2:
            raise ValidationError("Passwords don't match")
        return pw2


    # Override to hash password by using the User model manager's 'create_user' method
    def save(self, *args, **kwargs):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password']
        )
        user.userprofile.membership_type = self.cleaned_data['membership_type']
        user.userprofile.save()
        return user

class UserProfileForm(forms.ModelForm):
    """ Hidden form allowing profile picture uploads """
    class Meta:
        model = UserProfile
        fields = ('profile_pic',)

class ReturnBikeForm(forms.Form):
    hire_id = forms.IntegerField(widget=forms.HiddenInput())
    location = forms.ModelChoiceField(queryset=Location.objects.order_by('station_name'))
    discount = forms.CharField(required=False, label="Discount Code")

class MoveBikeForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.order_by('station_name'), required=True)
    new_location = forms.ModelChoiceField(queryset=Location.objects.order_by('station_name'), label = "New station", required=True)


    def clean(self):
        cleaned_data = super().clean()
        loc = cleaned_data.get('location')
        loc_new = cleaned_data.get('new_location')

        if loc and loc_new:
            if loc == loc_new:
                raise forms.ValidationError("Cannot move a bike to the same location as it previously resided")


class BikeHireForm(forms.Form):
    bike_id = forms.IntegerField()

class BikeRepairsForm(forms.ModelForm):
    """ Form that reports a bike for repair """

    class Meta:
        model= BikeRepairs
        fields=('bike',)

class RepairBikeForm(forms.Form):
    """ Form that repairs a bike """
    bike = forms.ModelChoiceField(queryset=Bikes.objects.filter(status=BikeStatus.BEING_REPAIRED))

class DiscountsForm(forms.ModelForm):
    date_from = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=('%d-%m-%Y', )
    )
    date_to = forms.DateField(
        widget=forms.DateInput(format='%d-%m-%Y'),
        input_formats=('%d-%m-%Y', )
    )
    discount_amount = forms.FloatField(label="Discount Amount (%)")

    class Meta:
        model= Discounts
        fields=('__all__')

    def clean_discount_amount(self):
        """ Bind the discount to between 0 and 100% """
        amount = self.cleaned_data.get('discount_amount')
        if amount is None:
            raise ValidationError("No discount percentage specified")
        if not 0 < amount <= 100:
            raise ValidationError("Invalid discount entered")

        # reduce to fraction
        amount /= 100
        return amount

    def clean(self):
        """ Check date-to is after date-from """
        cleaned_data = super().clean()
        dfrom = cleaned_data.get('date_from')
        dto = cleaned_data.get('date_to')

        if dfrom is None or dto is None:
            raise ValidationError("No dates entered for discount")
        if dfrom > dto:
            raise ValidationError("Date from cannot be greater than date to.")

    def __init__(self, *args, **kwargs):
        """ Disable autocomplete on the date fields """
        super().__init__(*args, **kwargs)
        self.fields['date_from'].widget.attrs.update({"autocomplete": "off"})
        self.fields['date_to'].widget.attrs.update({"autocomplete": "off"})