import pytest
from rest_framework.test import APIClient

CUSTOMERS_PATH = "/customers/"


@pytest.fixture
def customer_attrs() -> dict[str, str]:
    return {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
    }


def verify_customer_response(
    response: dict[str, str], expected_data: dict[str, str]
) -> None:
    assert response["first_name"] == expected_data["first_name"]
    assert response["last_name"] == expected_data["last_name"]
    assert response["email"] == expected_data["email"]


@pytest.mark.django_db
def test_add_customer(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 201
    verify_customer_response(response.data, customer_request)


@pytest.mark.django_db
def test_user_email_is_unique(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 201

    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 400
    assert response.data == {
        "email": ["customer with this email already exists."]
    }


@pytest.mark.django_db
def test_customer_name_is_required(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    customer_request["first_name"] = ""
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 400
    assert response.data == {"first_name": ["This field may not be blank."]}


@pytest.mark.django_db
def test_customer_email_is_required(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    customer_request["email"] = ""
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 400
    assert response.data == {"email": ["This field may not be blank."]}


@pytest.mark.django_db
def test_customer_email_needs_to_be_valid(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    customer_request["email"] = "not a valid email"
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 400
    assert response.data == {"email": ["Enter a valid email address."]}


@pytest.mark.django_db
def test_fetch_all_customers_sorted_by_last_name(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    customer_request = customer_attrs
    response = api_client.post(CUSTOMERS_PATH, customer_request, format="json")
    assert response.status_code == 201

    response = api_client.get(CUSTOMERS_PATH)
    assert response.status_code == 200
    assert len(response.data) == 1
    verify_customer_response(response.data[0], customer_request)


@pytest.mark.django_db
def test_removing_customer(
    api_client: APIClient, customer_attrs: dict[str, str]
) -> None:
    response = api_client.post(CUSTOMERS_PATH, customer_attrs, format="json")
    delete_url = CUSTOMERS_PATH + response.data["id"] + "/"
    response = api_client.delete(delete_url)
    assert response.status_code == 204
    response = api_client.delete(delete_url)
    assert response.status_code == 404
