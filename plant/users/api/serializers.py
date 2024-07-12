from rest_framework import serializers
from django_rest_passwordreset.serializers import PasswordTokenSerializer

from plant.users.models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = ["name", "url"]

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "pk"},
        }


class PasswordResetConfirmSerializer(PasswordTokenSerializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                detail="The two password fields didn't match."
            )

        return super().validate(data)
