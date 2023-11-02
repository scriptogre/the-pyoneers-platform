from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.templatetags.socialaccount import get_adapter
from allauth.utils import get_request_param
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from jinja2 import pass_context
from jinja2.ext import Extension
from markupsafe import Markup


class AllAuthExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.globals.update(
            {
                "provider_login_url": self.provider_login_url,
                "get_social_accounts": self.get_social_accounts,
                "get_providers": self.get_providers,
            }
        )

    @pass_context
    def provider_login_url(self, context, provider_id, **kwargs):
        request = context.get("request")  # Fetch request from context

        adapter = get_adapter(request)
        provider = adapter.get_provider(request, provider_id)
        query = kwargs
        auth_params = query.get("auth_params", None)
        scope = query.get("scope", None)
        process = query.get("process", None)

        if scope == "":
            del query["scope"]
        if auth_params == "":
            del query["auth_params"]

        if "next" not in query:
            next = get_request_param(request, "next")
            if next:
                query["next"] = next
            elif process == "redirect":
                query["next"] = request.get_full_path()
        else:
            if not query["next"]:
                del query["next"]

        return provider.get_login_url(request, **query)

    def get_social_accounts(self, user):
        return SocialAccount.objects.filter(user=user)

    def get_providers(self):
        return providers.registry.get_class_list()


def render_svg(filepath, css_classes=None):
    """
    Render SVG by relative filepath from the static folder and add optional CSS classes.

    Args:
    filepath (str): Relative path to SVG file within the static folder (e.g., 'svg/chevron.svg').
    css_classes (str, optional): Classes to add to SVG's 'class' attribute.

    Returns:
    jinja2.Markup: Safe HTML of the SVG or an empty string if not found.

    Raises:
    Exception: If SVG file is not found and settings.DEBUG is True.
    """
    path = finders.find(filepath, all=True)

    if not path:
        message = f"SVG '{filepath}' not found"
        if settings.DEBUG:
            raise Exception(message)
        else:
            return ""

    if isinstance(path, (list, tuple)):
        path = path[0]

    with open(path) as svg_file:
        svg_content = svg_file.read()

    if css_classes:
        if 'class="' in svg_content:
            new_class = f'class="{css_classes} '
            svg_content = svg_content.replace('class="', new_class)
        else:
            new_class = f' class="{css_classes}"'
            svg_content = svg_content.replace("<svg ", f"<svg {new_class} ")

    return Markup(svg_content)


def avatar_url(user):
    if user.is_authenticated:
        social_account = SocialAccount.objects.filter(user=user).first()
        if social_account:
            return social_account.get_avatar_url()
    return static("img/avatar-default.webp")


def to_roman(value: int) -> str:
    """
    Convert an integer to a Roman numeral.

    Usage: {{ 42|to_roman }}
    """
    if not (0 < value < 4000):
        raise ValueError("Value must be between 1 and 3999")

    int_vals = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    rom_syms = ("M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I")

    roman_numeral = ""
    for i, v in enumerate(int_vals):
        while value >= v:
            value -= v
            roman_numeral += rom_syms[i]

    return roman_numeral
