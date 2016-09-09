from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, RedirectView, TemplateView

from graph import models as graph_models
from graph.helpers import retrieve_facebook_posts


class IndexView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('facebook_posts')


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
class PostListView(ListView):
    model = graph_models.Post
    paginate_by = 25

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-created_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        retrieve_facebook_posts(user=self.request.user, retrieve_all=False)
        return context

    # TODO Add searching/sorting


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = graph_models.Post


@method_decorator(login_required, name='dispatch')
class AttachmentDetailView(DetailView):
    model = graph_models.Attachment


@method_decorator(login_required, name='dispatch')
class CommentDetailView(DetailView):
    model = graph_models.Comment


@method_decorator(login_required, name='dispatch')
class UsageView(TemplateView):
    template_name = 'graph/usage.html'
