"""
Guía de Testing para Arquitectura Hexagonal

Este archivo muestra cómo testear cada capa de la arquitectura.
"""

# ============================================================================

# PASO 1: Testear Domain Entities (Sin dependencias externas)

# ============================================================================

# tests/domain/test_entities.py

import pytest
from decimal import Decimal
from uuid import uuid4

from app.domain.entities import Product, Category
from app.domain.value_objects import Money
from app.domain.exceptions import InvalidEntityError, InsufficientInventoryError

class TestProduct:
"""Test Product entity."""

    def test_create_product_success(self):
        """Test creating a valid product."""
        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )
        assert product.name == "Laptop"
        assert product.stock_quantity == 10

    def test_create_product_invalid_name(self):
        """Test creating product with invalid name."""
        with pytest.raises(InvalidEntityError):
            Product(
                name="A",  # Too short
                description="High-performance laptop",
                sku="LAPTOP-001",
                price=Money(Decimal("999.99")),
                category_id=uuid4(),
                seller_id=uuid4(),
                stock_quantity=10
            )

    def test_reduce_stock_success(self):
        """Test reducing product stock."""
        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )
        product.reduce_stock(3)
        assert product.stock_quantity == 7

    def test_reduce_stock_insufficient_inventory(self):
        """Test reducing stock when insufficient."""
        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=5
        )
        with pytest.raises(InsufficientInventoryError):
            product.reduce_stock(10)

    def test_increase_stock_success(self):
        """Test increasing product stock."""
        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )
        product.increase_stock(5)
        assert product.stock_quantity == 15

