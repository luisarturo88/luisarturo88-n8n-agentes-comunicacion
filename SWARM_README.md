# Sistema de Enjambre de Agentes

## Arquitectura
Agentes autonomos se comunican via GitHub.

### Flujo
1. **Mensajero**: Recibe ordenes via webhook, escribe en /ordenes/
2. **Trabajador**: Detecta cambios en /ordenes/, ejecuta tareas via API n8n
3. **Consenso**: Propuestas en /propuestas/, revision cruzada
4. **Lock**: Archivos .lock evitan procesamiento duplicado

### Reglas
- Ordenes: `orden_AGENTE_FECHA.json`
- Resultados: /resultados/ con mismo nombre
- Errores: /errores/ con contexto completo
- Lock: crear antes de procesar, eliminar al terminar
