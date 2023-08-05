from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.utils.http import is_safe_url

from localcosmos_server.forms import EmailOrUsernameAuthenticationForm

# activate permission rules
from .permission_rules import *

class LogIn(LoginView):
    template_name = 'localcosmos_server/registration/login.html'
    form_class = EmailOrUsernameAuthenticationForm

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.GET.get(
            self.redirect_field_name,
            self.request.POST.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


class LoggedOut(TemplateView):
    template_name = 'localcosmos_server/registration/loggedout.html'
