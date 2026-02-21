"""
EJEMPLOS DE USO DE LA API

Este archivo muestra cómo usar los endpoints implementados.
"""

# ============================================================================

# PRE-REQUISITOS

# ============================================================================

"""

1. Instalar dependencias:
   pip install -r requirements.txt

2. Iniciar servidor:
   uvicorn app.main:app --reload

3. Acceder a documentación:
   http://localhost:8000/docs (Swagger UI)
   http://localhost:8000/redoc (ReDoc)
   """

# ============================================================================

# EJEMPLOS CON CURL

# ============================================================================

"""
╔════════════════════════════════════════════════════════════════════════════╗
║ CATEGORÍAS - CREAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X POST "http://localhost:8000/api/v1/categories/" \\
-H "Content-Type: application/json" \\
-d '{
"name": "Electronics",
"description": "Electronic devices and accessories"
}'

Response (201):
{
"id": "550e8400-e29b-41d4-a716-446655440000",
"name": "Electronics",
"description": "Electronic devices and accessories",
"is_active": true,
"created_at": "2026-02-21T10:30:00",
"updated_at": "2026-02-21T10:30:00"
}

╔════════════════════════════════════════════════════════════════════════════╗
║ CATEGORÍAS - LISTAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X GET "http://localhost:8000/api/v1/categories/?skip=0&limit=10" \\
-H "Content-Type: application/json"

Response (200):
[
{
"id": "550e8400-e29b-41d4-a716-446655440000",
"name": "Electronics",
"description": "Electronic devices and accessories",
"is_active": true,
"created_at": "2026-02-21T10:30:00",
"updated_at": "2026-02-21T10:30:00"
}
]

╔════════════════════════════════════════════════════════════════════════════╗
║ CATEGORÍAS - OBTENER POR ID ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X GET "http://localhost:8000/api/v1/categories/550e8400-e29b-41d4-a716-446655440000" \\
-H "Content-Type: application/json"

Response (200):
{
"id": "550e8400-e29b-41d4-a716-446655440000",
"name": "Electronics",
"description": "Electronic devices and accessories",
"is_active": true,
"created_at": "2026-02-21T10:30:00",
"updated_at": "2026-02-21T10:30:00"
}

╔════════════════════════════════════════════════════════════════════════════╗
║ CATEGORÍAS - ACTUALIZAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X PUT "http://localhost:8000/api/v1/categories/550e8400-e29b-41d4-a716-446655440000" \\
-H "Content-Type: application/json" \\
-d '{
"name": "Electronics & Gadgets",
"description": "Updated description",
"is_active": true
}'

Response (200):
{
"id": "550e8400-e29b-41d4-a716-446655440000",
"name": "Electronics & Gadgets",
"description": "Updated description",
"is_active": true,
"created_at": "2026-02-21T10:30:00",
"updated_at": "2026-02-21T10:35:00"
}

╔════════════════════════════════════════════════════════════════════════════╗
║ CATEGORÍAS - ELIMINAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X DELETE "http://localhost:8000/api/v1/categories/550e8400-e29b-41d4-a716-446655440000" \\
-H "Content-Type: application/json"

Response (204): No content

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - CREAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X POST "http://localhost:8000/api/v1/products/" \\
-H "Content-Type: application/json" \\
-d '{
"name": "Dell XPS 13",
"description": "Ultra-slim 13-inch laptop with powerful performance",
"sku": "DELL-XPS-13-2026",
"price": 1299.99,
"category_id": "550e8400-e29b-41d4-a716-446655440000",
"stock_quantity": 50
}'

Response (201):
{
"id": "660f9511-f30c-52e5-b827-557766551111",
"name": "Dell XPS 13",
"description": "Ultra-slim 13-inch laptop with powerful performance",
"sku": "DELL-XPS-13-2026",
"price": 1299.99,
"currency": "USD",
"category_id": "550e8400-e29b-41d4-a716-446655440000",
"seller_id": "770g0622-g41d-63f6-c838-668877662222",
"stock_quantity": 50,
"is_active": true,
"created_at": "2026-02-21T10:40:00",
"updated_at": "2026-02-21T10:40:00"
}

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - BUSCAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X GET "http://localhost:8000/api/v1/products/search/query?q=laptop&skip=0&limit=10" \\
-H "Content-Type: application/json"

Response (200):
[
{
"id": "660f9511-f30c-52e5-b827-557766551111",
"name": "Dell XPS 13",
"description": "Ultra-slim 13-inch laptop with powerful performance",
"sku": "DELL-XPS-13-2026",
"price": 1299.99,
"currency": "USD",
"category_id": "550e8400-e29b-41d4-a716-446655440000",
"seller_id": "770g0622-g41d-63f6-c838-668877662222",
"stock_quantity": 50,
"is_active": true,
"created_at": "2026-02-21T10:40:00",
"updated_at": "2026-02-21T10:40:00"
}
]

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - POR CATEGORÍA ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X GET "http://localhost:8000/api/v1/products/category/550e8400-e29b-41d4-a716-446655440000" \\
-H "Content-Type: application/json"

Response (200):
[
{
"id": "660f9511-f30c-52e5-b827-557766551111",
"name": "Dell XPS 13",
...
}
]

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - POR VENDEDOR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X GET "http://localhost:8000/api/v1/products/seller/770g0622-g41d-63f6-c838-668877662222" \\
-H "Content-Type: application/json"

Response (200):
[
{
"id": "660f9511-f30c-52e5-b827-557766551111",
"name": "Dell XPS 13",
...
}
]

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - ACTUALIZAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X PUT "http://localhost:8000/api/v1/products/660f9511-f30c-52e5-b827-557766551111" \\
-H "Content-Type: application/json" \\
-d '{
"price": 1199.99,
"stock_quantity": 45
}'

Response (200):
{
"id": "660f9511-f30c-52e5-b827-557766551111",
"name": "Dell XPS 13",
"price": 1199.99,
"stock_quantity": 45,
...
}

╔════════════════════════════════════════════════════════════════════════════╗
║ PRODUCTOS - ELIMINAR ║
╚════════════════════════════════════════════════════════════════════════════╝

curl -X DELETE "http://localhost:8000/api/v1/products/660f9511-f30c-52e5-b827-557766551111" \\
-H "Content-Type: application/json"

Response (204): No content
"""

