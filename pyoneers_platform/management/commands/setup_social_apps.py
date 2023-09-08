from django.core.management.base import BaseCommand
from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.db import IntegrityError
from django.conf import settings


class Command(BaseCommand):
    """
    Create or update social apps from a settings variable.

    This function reads from `SOCIAL_APPS_CONFIG` defined in Django `settings.py`
    to dynamically create or update social apps using the allauth package.
    Each social app is identified by its provider (e.g., 'google', 'discord').

    Raises
    ------
    IntegrityError
        If the social app is already associated with another site.
    Exception
        For other unspecified errors.

    Examples
    --------
    To use this function, define `SOCIAL_APPS_CONFIG` in `settings.py`:

    SOCIAL_APPS_CONFIG = {
        'google': {
            'name': 'Google',
            'client_id': 'YOUR_GOOGLE_CLIENT_ID',
            'secret': 'YOUR_GOOGLE_SECRET',
        },
        'discord': {
            'name': 'Discord',
            'client_id': 'YOUR_DISCORD_CLIENT_ID',
            'secret': 'YOUR_DISCORD_SECRET',
        },
    }
    """

    help = "Sets up social apps dynamically based on SOCIAL_APPS_CONFIG in settings."

    def handle(self, *args, **kwargs):
        self.stdout.write("Setting up social apps...")

        if not hasattr(settings, "SOCIAL_APPS_CONFIG"):
            self.stdout.write(
                self.style.ERROR(
                    "SOCIAL_APPS_CONFIG not found in settings. Skipping setup."
                )
            )
            return

        social_apps_config = settings.SOCIAL_APPS_CONFIG
        site = Site.objects.get_current()

        for provider, config in social_apps_config.items():
            try:
                app, created = SocialApp.objects.update_or_create(
                    provider=provider,
                    defaults={
                        "name": config.get("name", provider),
                        "client_id": config.get("client_id", ""),
                        "secret": config.get("secret", ""),
                    },
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"Created social app for {provider}.")
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(f"Updated social app for {provider}.")
                    )

                app.sites.add(site)

            except IntegrityError:
                self.stdout.write(
                    self.style.ERROR(
                        f"Couldn't create or update social app for {provider}. "
                        f"It might already be associated with another site."
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
