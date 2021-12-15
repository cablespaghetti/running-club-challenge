from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import get_account_adapter, DefaultSocialAccountAdapter
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from stravalib.client import Client
from main.strava import create_update_athlete
from django import forms

import logging


class DeactivateAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        user_email(user, email)
        user_username(user, username)
        if first_name:
            user_field(user, "first_name", first_name)
        if last_name:
            user_field(user, "last_name", last_name)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

        # Deactivate the account
        user.is_active = False

        if commit:
            # Ability not to commit makes it easier to derive from
            # this adapter by adding
            user.save()
            # Create an Athlete
            gender = None
            dob = None
            if 'gender' in data:
                gender = data['gender']
            if 'dob' in data:
                dob = data['dob']
            create_update_athlete(
                user=user,
                gender=gender,
                dob=dob,
            ),

        return user


class DeactivateSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. Accounts are disabled by default.
        """
        logger = logging.getLogger()
        u = sociallogin.user
        u.set_unusable_password()
        if form:
            get_account_adapter().save_user(request, u, form)
        else:
            get_account_adapter().populate_username(request, u)

        # Deactivate the account unless they are in the RRR Strava Club
        u.is_active = False
        if sociallogin.token.app.name == "Strava":
            client = Client()
            client.access_token = sociallogin.token.token
            client.refresh_token = sociallogin.token.token_secret
            client.token_expires_at = sociallogin.token.expires_at
            clubs = client.get_athlete_clubs()
            for club in clubs:
                if club.id == 7686:
                    u.is_active = True
                    break

        sociallogin.save(request)

        # Create an Athlete
        if sociallogin.account.extra_data:
            gender = None
            photo = None
            if 'sex' in sociallogin.account.extra_data and sociallogin.account.extra_data['sex'] in ['F', 'M']:
                gender = sociallogin.account.extra_data['sex']
            if 'profile' in sociallogin.account.extra_data:
                photo = sociallogin.account.extra_data['profile']
        create_update_athlete(user=u, gender=gender, photo=photo)

        return u


class AccountSignupForm(SignupForm):
    first_name = forms.CharField(max_length=150, label='First Name')
    last_name = forms.CharField(max_length=150, label='Last Name')
    GENDER_CHOICES = [
        ('F', 'Female'),
        ('M', 'Male')
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, label="Gender")
    dob = forms.DateField(label="Date of Birth")


class SocialAccountSignupForm(SocialSignupForm):
    dob = forms.DateField(label="Date of Birth")
