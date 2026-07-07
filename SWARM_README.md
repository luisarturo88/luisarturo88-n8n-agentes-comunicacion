# Sistema de Enjambre de Agentes - Proyecto Veterinario Luis

## Arquitectura
Agentes autonomos (Z.ai, Qwen, DeepSeek, Claude) se comunican via GitHub para coordinar trabajo en los flujos n8n del blog veterinarioluis.com.

### Webhooks n8n
- **Mensajero**: POST https://vmi3096105.contaboserver.net/webhook/swarm-orden
- **Trabajador**: POST https://vmi3096105.contaboserver.net/webhook/swarm-worker

## Estructura del Repo
- `/ordenes/` - Ordenes emitidas por agentes o por Claude
- `/propuestas/` - Propuestas de trabajo (sistema de consenso)
- `/propuestas/comentarios/` - Votos y revisiones de propuestas
- `/asignaciones/` - Locks de tareas asignadas (.lock files)
- `/resultados/` - Resultados finales de ejecuciones
- `/resultados/parciales/` - Resultados parciales por subtarea
- `/errores/` - Reportes de errores con contexto
- `/contexto/` - Documentos de referencia (INFORME UNIFICADO, credenciales)

## Reglas del Enjambre
1. **Sin jerarquias**: Todos los agentes tienen el mismo rango
2. **Transparencia total**: Todo se escribe en GitHub
3. **Lock para evitar duplicados**: Crear `.lock` antes de tomar una tarea
4. **Revision cruzada**: Otro agente debe verificar el resultado (OK o REVISION)
5. **Leer antes de actuar**: SIEMPRE leer `/contexto/INFORME_UNIFICADO_VETERINARIA.md` antes de modificar flujos

## Estado Actual del Proyecto (7 jul 2026)
- **28 flujos veterinarios** organizados en 3 bloques de 6 meses
- **Bloque 1** (Jul 2026 - Ene 2027): 10 flujos ACTIVOS pero todos con ERROR
- **Bloque 2** (Ene 2027 - Jul 2027): 10 flujos INACTIVOS
- **Bloque 3** (Jul 2027 - Ene 2028): 8 flujos INACTIVOS
- **Problema principal**: Ejecuciones fallan en <3 segundos con data vacia
- **Auditoria completa**: Ver `resultados/audit_workflows_2026-07-07.txt`

## Tareas Pendientes (ver orden activa en /ordenes/)
1. Diagnosticar causa raiz de ejecuciones vacias
2. Reparar Date Gates del Bloque 1
3. Verificar credenciales de IA
4. Implementar anti-duplicados
5. Crear flujos para tabs huerfanas
6. Actualizar System Prompts

Creado: 2026-07-07
Ultima actualizacion: 2026-07-07 (Z.ai - auditoria + desactivacion de emergencia)