class TestValueObjects:
"""Test Value Objects."""

    def test_money_creation(self):
        """Test creating Money value object."""
        money = Money(Decimal("100.00"), "USD")
        assert money.amount == Decimal("100.00")
        assert money.currency == "USD"

    def test_money_negative_amount(self):
        """Test Money with negative amount."""
        with pytest.raises(ValueError):
            Money(Decimal("-100.00"), "USD")

    def test_money_addition(self):
        """Test adding Money objects."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("50.00"), "USD")
        result = money1 + money2
        assert result.amount == Decimal("150.00")

    def test_money_different_currencies(self):
        """Test adding Money with different currencies."""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("50.00"), "EUR")
        with pytest.raises(ValueError):
            money1 + money2

# ============================================================================

# PASO 2: Testear Use Cases (Con mocks de repositorios)

# ============================================================================

# tests/application/test_use_cases.py

import pytest
from unittest.mock import AsyncMock, MagicMock
from decimal import Decimal
from uuid import uuid4

from app.application.use_cases import CreateProductUseCase
from app.domain.entities import Product
from app.domain.value_objects import Money
from app.domain.exceptions import EntityNotFoundError
from app.application.dtos import CreateProductRequest

class TestCreateProductUseCase:
"""Test CreateProductUseCase."""

    @pytest.mark.asyncio
    async def test_create_product_success(self):
        """Test successful product creation."""
        # Mock repositories
        product_repo = AsyncMock()
        category_repo = AsyncMock()

        # Setup mock responses
        category_repo.get_by_id.return_value = MagicMock()  # Category exists
        product_repo.add.return_value = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )

        # Execute use case
        use_case = CreateProductUseCase(product_repo, category_repo)
        request = CreateProductRequest(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Decimal("999.99"),
            category_id=uuid4(),
            stock_quantity=10
        )

        result = await use_case.execute(request, uuid4())

        assert result.name == "Laptop"
        assert product_repo.add.called

    @pytest.mark.asyncio
    async def test_create_product_category_not_found(self):
        """Test creating product with non-existent category."""
        # Mock repositories
        product_repo = AsyncMock()
        category_repo = AsyncMock()

        # Setup mock - category doesn't exist
        category_repo.get_by_id.return_value = None

        # Execute use case
        use_case = CreateProductUseCase(product_repo, category_repo)
        request = CreateProductRequest(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Decimal("999.99"),
            category_id=uuid4(),
            stock_quantity=10
        )

        with pytest.raises(EntityNotFoundError):
            await use_case.execute(request, uuid4())

# ============================================================================

# PASO 3: Testear Repositorios (Con base de datos de test)

# ============================================================================

# tests/infrastructure/test_repositories.py

import pytest
from decimal import Decimal
from uuid import uuid4
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.infrastructure.repositories import SQLAlchemyProductRepository
from app.domain.entities import Product
from app.domain.value_objects import Money

@pytest.fixture
async def test*db():
"""Create test database."""
engine = create_async_engine("sqlite+aiosqlite:///:memory:")
SessionLocal = sessionmaker(
engine, class*=AsyncSession, expire_on_commit=False
)

    async with engine.begin() as conn:
        # Create tables
        from app.core.database import Base
        await conn.run_sync(Base.metadata.create_all)

    async with SessionLocal() as session:
        yield session

    await engine.dispose()

class TestProductRepository:
"""Test ProductRepository."""

    @pytest.mark.asyncio
    async def test_add_product(self, test_db):
        """Test adding a product."""
        repo = SQLAlchemyProductRepository(test_db)

        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )

        result = await repo.add(product)

        assert result.id == product.id
        assert result.name == "Laptop"

    @pytest.mark.asyncio
    async def test_get_by_id(self, test_db):
        """Test getting product by ID."""
        repo = SQLAlchemyProductRepository(test_db)

        product = Product(
            name="Laptop",
            description="High-performance laptop",
            sku="LAPTOP-001",
            price=Money(Decimal("999.99")),
            category_id=uuid4(),
            seller_id=uuid4(),
            stock_quantity=10
        )

        await repo.add(product)
        result = await repo.get_by_id(product.id)

        assert result is not None
        assert result.name == "Laptop"

    @pytest.mark.asyncio
    async def test_get_nonexistent_product(self, test_db):
        """Test getting non-existent product."""
        repo = SQLAlchemyProductRepository(test_db)
        result = await repo.get_by_id(uuid4())
        assert result is None

# ============================================================================

# PASO 4: Testear API Endpoints (Integration Tests)

# ============================================================================

# tests/presentation/test_routes.py

import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.main import app

@pytest.fixture
def client():
"""Create test client."""
return TestClient(app)

class TestCategoryRoutes:
"""Test Category routes."""

    def test_health_check(self, client):
        """Test health check endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    @patch('app.infrastructure.config.RepositoryContainer.get_category_repository')
    def test_create_category(self, mock_repo, client):
        """Test creating a category."""
        # Mock repository
        mock_repo_instance = AsyncMock()
        mock_repo.return_value = mock_repo_instance

        response = client.post(
            "/api/v1/categories/",
            json={
                "name": "Electronics",
                "description": "Electronic products"
            }
        )

        # Status should be 201 or 200
        assert response.status_code in [200, 201]

# ============================================================================

# CONFIGURACIÓN DE PYTEST

# ============================================================================

# pytest.ini

"""
[pytest]
asyncio*mode = auto
testpaths = tests
python_files = test*_.py
python_classes = Test_
python*functions = test*\*
"""

# pyproject.toml

"""
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
"""

# ============================================================================

# EJECUTAR TESTS

# ============================================================================

"""

# Todos los tests

pytest

# Tests de una carpeta

pytest tests/domain/

# Tests de un archivo

pytest tests/domain/test_entities.py

# Tests de una clase

pytest tests/domain/test_entities.py::TestProduct

# Un test específico

pytest tests/domain/test_entities.py::TestProduct::test_create_product_success

# Con cobertura

pytest --cov=app tests/

# Verbose

pytest -v

# Por marcas

pytest -m "not slow"
"""

# ============================================================================

# MARCAS DE TESTS ÚTILES

# ============================================================================

"""

# conftest.py

import pytest

def pytest_configure(config):
config.addinivalue_line(
"markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
)
config.addinivalue_line(
"markers", "integration: marks tests as integration tests"
)

# Usar en tests

@pytest.mark.slow
def test_slow_operation():
pass

@pytest.mark.integration
def test_database_integration():
pass

# Ejecutar

pytest -m "not slow" # Todos excepto lentos
pytest -m "integration" # Solo integración
"""
