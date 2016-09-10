from django.conf.urls import url

from graph import views as graph_views

urlpatterns = [
    url(r'^$', graph_views.IndexView.as_view()),
    url(r'^privacy/$', graph_views.PrivacyView.as_view(), name="privacy"),
    url(r'^accounts/profile/$', graph_views.UserProfileView.as_view(), name="account_profile"),
    url(r'^facebook/posts/$', graph_views.PostListView.as_view(), name="facebook_posts"),
    url(r'^facebook/posts/(?P<pk>[0-9_]+)/$',
        graph_views.PostDetailView.as_view(),
        name="facebook_post"),
    url(r'^facebook/attachments/(?P<pk>[0-9_]+)/$',
        graph_views.AttachmentDetailView.as_view(),
        name="facebook_attachment"),
    url(r'^facebook/comments/(?P<pk>[0-9_]+)/$',
        graph_views.CommentDetailView.as_view(),
        name="facebook_comment"),

    url(r'^usage/$', graph_views.UsageView.as_view(), name="usage"),
    url(r'^usage/posts_by_day/$', graph_views.PostsByDayView.as_view(), name="posts_by_day"),
    url(r'^usage/posts_by_month/$', graph_views.PostsByMonthView.as_view(), name="posts_by_month"),
    url(r'^usage/posts_by_year/$', graph_views.PostsByYearView.as_view(), name="posts_by_year"),
]
