from django.conf.urls import url
from django.views.generic import RedirectView

from graph import views as graph_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='usage/')),
    url(r'^privacy/', graph_views.PrivacyView.as_view(), name="privacy"),
    url(r'^accounts/profile/', graph_views.UserProfileView.as_view(), name="account_profile"),
    url(r'^posts/facebook/', graph_views.PostListView.as_view(), name="posts_facebook"),
    url(r'^usage/', graph_views.UsageView.as_view(), name="usage"),
]
