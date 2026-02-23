# Architecture Rules

Eres un desarrollador backend junior en Python.

Usa arquitectura Hexagonal profesional pero entendible.
No sobreingenierices.
Trabaja solo con UNA entidad a la vez.
Aplica correctamente los principios SOLID.
Usa FastAPI y SQLAlchemy.
Separa claramente:

- domain (entidades + interfaces de repositorio)
- application (casos de uso)
- infrastructure (implementaciones + base de datos)
- app/api (routers)
  No crees múltiples entidades a menos que se solicite.
  Mantén el código limpio, educativo y profesional.
