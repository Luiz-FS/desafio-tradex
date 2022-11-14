from http import HTTPStatus
import pytest
from product_cost import serializers, models
from events.models import Event


@pytest.mark.django_db
class TestList:

    def test_list_products_cost(self, client, make_products_cost, authenticator_mock):
        # arrange
        authenticator_mock(success=True)
        expected_products_cost = serializers.ProductCostSerializer(make_products_cost, many=True).data
        expected_products_cost = sorted(expected_products_cost, key=lambda cost: cost["date"])

        for product in expected_products_cost:
            product["product"] = str(product["product"])

        # act
        response = client.get("/api/cost/")
        data = response.json()

        #assert
        assert expected_products_cost == data["results"]

    def test_list_products_cost_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.get("/api/cost/")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED


@pytest.mark.django_db
class TestCreate:
    def test_create_product_cost(self, client, authenticator_mock, make_products):
        # arrange
        user = authenticator_mock(success=True)
        product = make_products[0]
        product_cost_data = {
            "cost": "20.00",
            "date": "2022-11-14",
            "product": str(product.id)
        }

        # act
        response = client.post("/api/cost/", product_cost_data, content_type="application/json")
        data = response.json()
        event = Event.objects.all().first()

        product_cost = models.ProductCost.objects.get(id=data["id"])
        product_cost_raw = serializers.ProductCostSerializer(product_cost).data
        product_cost_raw["product"] = str(product_cost_raw["product"])

        #assert
        assert data == product_cost_raw
        assert event.name == "create_product_cost"
        assert event.entity_id == product_cost.id
        assert event.user_email == user.email
        assert event.data == product_cost_data
    
    def test_create_product_cost_unauthorized(self, client, authenticator_mock):
        # arrange
        authenticator_mock(success=False)

        # act
        response = client.post("/api/cost/", {
            "cost": "20.00",
            "date": "2022-11-14",
            "product": "38db57c3-e91c-4069-a410-e34860bc2a30"
        }, content_type="application/json")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED
    
    @pytest.mark.parametrize(
        'cost',
        [
            "5.00",
            "50.00"
        ]
    )
    def test_create_product_cost_bad_request(self, client, authenticator_mock, make_products, cost):
        # arrange
        authenticator_mock(success=True)
        product = make_products[0]
        product_cost_data = {
            "cost": cost,
            "date": "2022-11-14",
            "product": str(product.id)
        }
        expected_response = {
            'detail': 'Cost must be greater than 10.00 and less than 40.00.'
        }

        # act
        response = client.post("/api/cost/", product_cost_data, content_type="application/json")
        data = response.json()
        
        # assert
        assert data == expected_response
        assert response.status_code == HTTPStatus.BAD_REQUEST



@pytest.mark.django_db
class TestPatch:
    def test_patch_product(self, client, authenticator_mock, make_products_cost):
        # arrange
        user = authenticator_mock(success=True)
        product_cost = make_products_cost[0]
        product_cost_data = {
            "cost": "25.00",
        }

        # act
        response = client.patch(f"/api/cost/{product_cost.id}/", product_cost_data, content_type="application/json")
        data = response.json()
        event = Event.objects.all().first()

        product_cost = models.ProductCost.objects.get(id=data["id"])
        product_cost_raw = serializers.ProductCostSerializer(product_cost).data
        product_cost_raw["product"] = str(product_cost_raw["product"])
        
        #assert
        assert data == product_cost_raw
        assert event.name == "update_product_cost"
        assert event.entity_id == product_cost.id
        assert event.user_email == user.email
        assert event.data == product_cost_data
    
    def test_patch_product_cost_unauthorized(self, client, authenticator_mock, make_products_cost):
        # arrange
        authenticator_mock(success=False)
        product_cost = make_products_cost[0]
        product_cost_data = {
            "name": "test-patch",
        }

        # act
        response = client.patch(f"/api/cost/{product_cost.id}/", product_cost_data, content_type="application/json")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED



@pytest.mark.django_db
class TestDelete:
    def test_delete_product_cost(self, client, authenticator_mock, make_products_cost):
        # arrange
        user = authenticator_mock(success=True)
        product_cost = make_products_cost[0]

        # act
        client.delete(f"/api/cost/{product_cost.id}/")
        event = Event.objects.all().first()
        
        #assert
        assert event.name == "delete_product_cost"
        assert event.entity_id == product_cost.id
        assert event.user_email == user.email
        assert event.data == {}
    
    def test_delete_product_cost_unauthorized(self, client, authenticator_mock, make_products_cost):
        # arrange
        authenticator_mock(success=False)
        product_cost = make_products_cost[0]

        # act
        response = client.patch(f"/api/cost/{product_cost.id}/")

        # assert
        assert response.status_code == HTTPStatus.UNAUTHORIZED