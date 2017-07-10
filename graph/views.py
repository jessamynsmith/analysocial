import datetime
from dateutil.relativedelta import relativedelta

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query_utils import Q
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, TemplateView
from django.views.generic.edit import FormMixin
from jsonview.views import JsonView

from graph import forms as graph_forms
from graph import models as graph_models
from graph import helpers


class FormListView(FormMixin, ListView):
    def get_form_kwargs(self):
        kwargs = super(FormListView, self).get_form_kwargs()
        if self.request.method == 'GET':
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        return super(FormListView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FormListView, self).get_context_data(**kwargs)
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class IndexView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('facebook_posts')


class PrivacyView(TemplateView):
    template_name = 'account/privacy.html'

    def get_context_data(self, **kwargs):
        context = super(PrivacyView, self).get_context_data(**kwargs)
        context['admin_email'] = settings.ADMINS[0][1]
        return context


class PostListView(LoginRequiredMixin, FormListView):
    model = graph_models.Post
    paginate_by = 25
    searchable_fields = [
        "created_time",
        "story",
        "message",
        "comment__from_json",
        "comment__message",
    ]
    form_class = graph_forms.SearchForm

    def get_queryset(self):
        queryset = super(PostListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-created_time')
        if self.form.is_valid():
            start_date = self.form.cleaned_data.get('start_date')
            end_date = self.form.cleaned_data.get('end_date')
            search_text = self.form.cleaned_data.get('text')
            if start_date:
                queryset = queryset.filter(created_time__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_time__lt=end_date + relativedelta(days=1))
            if search_text:
                q = Q()
                for field in self.searchable_fields:
                    q |= Q(**{'%s__icontains' % field: search_text})
                queryset = queryset.filter(q).distinct()
        return queryset

    def post(self, request, *args, **kwargs):
        helpers.retrieve_facebook_posts(user=self.request.user, ignore_errors=True)
        return self.get(request, *args, **kwargs)


class PostDetailView(LoginRequiredMixin, DetailView):
    model = graph_models.Post


class AttachmentDetailView(LoginRequiredMixin, DetailView):
    model = graph_models.Attachment


class CommentDetailView(LoginRequiredMixin, DetailView):
    model = graph_models.Comment


class MessageListView(LoginRequiredMixin, FormListView):
    model = graph_models.Message
    paginate_by = 25
    searchable_fields = [
        "updated_time",
        "message",
        "from_data",
        "to_data",
    ]
    form_class = graph_forms.SearchForm

    def get_queryset(self):
        queryset = super(MessageListView, self).get_queryset()
        queryset = queryset.filter(user=self.request.user).order_by('-updated_time')
        if self.form.is_valid():
            start_date = self.form.cleaned_data.get('start_date')
            end_date = self.form.cleaned_data.get('end_date')
            search_text = self.form.cleaned_data.get('text')
            if start_date:
                queryset = queryset.filter(updated_time__gte=start_date)
            if end_date:
                queryset = queryset.filter(updated_time__lt=end_date + relativedelta(days=1))
            if search_text:
                q = Q()
                for field in self.searchable_fields:
                    q |= Q(**{'%s__icontains' % field: search_text})
                queryset = queryset.filter(q).distinct()
        return queryset


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = graph_models.Message


class UsageView(LoginRequiredMixin, TemplateView):
    template_name = 'graph/usage.html'

    def get_context_data(self, **kwargs):
        context = super(UsageView, self).get_context_data(**kwargs)
        context['graph_types'] = [
            ['posts_by_day', 'Posts By Day'],
            ['posts_by_month', 'Posts By Month'],
            ['posts_by_year', 'Posts By Year'],
        ]
        posts = graph_models.Post.objects.all().order_by('created_time')
        num_posts = posts.count()
        original_posts = posts.filter(attachment__isnull=True).count()
        shared_posts = posts.filter(attachment__isnull=False).exclude(
            message__exact='').count()
        blank_shares = posts.filter(attachment__isnull=False).filter(
            message__exact='').count()
        context['posts'] = list(posts.values_list('created_time', flat=True))
        context['num_posts'] = num_posts
        context['original_posts'] = round((original_posts * 100) / num_posts)
        context['shared_with_commentary'] = round((shared_posts * 100) / num_posts)
        context['blank_shares'] = round((blank_shares * 100) / num_posts)

        posts = graph_models.Post.objects.filter(user=self.request.user)
        posts_by_day = helpers.posts_by_day(posts)
        post_counts_by_day = [day[1] for day in posts_by_day]
        six_months_ago = datetime.date.today() - relativedelta(months=6)
        last_6_months = [day[1] for day in posts_by_day.filter(created_time__gt=six_months_ago)]
        posts_by_count = sorted(post_counts_by_day)
        maximum_posts = ''
        if len(posts_by_count):
            maximum_posts = posts_by_count[-1]
        context['posts_by_day'] = {
            'average_all_time': helpers.get_mean(post_counts_by_day),
            'average_6_months': helpers.get_mean(last_6_months),
            'maximum': maximum_posts,
            'median': helpers.get_median(post_counts_by_day),
            'mode': helpers.get_mode(post_counts_by_day),
        }

        comments = graph_models.Comment.objects.filter(post__user=self.request.user)
        comments_by_post = helpers.comments_by_post(comments)
        comment_counts_by_post = [day[1] for day in comments_by_post]
        six_months_ago = datetime.date.today() - relativedelta(months=6)
        last_6_months = [day[1] for day in comments_by_post.filter(
            post__created_time__gt=six_months_ago)]
        context['comments_by_post'] = {
            'average_all_time': helpers.get_mean(comment_counts_by_post),
            'average_6_months': helpers.get_mean(last_6_months),
            'maximum': comments_by_post.last(),
            'median': helpers.get_median(comment_counts_by_post),
            'mode': helpers.get_mode(comment_counts_by_post),
        }

        return context


class PostsByDayView(LoginRequiredMixin, JsonView):
    def get_context_data(self, **kwargs):
        posts = graph_models.Post.objects.filter(user=self.request.user)
        context = {
            'data': list(helpers.posts_by_day(posts))
        }
        return context


class PostsByMonthView(LoginRequiredMixin, JsonView):
    def get_context_data(self, **kwargs):
        posts = graph_models.Post.objects.filter(user=self.request.user)
        context = {
            'data': list(helpers.posts_by_month(posts))
        }
        return context


class PostsByYearView(LoginRequiredMixin, JsonView):
    def get_context_data(self, **kwargs):
        posts = graph_models.Post.objects.filter(user=self.request.user)
        context = {
            'data': list(helpers.posts_by_year(posts))
        }
        return context
