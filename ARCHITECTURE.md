# Hexagonal Architecture - Marketplace Project

## Descripción General

Este proyecto implementa una **Arquitectura Hexagonal (Ports & Adapters)** moderna, escalable y siguiendo principios **SOLID** y **Clean Architecture**.

## Estructura del Proyecto

```
app/
├── domain/                          # Capa de Dominio (Core del negocio)
│   ├── entities/                   # Entidades del dominio
│   ├── value_objects/              # Objetos de valor
│   ├── ports/                      # Puertos (interfaces de repositorios)
│   └── exceptions/                 # Excepciones del dominio
│
├── application/                     # Capa de Aplicación
│   ├── use_cases/                  # Casos de uso
│   ├── dtos/                       # Data Transfer Objects
│   └── mappers/                    # Mappers (DTO ↔ Entidades)
│
├── infrastructure/                  # Capa de Infraestructura
│   ├── repositories/               # Implementaciones de puertos
│   └── config/                     # Inyección de dependencias
│
├── presentation/                    # Capa de Presentación
│   ├── api/                        # Routers y endpoints
│   └── schemas/                    # Esquemas Pydantic para validación
│
├── core/                           # Configuración base
│   └── database.py                 # Configuración de BD
│
└── main.py                        # Punto de entrada de la aplicación
```

## Principios Arquitectónicos

### 1. **Hexagonal Architecture**

- El **dominio está al centro** y completamente aislado de dependencias externas
- **Puertos** (interfaces) definen los contratos de comunicación
- **Adaptadores** (implementaciones) conectan el dominio con sistemas externos

### 2. **Capas e Inversión de Dependencias**

```
Presentation Layer (endpoints)
         ↓
Application Layer (use cases, DTOs)
         ↓
Domain Layer (entities, ports) ← Aquí vive la lógica de negocio
         ↑
Infrastructure Layer (repositories, DB)
```

**Regla Clave**: Las capas internas nunca dependen de las capas externas. El dominio es completamente independiente.

### 3. **Responsabilidades de Cada Capa**

#### **Domain Layer** (Núcleo del Negocio)

- **Entities**: Objetos con identidad única (ej: `Product`, `Order`, `User`)
- **Value Objects**: Objetos sin identidad que modelan conceptos (ej: `Money`, `Email`, `Address`)
- **Ports**: Interfaces que definen cómo el dominio interactúa con el mundo exterior
- **Exceptions**: Excepciones del dominio

**Características**:

- No tiene dependencias externas
- Contiene la lógica de negocio pura
- Implementa reglas de negocio y validaciones

#### **Application Layer** (Orquestación)

- **Use Cases**: Implementan procesos de negocio coordinando entidades y puertos
- **DTOs**: Objetos de transferencia de datos (request/response)
- **Mappers**: Convierten entre entidades y DTOs

**Características**:

- Orquesta la lógica del dominio
- No accede directamente a bases de datos
- Comunica con el dominio a través de entidades

#### **Infrastructure Layer** (Detalles Técnicos)

- **Repository Implementations**: Implementan los puertos del dominio
- **Config**: Inyección de dependencias y configuración

**Características**:

- Implementa los puertos definidos en el dominio
- Maneja persistencia, bases de datos, APIs externas

#### **Presentation Layer** (Interfaces de Usuario)

- **Routers**: Endpoints de FastAPI
- **Schemas**: Validación de requests/responses con Pydantic

**Características**:

- Puerta de entrada a la aplicación
- Valida y formatea datos para cliente
- Maneja errores HTTP

### 4. **Principios SOLID**

- **S**ingle Responsibility: Cada clase tiene una responsabilidad única
- **O**pen/Closed: Abierta para extensión (nuevos adapters), cerrada para modificación
- **L**iskov Substitution: Los puertos (interfaces) permiten intercambiar implementaciones
- **I**nterface Segregation: Interfaces específicas (ports) pequeñas y coherentes
- **D**ependency Inversion: Dependencias inyectadas, no creadas internamente

## Ejemplo de Flujo

### Crear un Producto

```
1. Cliente envía POST /api/v1/products
                ↓
2. ProductRouter recibe el request (estrategia)
                ↓
3. ProductSchema valida datos (Pydantic)
                ↓
4. CreateProductUseCase orquesta el proceso
                ↓
5. Valida existencia de categoría (CategoryRepository)
                ↓
6. Crea entidad Product (Domain Layer)
                ↓
7. Guarda en BD (SQLAlchemyProductRepository)
                ↓
8. Mapea a ProductDTO
                ↓
9. DevuelveProductSchema al cliente
```

## Ventajas de esta Arquitectura

✅ **Testeable**: Dominio sin dependencias, fácil de testear
✅ **Flexible**: Cambiar de BD o adaptadores sin tocar dominio
✅ **Escalable**: Nuevos casos de uso sin afectar código existente
✅ **Mantenible**: Código organizado y responsabilidades claras
✅ **Independiente de Frameworks**: Dominio no sabe de FastAPI o SQLAlchemy
✅ **SOLID**: Aplicación de principios modernos de OOP

## Flujo de Datos con DTOs

```
Request (JSON)
      ↓
Schema (Validación Pydantic)
      ↓
DTO (Objeto de datos interno)
      ↓
Entity (Dominio)
      ↓
Repository (Infraestructura)
      ↓
Database
      ↓
Entity (Dominio)
      ↓
DTO (Objeto de datos interno)
      ↓
Schema (Serialización)
      ↓
Response (JSON)
```

## Extensión del Proyecto

Para agregar una nueva entidad (ej: Reviews):

1. **Domain**: Crear `Review` entity, `ReviewRepository` port
2. **Application**: Crear use cases (`CreateReviewUseCase`, etc.)
3. **Infrastructure**: Implementar `SQLAlchemyReviewRepository`
4. **Presentation**: Crear `review_routes.py` y `ReviewSchema`

Sin tocar código existente (Open/Closed Principle).

## Configuración

Las dependencias se inyectan a través de `RepositoryContainer`, permitiendo:

- Cambiar implementaciones sin modificar use cases
- Testear con mocks fácilmente
- Mantener separación de responsabilidades

## Próximos Pasos

- [ ] Implementar autenticación/autorización
- [ ] Agregar tests unitarios y de integración
- [ ] Implementar logging centralizado
- [ ] Agregar validaciones más complejas en el dominio
- [ ] Implementar eventos de dominio
- [ ] Agregar caching
- [ ] Implementar paginación mejorada
