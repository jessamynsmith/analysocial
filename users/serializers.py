from django.contrib.auth import get_user_model
from rest_framework import serializers

from users import models as user_models


class UserSerializer(serializers.ModelSerializer):
    userprofile = serializers.HyperlinkedRelatedField(read_only=True, view_name='userprofiles-detail')

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'userprofile')


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = user_models.UserProfile
        fields = "__all__"
