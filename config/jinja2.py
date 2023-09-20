from jinja2 import pass_context
from jinja2.ext import Extension
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount import providers
from allauth.socialaccount.templatetags.socialaccount import (
    get_adapter,
)
from allauth.utils import get_request_param
from markdown import Markdown
from wagtailmarkdown.utils import _get_markdown_kwargs

from pyoneers_platform.course.models import Chapter, Module


class AllAuthExtension(Extension):
    def __init__(self, environment):
        super(AllAuthExtension, self).__init__(environment)
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
