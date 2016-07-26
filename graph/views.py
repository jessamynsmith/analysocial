from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

import facebook


@method_decorator(login_required, name='dispatch')
class UserProfileView(TemplateView):
    template_name = 'account/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        social_accounts = self.request.user.socialaccount_set.all()
        if social_accounts.count():
            graph_api = facebook.GraphAPI(social_accounts[0].socialtoken_set.all()[0].token)
            context['info'] = graph_api.get_objects(['me'])
        return context
