import pytest

ORDERS_PATH = "/orders/"


@pytest.mark.django_db
def test_create_new_order(api_client) -> None:
    response = api_client.post(ORDERS_PATH)
    assert response.status_code == 201


@pytest.mark.django_db
def test_retrieve_order(api_client) -> None:
    response = api_client.post(ORDERS_PATH)
    assert response.status_code == 201
    order_id = response.data["id"]
    order_path = ORDERS_PATH + order_id + "/"
    response = api_client.get(order_path)
    assert response.status_code == 200
    assert response.data["id"] == order_id
