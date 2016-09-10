import datetime
from dateutil import relativedelta

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, RedirectView, TemplateView, View
from django.views.generic.base import ContextMixin
from jsonview.decorators import json_view

from graph import models as graph_models
from graph import helpers


@method_decorator(json_view, name='dispatch')
class JsonView(ContextMixin, View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return context


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
        return context

    def post(self, request, *args, **kwargs):
        helpers.retrieve_facebook_posts(user=self.request.user, ignore_errors=True)
        return self.get(request, *args, **kwargs)


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

    def get_context_data(self, **kwargs):
        context = super(UsageView, self).get_context_data(**kwargs)
        context['graph_types'] = [
            ['posts_by_day', 'Posts By Day'],
            ['posts_by_month', 'Posts By Month'],
        ]
        posts = graph_models.Post.objects.all().order_by('created_time')
        context['posts'] = list(posts.values_list('created_time', flat=True))

        posts = graph_models.Post.objects.filter(user=self.request.user)
        posts_by_day = helpers.posts_by_day(posts)
        post_counts_by_day = [day[1] for day in posts_by_day]
        six_months_ago = datetime.date.today() - relativedelta.relativedelta(months=6)
        last_6_months = [day[1] for day in posts_by_day.filter(created_time__gt=six_months_ago)]
        posts_by_count = sorted(post_counts_by_day)
        context['posts_by_day'] = {
            'average_all_time': helpers.get_mean(post_counts_by_day),
            'average_6_months': helpers.get_mean(last_6_months),
            'maximum': posts_by_count[-1],
            'median': helpers.get_median(post_counts_by_day),
            'mode': helpers.get_mode(post_counts_by_day),
        }
        return context


@method_decorator(login_required, name='dispatch')
class PostsByDayView(JsonView):
    def get_context_data(self, **kwargs):
        posts = graph_models.Post.objects.filter(user=self.request.user)
        context = {
            'data': list(helpers.posts_by_day(posts))
        }
        return context


@method_decorator(login_required, name='dispatch')
class PostsByMonthView(JsonView):
    def get_context_data(self, **kwargs):
        posts = graph_models.Post.objects.filter(user=self.request.user)
        context = {
            'data': list(helpers.posts_by_month(posts))
        }
        return context
