
import pytest
from fastapi import status

def test_create_product(client, test_category):
    """Test creating a new product."""
    product_data = {
        "name": "Monitor",
        "price": 300.0,
        "quantity": 20,
        "category_id": test_category.id
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["id"] is not None

def test_get_all_products(client, test_products):
    """Test retrieving a list of all products."""
    response = client.get("/products/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 3
    assert data[0]["name"] == "Laptop"

def test_get_product_by_id(client, test_products):
    """Test retrieving a single product by its ID."""
    product_id = test_products[0].id
    response = client.get(f"/products/{product_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Laptop"

def test_get_nonexistent_product(client):
    """Test retrieving a product that does not exist."""
    response = client.get("/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_update_product(client, test_products):
    """Test updating an existing product."""
    product_id = test_products[0].id
    update_data = {"name": "Gaming Laptop", "price": 1500.0}
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Gaming Laptop"
    assert data["price"] == 1500.0
    assert data["quantity"] == test_products[0].quantity 

def test_update_nonexistent_product(client):
    """Test updating a product that does not exist."""
    response = client.put("/products/99999", json={"name": "New Name"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_product(client, test_products):
    """Test deleting a product."""
    product_id = test_products[0].id
    response = client.delete(f"/products/{product_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND

def test_delete_nonexistent_product(client):
    """Test deleting a product that does not exist."""
    response = client.delete("/products/99999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_search_products(client, test_products):
    """Test searching products by name."""

    response = client.get("/products/?search=Laptop")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"


    response = client.get("/products/?search=Mouse")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mouse"


    response = client.get("/products/?search=NonExistent")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 0

def test_filter_by_price(client, test_products):
    """Test filtering products by price range."""

    response = client.get("/products/?min_price=50")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2 # Laptop and Keyboard
    assert all(p["price"] > 50 for p in data)


    response = client.get("/products/?max_price=100")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2 # Mouse and Keyboard
    assert all(p["price"] < 100 for p in data)


    response = client.get("/products/?min_price=50&max_price=100")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1 # Keyboard
    assert 50 <= data[0]["price"] <= 100

def test_pagination(client, test_products):
    """Test pagination with skip and limit."""
    # Get first product (limit=1, skip=0)
    response = client.get("/products/?limit=1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Laptop"


    response = client.get("/products/?limit=1&skip=1")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Mouse"


    response = client.get("/products/?limit=2")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
