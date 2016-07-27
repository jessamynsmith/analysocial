from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

import facebook


class PrivacyView(TemplateView):
    template_name = 'account/privacy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)
        context['admin_email'] = settings.ADMINS[0][1]
        return context


@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['social_accounts'] = self.request.user.socialaccount_set.all()
        return context


@method_decorator(login_required, name='dispatch')
class UsageView(TemplateView):
    template_name = 'graph/usage.html'

    def get_context_data(self, **kwargs):
        context = super(UsageView, self).get_context_data(**kwargs)
        social_accounts = self.request.user.socialaccount_set.all()
        if social_accounts.count():
            graph_api = facebook.GraphAPI(social_accounts[0].socialtoken_set.all()[0].token)
            context['social_account'] = graph_api.get_connections('me', 'posts')
        return context
