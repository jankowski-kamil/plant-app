import pytest
from django.urls import reverse
from rest_framework import status


class TestUserViewSet:
    @pytest.mark.django_db()
    def test_list_users(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("api:user-list")
        response = api_client.get(url)
        assert len(response.data) == 1
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_user_detail(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse("api:user-detail", kwargs={"pk": user.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db()
    def test_register_user(self, api_client, user):
        url = reverse("users:rest_register")
        response = api_client.post(
            url,
            {
                "email": "test@test.pl",
                "password1": "hvFVAPi.02^E!",
                "password2": "hvFVAPi.02^E!",
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["access"]

    @pytest.mark.django_db()
    def test_login_user(self, api_client, user):
        payload = {
            "email": "test@test.pl",
            "password1": "hvFVAPi.02^E!",
            "password2": "hvFVAPi.02^E!",
        }
        url_register = reverse("users:rest_register")
        api_client.post(url_register, payload)
        url_login = reverse("users:login")
        response = api_client.post(
            url_login,
            {"email": payload["email"], "password": payload["password1"]},
        )
        assert response.status_code == status.HTTP_200_OK
