from fastapi.testclient import TestClient
from ..main import app
from ..dependencies.database import SessionLocal, engine, Base
from sqlalchemy.orm import sessionmaker
from .. import models, crud, schemas

client = TestClient(app)

# Initialize the database for testing
def setup_module():
    Base.metadata.create_all(bind=engine)

def teardown_module():
    Base.metadata.drop_all(bind=engine)

def get_test_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_menu_item():
    menu_item = {
        "name": "Burger",
        "ingredients": "Beef, Lettuce, Tomato",
        "price": 5.99,
        "calories": 500,
        "category": "Main"
    }
    response = client.post("/menu/", json=menu_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Burger"
    assert data["ingredients"] == "Beef, Lettuce, Tomato"
    assert data["price"] == 5.99
    assert data["calories"] == 500
    assert data["category"] == "Main"

def test_read_all_menu_items():
    response = client.get("/menu/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_read_menu_item():
    menu_item = {
        "name": "Pizza",
        "ingredients": "Cheese, Tomato, Dough",
        "price": 7.99,
        "calories": 700,
        "category": "Main"
    }
    create_response = client.post("/menu/", json=menu_item)
    menu_item_id = create_response.json()["id"]

    response = client.get(f"/menu/{menu_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == menu_item_id
    assert data["name"] == "Pizza"

def test_update_menu_item():
    menu_item = {
        "name": "Salad",
        "ingredients": "Lettuce, Tomato, Cucumber",
        "price": 4.99,
        "calories": 200,
        "category": "Appetizer"
    }
    create_response = client.post("/menu/", json=menu_item)
    menu_item_id = create_response.json()["id"]

    update_data = {
        "name": "Greek Salad",
        "ingredients": "Lettuce, Tomato, Cucumber, Feta",
        "price": 5.99,
        "calories": 250,
        "category": "Appetizer"
    }
    response = client.put(f"/menu/{menu_item_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Greek Salad"

def test_delete_menu_item():
    menu_item = {
        "name": "Pasta",
        "ingredients": "Pasta, Sauce, Cheese",
        "price": 6.99,
        "calories": 600,
        "category": "Main"
    }
    create_response = client.post("/menu/", json=menu_item)
    menu_item_id = create_response.json()["id"]

    response = client.delete(f"/menu/{menu_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == menu_item_id
    assert data["name"] == "Pasta"

    # Try deleting again, should return 404
    response = client.delete(f"/menu/{menu_item_id}")
    assert response.status_code == 404
