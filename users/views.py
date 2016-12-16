from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse
from django.views.generic import UpdateView


class UserProfileView(LoginRequiredMixin, UpdateView):
    fields = ['receive_emails']

    def get_object(self, *args, **kwargs):
        return self.request.user.userprofile

    def get_success_url(self):
        return reverse('facebook_posts')

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context['social_accounts'] = self.request.user.socialaccount_set.all()
        return context
