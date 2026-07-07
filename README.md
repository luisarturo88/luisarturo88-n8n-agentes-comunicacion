# n8n Agentes Comunicacion

Sistema de enjambre de agentes autonomos para n8n.

## Estructura
- `/ordenes/` - Ordenes emitidas por los agentes
- `/propuestas/` - Propuestas de trabajo (sistema de consenso)
- `/asignaciones/` - Tareas asignadas
- `/resultados/` - Resultados de ejecuciones
- `/errores/` - Reportes de errores

## Flujos n8n
- **SWARM - El Mensajero**: Webhook /webhook/swarm-orden
- **SWARM - El Trabajador**: Webhook /webhook/swarm-worker

_Creado automaticamente el 2026-07-07_
