
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import get_db, Base
from app.models import Product, Category


SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    return TestClient(app)

@pytest.fixture
def test_category(db):
    category = Category(name="Electronics")
    db.add(category)
    db.commit()
    db.refresh(category)
    yield category

    db.delete(category)
    db.commit()

@pytest.fixture
def test_products(db, test_category):
    products = [
        Product(name="Laptop", price=1200.0, quantity=10, category_id=test_category.id),
        Product(name="Mouse", price=25.0, quantity=50, category_id=test_category.id),
        Product(name="Keyboard", price=75.0, quantity=30, category_id=test_category.id),
    ]
    db.add_all(products)
    db.commit()
    yield products

    for product in products:
        db.delete(product)
    db.commit()