# ============================================================================

# EJEMPLOS CON PYTHON REQUESTS

# ============================================================================

"""
import requests

API_URL = "http://localhost:8000/api/v1"

# CREAR CATEGORÍA

def create_category(name, description):
response = requests.post(
f"{API_URL}/categories/",
json={"name": name, "description": description}
)
assert response.status_code == 201
return response.json()

# CREAR PRODUCTO

def create_product(name, description, sku, price, category_id, stock):
response = requests.post(
f"{API_URL}/products/",
json={
"name": name,
"description": description,
"sku": sku,
"price": price,
"category_id": category_id,
"stock_quantity": stock
}
)
assert response.status_code == 201
return response.json()

# BUSCAR PRODUCTOS

def search_products(query):
response = requests.get(
f"{API_URL}/products/search/query",
params={"q": query}
)
assert response.status_code == 200
return response.json()

# USO

category = create_category("Electronics", "Electronic products")
product = create_product(
name="Dell XPS 13",
description="Ultra-slim laptop",
sku="DELL-XPS-13",
price=1299.99,
category_id=category["id"],
stock=50
)
results = search_products("laptop")
print(results)
"""

# ============================================================================

# EJEMPLOS CON FASTAPI TEST CLIENT

# ============================================================================

"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
response = client.get("/")
assert response.status_code == 200
assert response.json()["status"] == "ok"

def test_create_category():
response = client.post(
"/api/v1/categories/",
json={
"name": "Electronics",
"description": "Electronic devices"
}
)
assert response.status_code == 201
assert response.json()["name"] == "Electronics"

def test_list_categories():
response = client.get("/api/v1/categories/")
assert response.status_code == 200
assert isinstance(response.json(), list)

def test_create_product(): # Crear categoría primero
cat_response = client.post(
"/api/v1/categories/",
json={
"name": "Electronics",
"description": "Electronic devices"
}
)
category_id = cat_response.json()["id"]

    # Crear producto
    response = client.post(
        "/api/v1/products/",
        json={
            "name": "Dell XPS 13",
            "description": "Ultra-slim laptop",
            "sku": "DELL-XPS-13",
            "price": 1299.99,
            "category_id": category_id,
            "stock_quantity": 50
        }
    )
    assert response.status_code == 201
    assert response.json()["name"] == "Dell XPS 13"

"""

# ============================================================================

# CÓDIGOS DE RESPUESTA HTTP

# ============================================================================

"""
✅ 200 OK - Solicitud exitosa

- GET, PUT, DELETE (en algunos casos)

✅ 201 CREATED - Recurso creado exitosamente

- POST para crear nuevos recursos

✅ 204 NO CONTENT - Solicitud exitosa sin contenido

- DELETE

✅ 400 BAD REQUEST - Error de validación o negocio

- Entidad no válida
- Datos insuficientes
- Violación de restricuenciones de negocio

✅ 404 NOT FOUND - Recurso no encontrado

- ID que no existe

✅ 500 INTERNAL SERVER ERROR - Error del servidor

- Errores no controlados
  """

# ============================================================================

# ESTRUCTURA DE ERRORES

# ============================================================================

"""
Error 400 BAD REQUEST:
{
"detail": "Category name must be at least 2 characters"
}

Error 404 NOT FOUND:
{
"detail": "Category 550e8400-e29b-41d4-a716-446655440000 not found"
}

Error 500 INTERNAL SERVER ERROR:
{
"detail": "Internal server error"
}
"""
