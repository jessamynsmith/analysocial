from django.conf.urls import include, url

from users import views as user_views


urlpatterns = [
    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', user_views.UserProfileView.as_view(), name="user_profile"),
]
