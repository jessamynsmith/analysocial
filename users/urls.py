from django.conf.urls import include, url
from rest_framework import routers

from users import views as user_views


router = routers.DefaultRouter()
router.register(r'users', user_views.UserViewSet, basename='users')
router.register(r'userprofiles', user_views.UserProfileViewSet, basename='userprofiles')


urlpatterns = [
    url(r'^api/v1/', include(router.urls)),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^accounts/profile/$', user_views.UserProfileView.as_view(), name="user_profile"),
]
