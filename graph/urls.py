from django.conf.urls import url
from django.views.generic import RedirectView

from graph import views as graph_views

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='accounts/profile/'), name="account_profile"),
    url(r'^accounts/profile/', graph_views.UserProfileView.as_view()),
]
