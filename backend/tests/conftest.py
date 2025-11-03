"""
Pytest configuration and shared fixtures
"""
import os
import sys
from pathlib import Path
from typing import Generator, AsyncGenerator
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set test environment before importing app modules
os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["CACHE_ENABLED"] = "false"

from app.models.base import Base
from app.api.deps import get_db
from app.config.redis import RedisClient

# Test database URL - use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Faker instance for test data
fake = Faker(['es_ES'])


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create test database tables before all tests
    Drop tables after all tests
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    # Clean up test database file
    if os.path.exists("./test.db"):
        try:
            os.remove("./test.db")
        except PermissionError:
            # On Windows, sometimes the file is locked
            pass


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session for each test
    Rollback after test to maintain isolation
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with dependency overrides
    """
    # Import app here to avoid connection issues at module load
    from app.main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def mock_redis(mocker):
    """
    Mock Redis client for cache tests
    """
    mock_client = mocker.MagicMock()
    mocker.patch.object(RedisClient, 'get_client', return_value=mock_client)
    return mock_client


@pytest.fixture
def test_image_path() -> Generator[Path, None, None]:
    """
    Create a temporary test image file
    """
    from PIL import Image

    # Create a simple test image
    test_image_dir = Path("./test_images")
    test_image_dir.mkdir(exist_ok=True)

    test_image_path = test_image_dir / "test_product.jpg"
    img = Image.new('RGB', (800, 600), color='red')
    img.save(test_image_path, 'JPEG')

    yield test_image_path

    # Cleanup
    if test_image_path.exists():
        test_image_path.unlink()
    if test_image_dir.exists():
        test_image_dir.rmdir()


@pytest.fixture
def sample_user_data() -> dict:
    """
    Generate sample user data for tests
    """
    return {
        "email": fake.email(),
        "username": fake.user_name(),
        "password": "Test123!@#",
        "full_name": fake.name(),
    }


@pytest.fixture
def sample_product_data() -> dict:
    """
    Generate sample product data for tests
    """
    return {
        "name": fake.word().title() + " Product",
        "description": fake.sentence(),
        "price": float(fake.random_int(min=100, max=10000)) / 100,
        "stock": fake.random_int(min=0, max=100),
        "category_id": 1,
    }


@pytest.fixture
def sample_category_data() -> dict:
    """
    Generate sample category data for tests
    """
    return {
        "name": fake.word().title(),
        "description": fake.sentence(),
    }


@pytest.fixture
def sample_order_data() -> dict:
    """
    Generate sample order data for tests
    """
    return {
        "status": "pending",
        "total_amount": float(fake.random_int(min=1000, max=50000)) / 100,
        "shipping_address": fake.address(),
    }


# Markers for test organization
def pytest_configure(config):
    """
    Register custom markers
    """
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "auth: Authentication tests")
    config.addinivalue_line("markers", "products: Product-related tests")
    config.addinivalue_line("markers", "categories: Category-related tests")
    config.addinivalue_line("markers", "orders: Order-related tests")
    config.addinivalue_line("markers", "cart: Cart-related tests")
    config.addinivalue_line("markers", "cache: Cache-related tests")
    config.addinivalue_line("markers", "images: Image processing tests")
