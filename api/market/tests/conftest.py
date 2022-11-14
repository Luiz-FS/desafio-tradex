import pytest
from django.contrib.auth.models import User
from product.models import Product
from product_cost.models import ProductCost


class ResponseMock:
    status_code = 200

    def __init__(self, status_code):
        self.status_code = status_code

    def json(self):  # pragma nocover
        return {}


class RequestMock:
    headers = {}
    session = {}

    def __init__(self, headers, session):
        self.headers = headers
        self.session = session

class IOMock:
    def write(self):  # pragma nocover
        pass


class OpenMock:
    def __init__(*args, **kwargs):
        pass

    def __enter__(self):
        return IOMock()
    
    def __exit__(self, *args, **kwargs):
        pass


@pytest.fixture
def make_products():
    return [
        Product.objects.create(
            name=f"product{i}",
            ean=3212,
            weight=1,
            min_cost="10",
            max_cost="40"
        )

        for i in range(10)
    ]


@pytest.fixture
def make_products_cost(make_products):
    return [
        ProductCost.objects.create(
            cost="20",
            date=f"2022-11-{10 + i}",
            product=make_products[i]
        )

        for i in range(10)
    ]


@pytest.fixture
def authenticator_mock(mocker):
    def mock_value(success=True):
        user = User(
            id=1,
            email="test@test.com"
        )

        if success:
            return_value = (user, None)
        else:
            return_value = None

        mocker.patch("middlewares.authentication.JWTAuthentication.authenticate", return_value=return_value)
        return user
    
    return mock_value


@pytest.fixture
def request_mock():
    return RequestMock


@pytest.fixture
def response_mock():
    return ResponseMock


@pytest.fixture
def open_mock():
    return OpenMock

@pytest.fixture
def io_mock():
    return IOMock
