from django.shortcuts import redirect
from django.urls import NoReverseMatch, resolve, reverse


class DirectToModalRedirectionMiddleware:
    """
    Handles direct access to pages typically displayed in modals.

    If a user directly visits a URL meant for a modal, they are redirected to the homepage.
    The `modal_url` query parameter is added to this URL, prompting the front-end to open the intended page in a modal
    via htmx.

    Example: A direct visit to /accounts/login/ becomes a redirect to /?modal_url=/accounts/login/,
    causing the front-end to display the login in a modal.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.htmx:
            view_name = resolve(request.path_info).url_name
            modal_url = None
            if view_name in [
                "account_login",
                "account_signup",
                "account_reset_password",
                "account_reset_password_from_key",
                "account_confirm_email",
                "account_change_password",
                "account_set_password",
                "account_email",
                "account_logout",
            ]:
                try:
                    # For views that don't need arguments
                    modal_url = reverse(view_name)
                except NoReverseMatch:
                    # Handle views that expect arguments
                    if view_name == "account_reset_password_from_key":
                        uidb36 = request.resolver_match.kwargs.get("uidb36")
                        key = request.resolver_match.kwargs.get("key")
                        modal_url = reverse(view_name, kwargs={"uidb36": uidb36, "key": key})
                    # Add more views that require arguments here as needed
                    # ...
                if modal_url:
                    home_url = reverse("home")
                    return redirect(f"{home_url}?modal_url={modal_url}")
        return response
