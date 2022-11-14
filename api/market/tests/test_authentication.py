import pytest
from middlewares.authentication import JWTAuthentication
from http import HTTPStatus
from django.contrib.auth.models import User
from rest_framework import exceptions
from market import settings

class TestIsAuthenticated:
    def test_authenticate_sucess(self, mocker, request_mock, response_mock):
        # arrange
        user_data = {
            "id": 1,
            "email": "test@test.com"
        }
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={})
        response = response_mock(status_code=200)
        mock_get = mocker.patch("requests.get", return_value=response)
        mock_parse_data = mocker.patch.object(response_mock, 'json', return_value=user_data)
        expected_user = User(**user_data)

        # act
        result = JWTAuthentication().authenticate(request)

        # assert
        mock_get.assert_called_with(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={request.headers['Authorization']}")
        mock_parse_data.assert_called()
        assert result[0] == expected_user
        assert result[1] == request.headers['Authorization']
        assert request.session.get("token") == request.headers['Authorization']
        assert request.session.get("user") == user_data
    
    def test_authenticate_token_already_exists(self, mocker, request_mock):
        # arrange
        user_data = {
            "id": 1,
            "email": "test@test.com"
        }
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={"token": "48309809384349089023", "user": user_data})
        mock_get = mocker.patch("requests.get")
        expected_user = User(**user_data)

        # act
        result = JWTAuthentication().authenticate(request)

        # assert
        mock_get.assert_not_called()
        assert result[0] == expected_user
        assert result[1] == request.headers['Authorization']
    
    def test_not_authenticate(self, mocker, request_mock, response_mock):
        # arrange
        request = request_mock(headers={"Authorization": "48309809384349089023"}, session={})
        response = response_mock(status_code=404)
        mock_get = mocker.patch("requests.get", return_value=response)

        # act
        with pytest.raises(exceptions.AuthenticationFailed):
            JWTAuthentication().authenticate(request)

        # assert
        mock_get.assert_called_with(f"{settings.AUTHENTICATOR_URI}/auth/verify?token={request.headers['Authorization']}")
        assert request.session.get("token") == None
        assert request.session.get("user") == None
    
    def test_not_authenticate_empty_token(self, mocker, request_mock):
        # arrange
        request = request_mock(headers={}, session={})
        mock_get = mocker.patch("requests.get")

        # act
        result = JWTAuthentication().authenticate(request)

        # assert
        mock_get.assert_not_called()
        assert not result
        assert request.session.get("token") == None
        assert request.session.get("user") == None
    
    def test_authenticate_header(self):
        # act
        result = JWTAuthentication().authenticate_header({})

        # assert
        assert result == HTTPStatus.UNAUTHORIZED

        