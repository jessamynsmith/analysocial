from django.conf.urls import url

from graph import views as graph_views

urlpatterns = [
    url(r'^$', graph_views.IndexView.as_view()),
    url(r'^privacy/', graph_views.PrivacyView.as_view(), name="privacy"),
    url(r'^accounts/profile/', graph_views.UserProfileView.as_view(), name="account_profile"),
    url(r'^posts/facebook/', graph_views.PostListView.as_view(), name="posts_facebook"),
    url(r'^usage/', graph_views.UsageView.as_view(), name="usage"),
]
