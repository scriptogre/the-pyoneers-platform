from django.conf import settings
from django.shortcuts import redirect
from django.urls import resolve, reverse


class DirectToModalRedirectionMiddleware:
    """
    Handles direct access to pages typically displayed in modals.

    If a user directly visits a URL meant for a modal, they are redirected to the homepage.
    The `modal_url` query parameter is added to this URL, prompting the front-end to open the intended page in a modal
    via htmx.

    Example: A direct visit to /login/ becomes a redirect to /?modal_url=/login/,
    causing the front-end to display the login in a modal.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.htmx:
            view_name = resolve(request.path_info).url_name
            if view_name in settings.MODAL_VIEWS:
                kwargs = request.resolver_match.kwargs  # Get any URL arguments
                modal_url = reverse(view_name, kwargs=kwargs)
                home_url = reverse("home")
                return redirect(f"{home_url}?modal_url={modal_url}")
        return response
