from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import UpdateView
from rest_framework import viewsets

from users import models as user_models
from users import serializers


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


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return user_models.UserProfile.objects.filter(user=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return get_user_model().objects.filter(id=self.request.user.id)
