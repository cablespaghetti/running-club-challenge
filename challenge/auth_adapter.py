from allauth.socialaccount.adapter import get_account_adapter, DefaultSocialAccountAdapter
from stravalib.client import Client


class DeactivateSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login. Accounts are disabled by default.
        """
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
        return u
