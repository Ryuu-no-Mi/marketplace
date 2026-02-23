# Marketplace Backend

Backend escalable para una plataforma de marketplace, implementado con **Arquitectura Hexagonal (Ports & Adapters)**.

## Estructura del Proyecto

```
app/
├── api/                      # Capa de Presentación (FastAPI)
│   ├── schemas.py           # DTOs (Data Transfer Objects)
│   └── product_router.py    # Rutas de la API
├── application/             # Capa de Aplicación
│   └── use_cases/           # Casos de uso
│       └── create_product.py
├── domain/                  # Capa de Dominio (Lógica de Negocio Pura)
│   ├── entities/            # Entidades del dominio
│   │   └── product.py       # Entidad Product
│   └── repositories/        # Interfaces (puertos)
│       └── product_repository.py
├── infrastructure/          # Capa de Infraestructura
│   ├── repositories/        # Implementaciones (adaptadores)
│   │   ├── models.py        # Modelos SQLAlchemy
│   │   └── sqlalchemy_product_repository.py
│   └── __init__.py
└── core/
    └── database.py          # Configuración de BD

```

## Principios Arquitectónicos

✅ **Dominio Puro**: Sin dependencias de frameworks (FastAPI, SQLAlchemy)
✅ **Inversión de Dependencias**: Las implementaciones dependen de abstracciones
✅ **Separación de Capas**: Cada capa con responsabilidades claras
✅ **Inyección de Dependencias**: Acoplamiento débil entre componentes

## Tecnologías

- **FastAPI** - Framework web
- **SQLAlchemy** - ORM
- **Pydantic** - Validación de datos
- **PostgreSQL** - Base de datos

## Configuración

1. Crear entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate      # Windows
```

2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Ejecutar con Uvicorn:

```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Productos

- **POST** `/products/` - Crear un producto
    ```json
    {
        "name": "Laptop",
        "price": 999.99
    }
    ```

## Flujo de una Petición

```
HTTP POST /products/
    ↓
FastAPI Router (api/product_router.py)
    ↓
Caso de Uso (application/use_cases/CreateProduct)
    ↓
Entidad de Dominio (domain/entities/Product)
    ↓
Repositorio SQLAlchemy (infrastructure/repositories/)
    ↓
Base de Datos
```
