import pytest
from http import HTTPStatus
from uuid import uuid4
from datetime import datetime
from product import serializers, models
from events.models import Event
from market import settings


@pytest.mark.django_db
class TestList:

    def test_list_products(self, client, make_products, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        expected_products = serializers.ProductSerializer(make_products, many=True).data
        expected_products = sorted(expected_products, key=lambda product: product["name"])

        # act
        response = client.get("/api/product/")
        data = response.json()

        #assert
        assert expected_products == data["results"]

    def test_list_product_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.get("/api/product/")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
class TestCreate:
    def test_create_product(self, client, authenticator_mock):
        # arrange
        user = authenticator_mock(success=True)
        product_data = {
            "name": "test",
            "ean": 438,
            "weight": 2,
            "min_cost": "1.00",
            "max_cost": "2.00"
        }

        # act
        response = client.post("/api/product/", product_data, content_type="application/json")
        data = response.json()
        event = Event.objects.all().first()

        product = models.Product.objects.get(id=data["id"])
        product_raw = serializers.ProductSerializer(product).data
        
        #assert
        assert data == product_raw
        assert event.name == "create_product"
        assert event.entity_id == product.id
        assert event.user_email == user.email
        assert event.data == product_data
    
    def test_create_product_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.post("/api/product/", {
            "name": "test",
            "ean": 438,
            "weight": 2,
            "min_cost": "1.00",
            "max_cost": "2.00"
        }, content_type="application/json")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    @pytest.mark.parametrize(
        'min_cost,max_cost,message',
        [
            ('-1.00', '1.00', 'new row for relation "product_product" violates check constraint "min_cost__gte_0"'),
            ('2.00', '1.00', 'new row for relation "product_product" violates check constraint "min_cost__lte_max_cost"')
        ]
    )
    def test_create_product_bad_request(self, client, authenticator_mock, min_cost, max_cost, message):
        # arrange
        authenticator_mock(success=True)
        product_data = {
            "name": "test",
            "ean": 438,
            "weight": 2,
            "min_cost": min_cost,
            "max_cost": max_cost
        }
        expected_response = {'detail': message}

        # act
        response = client.post("/api/product/", product_data, content_type="application/json")
        data = response.json()
        
        # assert
        assert data == expected_response
        assert response.status_code == HTTPStatus.BAD_REQUEST
    
    def test_upload_image(self, client, mocker, make_products, authenticator_mock, open_mock, io_mock):
        # arrange
        user = authenticator_mock(success=True)
        product = make_products[0]
        mock_uuid = uuid4()
        mock_now = datetime.now()
        mock_open = mocker.patch("product.views.open", return_value=open_mock())
        mock_io = mocker.patch.object(io_mock, "write")
        mock_verify_process_area = mocker.patch("product.views.verify_process_area")
        mock_datetime = mocker.patch("product.views.datetime")
        mock_datetime.now.return_value = mock_now
        mocker.patch("uuid.uuid4", return_value=mock_uuid)
        expected_filename = f"{mock_uuid}-{mock_now.timestamp()}.png"

        # act
        with open("tests/fixtures/image.png", 'rb') as f:
            response = client.post(
                f"/api/product/{product.id}/upload_image/",
                data={
                    "file": f
                },
                format="multipart"
            )
        
        product.refresh_from_db()
        data = response.json()
        event = Event.objects.all().first()

        product = models.Product.objects.get(id=data["id"])
        product_raw = serializers.ProductSerializer(product).data

        # assert
        mock_open.assert_called_with(f"{settings.PROCESS_AREA}/{expected_filename}", "wb")
        mock_io.assert_called()
        mock_verify_process_area.assert_called()

        assert data == product_raw
        assert response.status_code ==HTTPStatus.CREATED
        assert event.name == "update_product"
        assert event.entity_id == product.id
        assert event.user_email == user.email
        assert event.data == {"image": expected_filename}
    
    def test_upload_image_without_file(self, client, make_products, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        product = make_products[0]
        expected_response = {'detail': "File field is required"}

        # act
        response = client.post(
            f"/api/product/{product.id}/upload_image/",
            data={},
            format="multipart"
        )
        data = response.json()

        # assert
        assert data == expected_response
    
    def test_upload_image_invalid_file(self, client, make_products, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        product = make_products[0]
        expected_response = {'detail': "Only images are accepted"}

        # act
        with open("tests/fixtures/image.txt", 'rb') as f:
            response = client.post(
                f"/api/product/{product.id}/upload_image/",
                data={
                    "file": f
                },
                format="multipart"
            )
        data = response.json()

        # assert
        assert data == expected_response


@pytest.mark.django_db
class TestPatch:
    def test_patch_product(self, client, authenticator_mock, make_products):
        # arrange
        user = authenticator_mock(success=True)
        product = make_products[0]
        product_data = {
            "name": "test-patch",
        }

        # act
        response = client.patch(f"/api/product/{product.id}/", product_data, content_type="application/json")
        data = response.json()
        event = Event.objects.all().first()

        product = models.Product.objects.get(id=data["id"])
        product_raw = serializers.ProductSerializer(product).data
        
        #assert
        assert data == product_raw
        assert event.name == "update_product"
        assert event.entity_id == product.id
        assert event.user_email == user.email
        assert event.data == product_data
    
    def test_patch_product_unauthorized(self, client, authenticator_mock, make_products):
        # arrange
        authenticator_mock(success=False)
        product = make_products[0]
        product_data = {
            "name": "test-patch",
        }

        # act
        response = client.patch(f"/api/product/{product.id}/", product_data, content_type="application/json")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED



@pytest.mark.django_db
class TestDelete:
    def test_delete_product(self, client, authenticator_mock, make_products):
        # arrange
        user = authenticator_mock(success=True)
        product = make_products[0]

        # act
        client.delete(f"/api/product/{product.id}/")
        event = Event.objects.all().first()
        
        #assert
        assert event.name == "delete_product"
        assert event.entity_id == product.id
        assert event.user_email == user.email
        assert event.data == {}
    
    def test_delete_product_unauthorized(self, client, authenticator_mock, make_products):
        # arrange
        authenticator_mock(success=False)
        product = make_products[0]

        # act
        response = client.patch(f"/api/product/{product.id}/")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED