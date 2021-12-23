import logging

from django.utils.datastructures import MultiValueDictKeyError
from stravalib.client import Client
from allauth.socialaccount.models import SocialApp

import challenge.settings

logger = logging.getLogger()


def get_subscription():
    client = Client()
    strava_app = SocialApp.objects.get(name='Strava')
    subscriptions = client.list_subscriptions(client_id=strava_app.client_id, client_secret=strava_app.secret)
    subscription_count = 0
    for subscription in subscriptions:
        subscription_count += 1
        logger.info(f"Subscription present with url {subscription.callback_url} created at {subscription.created_at}")
    if not subscription_count:
        logger.warning("There is currently no Strava webhook subscription set up")
        client.create_subscription(
            client_id=strava_app.client_id,
            client_secret=strava_app.secret,
            callback_url=f"https://{challenge.settings.ALLOWED_HOSTS[0]}/strava/callback/{challenge.settings.STRAVA_VERIFY_TOKEN}",
            verify_token=challenge.settings.STRAVA_VERIFY_TOKEN
        )


def verify_callback(request):
    client = Client()
    try:
        strava_request = {
            k: request.GET[k]
            for k in ("hub.challenge", "hub.mode", "hub.verify_token")
        }
        logger.info("Handled valid Strava subscription callback")
        return client.handle_subscription_callback(
            strava_request,
            verify_token=challenge.settings.STRAVA_VERIFY_TOKEN
        )
    except (AssertionError, MultiValueDictKeyError):
        logger.warning("Handled invalid Strava subscription callback")


def handle_callback(request):
    client = Client()
    update = client.handle_subscription_update(request.body)
    logger.info(f"Handled Strava subscription callback for {update.owner_id}")
    return update.owner_id
