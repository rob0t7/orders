import pytest
from rest_framework.test import APIClient
from orders.models import Product


PRODUCT_PATH = "/products/"


def verify_product_response(product_data, expected_product):
    assert product_data["name"] == expected_product.name
    assert product_data["price"] == expected_product.price


@pytest.mark.django_db
def test_list_products_in_alph_order(api_client: APIClient) -> None:
    product1 = Product.objects.create(name="Tacos", price="10.99")
    product2 = Product.objects.create(name="Cookies", price="5.00")

    response = api_client.get("/products/")

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert len(response.data) == 2
    verify_product_response(response.data[0], product2)
    verify_product_response(response.data[1], product1)


@pytest.mark.django_db
def test_create_product(api_client: APIClient) -> None:
    response = api_client.get(PRODUCT_PATH)
    assert response.status_code == 200
    assert len(response.data) == 0

    expected_product = Product(name="Tacos", price="10.99")
    response = api_client.post(
        PRODUCT_PATH,
        {"name": expected_product.name, "price": expected_product.price},
        format="json",
    )

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    verify_product_response(response.data, expected_product)


@pytest.mark.django_db
def test_product_name_is_unique(api_client: APIClient) -> None:
    Product.objects.create(name="Cookies", price=10)

    response = api_client.post(
        PRODUCT_PATH, {"name": "Cookies", "price": "5.00"}, format="json"
    )

    assert response.status_code == 400
    assert response.data["name"] == ["product with this name already exists."]


@pytest.mark.django_db
def test_product_must_have_positive_price(api_client: APIClient) -> None:
    response = api_client.post(
        PRODUCT_PATH, {"name": "Cookies", "price": "-0.01"}, format="json"
    )
    assert response.status_code == 400
    assert response.data["price"] == [
        "Ensure this value is greater than or equal to 0."
    ]


@pytest.mark.django_db
def test_product_must_have_name(api_client: APIClient) -> None:
    response = api_client.post(
        PRODUCT_PATH, {"name": "", "price": "0"}, format="json"
    )
    assert response.status_code == 400
    assert response.data["name"] == ["This field may not be blank."]


@pytest.mark.django_db
def test_retrieve_product(api_client: APIClient) -> None:
    expected_product = Product.objects.create(name="Cookies", price="0.00")
    response = api_client.get(f"{PRODUCT_PATH}123123123123/")
    assert response.status_code == 404

    response = api_client.get(f"{PRODUCT_PATH}{expected_product.id}/")
    assert response.status_code == 200
    verify_product_response(response.data, expected_product)


@pytest.mark.django_db
def test_removing_product(api_client: APIClient) -> None:
    product = Product.objects.create(name="Cookies", price=0)
    response = api_client.delete(f"{PRODUCT_PATH}{product.id}/")
    assert response.status_code == 204
    response = api_client.delete(f"{PRODUCT_PATH}{product.id}/")
    assert response.status_code == 404
    response = api_client.get(f"{PRODUCT_PATH}{product.id}/")
    assert response.status_code == 404
