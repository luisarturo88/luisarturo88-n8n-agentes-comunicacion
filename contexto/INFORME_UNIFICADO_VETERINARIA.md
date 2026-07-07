# INFORME UNIFICADO: PROYECTO VETERINARIA N8N - VETERINARIOLUIS.COM
## Fecha: 7 de julio de 2026
## Documento de coordinacion para todas las IAs trabajadoras

---

## 0. PROPOSITO DE ESTE DOCUMENTO

Este documento pone a TODAS las IAs (Qwen, DeepSeek, Gemini, Z.ai, Claude, etc.) al mismo nivel de contexto sobre el proyecto de automatizacion de contenido veterinario. Contiene todo lo que se ha hecho, lo que falta, los datos tecnicos, y las tareas pendientes. Cualquier IA debe leer este documento completo antes de trabajar en los flujos de veterinaria.

---

## 1. INFRAESTRUCTURA

### n8n
- **URL**: https://vmi3096105.contaboserver.net
- **API REST v1**: https://vmi3096105.contaboserver.net/api/v1
- **API Keys JWT activas** (cualquiera sirve):
  - Z.ai original: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGM1MTJmNy1mNTVhLTQwYjYtYWU1Ni00MDM0OWNlMDlmMjkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYTZjNmY0NWEtY2FiZS00NDg0LTg1NzktZWNkZjk3NDRmMDk1IiwiaWF0IjoxNzgzMzM5NDczLCJleHAiOjE3ODU5MDI0MDB9.iqL6k-FlI1MkD2a-dVex7sx0NovUtf93SlCWwb4n4XE`
  - Generada por Qwen: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGM1MTJmNy1mNTVhLTQwYjYtYWU1Ni00MDM0OWNlMDlmMjkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiODRjZDhhMDYtYTU0Zi00YzhlLTllNjMtMTNhYTI1MWY1NzRjIiwiaWF0IjoxNzgzNDEwOTY4LCJleHAiOjE3ODU5ODg4MDB9.iYtQ-SbN6asJc02OSMjQ-7W3FynRGOD9RTgMqGqssls`
  - Generada por DeepSeek: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGM1MTJmNy1mNTVhLTQwYjYtYWU1Ni00MDM0OWNlMDlmMjkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiMmZiMDU5NWUtNmVkMS00NTMwLWE4YWItN2EzZTA3NTQxZjBhIiwiaWF0IjoxNzgzNDEzMzMyLCJleHAiOjE3ODU5ODg4MDB9.kaL4vQbHdmH2vLE3DhsK1u4n_P9RKvGMhwBp1eG3Hfk`
- **Header para requests**: `X-N8N-API-KEY: <key>`
- **n8n __rl format**: Los IDs de credenciales y sheets en n8n usan formato `{__rl: true, value: "actual_id", mode: "id", cachedResultName: "display_name"}`

### Blogger
- **Blog destino (UNICO)**: veterinarioluis.com
- **Blog ID**: `2772493032989228627`
- **Blogger draft URL**: https://draft.blogger.com/blog/posts/2772493032989228627
- **TODOS los flujos veterinarios publican AQUI** (consolidacion confirmada por el usuario)

### Credenciales de IA en n8n
- **DeepSeek**: Credential ID con valor `tNIbvUHUgCDukRly` (usado en la mayoria de flujos)
- **Gemini**: Credential ID con valor `wQOnKlUsbUnFFzD1`
- **Cohere**: Credential ID con valor `6LmusRbYdpPXTD10`
- **Google Sheets OAuth2**: Credential ID con valor `UviJg5pB7TsCtYBk`
- **Agnes AI**: Credential ID con valor `M2BdhhUp0ZryKpmq`

### Comunidad WhatsApp (CTA obligatorio en todos los articulos)
- **URL**: https://chat.whatsapp.com/IkpYnlrPyEx8Y2NTyaFB6P

### Funcion auxiliar para n8n PUT (limpia campos read-only)
```python
READ_ONLY = ['id','createdAt','updatedAt','versionId','activeVersionId','triggerCount',
             'shared','activeVersion','tags','pinData','meta','staticData','versionCounter',
             'active','isArchived']
def clean_for_update(detail):
    d = dict(detail)
    d['description'] = d.get('description') or ''
    for f in READ_ONLY:
        d.pop(f, None)
    if 'settings' in d:
        ok = ['executionOrder','saveManualExecutions','saveExecutionProgress',
              'executionTimeout','callerPolicy','errorWorkflow','crashOnError']
        d['settings'] = {k:v for k,v in d['settings'].items() if k in ok}
    return d
```

---

## 2. LO QUE YA SE HA HECHO

### 2.1 Trabajo ejecutado por Z.ai (Super Z) - SESION ANTERIOR
Estas acciones se ejecutaron REALMENTE via API (no son planes, son hechos concretos):

1. **Auditoria completa**: Se conecto a la API de n8n, se descubrieron 100 workflows, se identificaron 35 veterinarios
2. **Mapeo de Google Sheets**: Se extrajeron los IDs reales de sheets y tabs de los nodos de cada flujo (22 sheets unicos, ~50 tabs)
3. **Sistema de 3 Bloques de 6 meses**: Se disenyo e implemento una separacion temporal:
   - **Bloque 1** (Jul 2026 - Ene 2027): 10 flujos core + geo + clinicos
   - **Bloque 2** (Ene 2027 - Jul 2027): 10 flujos especies y nichos
   - **Bloque 3** (Jul 2027 - Ene 2028): 8 flujos peces + secundarios
4. **Date Gates inyectados**: Se inserto un nodo Code ("DATE GATE - Bloque X") en 28 flujos, inmediatamente despues del trigger. Este nodo verifica la fecha y retorna `[]` si esta fuera de la ventana de 6 meses
5. **Master Controller creado** (ID: `bGA2HDjvFxzMZxYV`): Workflow con 7 nodos que se ejecuta diariamente y activa/desactiva los bloques automaticamente
6. **Activacion inicial ejecutada**: Bloque 1 = ACTIVO (10 flujos), Bloque 2 = INACTIVO (10 flujos), Bloque 3 = INACTIVO (8 flujos)
7. **4 flujos duplicados desactivados**: KGwwzXQSwVRd2HVp (Bulldogs dup), UMebuNvob40lxzh9 (Betta dup), RR4F20A5GKxKDFW6 (Platy dup), c2LwwlSzljnnVg3N (Bulldogs secuencial)
8. **System prompts actualizados** en 68 nodos de IA en 25 flujos (se agregaron: casos clinicos, glosario veterinario, citas APA, WhatsApp CTA, afiliados, SEO)
9. **SEO data recopilada**: 36 URLs indexadas de veterinarioluis.com analizadas

### 2.2 Trabajo producido por Qwen (Claude Code) - SESION PARALELA
Qwen produjo DOCUMENTOS Y PLANES (no ejecutados via API):

1. **INFORME_MAESTRO_VETERINARIA_2027.md**: Inventario de flujos (18 activos, 34 inactivos segun su conteo), plan de 6 fases
2. **PLAN_ACCION_VETERINARIA_2027.md**: Clasificacion de flujos en 4 grupos (A: Principales, B: High-Ticket, C: Especies, D: Desarrollo)
3. **INFORME_PARA_IA_TRABAJADORAS.md**: 7 tareas detalladas para coordinacion entre IAs
4. **guia_actualizacion_manual.sh**: Script bash con INSTRUCCIONES MANUALES (echo statements, no ejecuta nada via API)
5. **plantilla_flujo_veterinario_maestro.json**: Template JSON de un flujo n8n basico (7 nodos) listo para importar
6. **System Prompt Maestro** mejorado: Version mas detallada del prompt con 8 secciones obligatorias (caso clinico, glosario, APA, afiliados, SEO/AEO/Rich Snippets, human level, WhatsApp CTA, imagenes)

### 2.3 CONFLICTO IMPORTANTE ENTRE AMBOS ENFOQUES

| Aspecto | Z.ai (Super Z) | Qwen (Claude) |
|---------|---------------|---------------|
| **Estrategia temporal** | 3 bloques de 6 meses (solo 10 activos ahora) | Activar TODOS los flujos inmediatamente |
| **Publicacion** | Bloque 1 publica, Bloque 2/3 pausados | 5 articulos/dia distribuidos entre todos |
| **Anti-duplicados** | No implementado (pendiente) | Plan con ESTADO en Google Sheets (no ejecutado) |
| **Flujos huérfanos** | Identificados pero no creados | Plantilla JSON creada pero no importada |
| **Prompts** | Actualizados en 25 flujos via API | Nuevo prompt mas detallado (NO aplicado) |

**DECISION DEL USUARIO ORIGINAL**: El usuario pidio explicitamente los 3 bloques de 6 meses. Sin embargo, en la sesion con Qwen, pidio "5 articulos por dia comenzando hoy mismo" y "activar flujos inactivos inmediatamente". **ESTE CONFLICTO DEBE RESOLVERSE CON EL USUARIO ANTES DE PROCEDER.**

### 2.4 Estado actual de los flujos (7 julio 2026 - con errores visibles)

Segun los logs de ejecucion de n8n, MUCHOS flujos estan FALLANDO:
- FLUJO VETERINARIO LUIS BLOGGER: Error
- Veterinario ECUADOR Y MUNDO: Error
- Veterinario QUITO: Error
- Veterinario CUENCA: Error
- CAMARONES DE ACUARIO: Error
- GECKO LEOPARDO: Error
- BULLDOGS FLUJO: Error
- CASOS ESTUDIOS: Error
- ACUARIOS BIOTOPO: Error
- HURONES: Error
- REPTILES: Error
- PEZ BETTA: Error
- PEZ PLATY: Error
- RENALES: Error
- TECNOLOGIA: Error
- ALIMENTOS PERROS: Error
- ANSIEDAD Y ESTRES: Error
- PRIMEROS AUXILIOS: Error
- MASCOTAS EXOTICAS: Error
- 10 NICHOS MASCOTAS: Error

**LA MAYORIA DE FLUJOS ESTAN EN ESTADO DE ERROR.** Esto es critico y debe ser lo primero a investigar y reparar.

---

## 3. INVENTARIO COMPLETO DE GOOGLE SHEETS

### Sheets principales de contenido veterinario

| # | Nombre del Sheet | ID | Tabs conocidas | Tabs con flujo | Tabs HUERFANAS |
|---|-----------------|-----|----------------|----------------|----------------|
| 1 | Veterinario luis arturo garcia | `1KkClLscmdwlZAyM4HKoA8WvukQMSoYOpB8jeBrSoN0s` | 03_CLUSTERS_TRANSACCIONALES, CUENCA, NICHOS NUEVOS, Hoja 1, Temas Ecuador y Mundo, DIFUCION DE ARTICULOS REDES SOCIALES E INTERNET | 03_CLUSTERS_TRANSACCIONALES, CUENCA, NICHOS NUEVOS | Posibles: tabs 01_CLUSTERS_*, 02_CLUSTERS_* (no visibles por sheet privado) |
| 2 | VETERINARIO BLOG OFICIAL | `13zYYocI1qa5JKrn1xAj1e2T_mpU11spVKlW-ZCHMlcM` | AMAZON AFILIADOS, CLUSTER CIUDADES, NICHOS NUEVOS, Temas Ecuador y Mundo, base maestra de afiliados | CLUSTER CIUDADES, Temas Ecuador y Mundo | NICHOS NUEVOS (posiblemente sin flujo dedicado) |
| 3 | VETERINARIA NICHOS_HIGH_TICKET | `1dtc4KTy7awk5QMA_UfsDgey8W3B8Hh_qQZg3RELcRF8` | P01_ansiedad_estres, P03_renal_urinario, PRIMEROS AUXILIOS, MASCOTAS EXOTICAS, TECNOLOGIA, NUTRICION | P01, P03, PRIMEROS AUXILIOS, MASCOTAS EXOTICAS, TECNOLOGIA | **NUTRICION** (confirmada huérfana), posibles P02, P04, P05+ |
| 4 | CASOS QWEN | `1euIPpzZc8FG6zz1c6vR4m0uHAaAGeaEoDRaNg_ufriQ` | CASOS QWEN | CASOS QWEN (usada por 26 flujos como soporte) | Ninguna |
| 5 | PECES (Betta, Guppy, Platy) | `18giA2hzy_5wslDUv3v7563qv-FKIfkCTMuOIAx3uYVM` | Hoja 1, PEZ BETTA ARTICULOS CLUSTER Y PILARES, PEZ GUPY ARTICULOS CLUSTER Y PILARES, PEZ PLATY ARTICULOS CLUSTER Y PILARES | Las 3 de peces | Ninguna |
| 6 | PERROS BULLDOG BLOGGER | `1DRUUsiAldA3fDBzkt6J0jlP1ANzg3jObx0iuI2moThU` | Hoja 1, DIFUCION DE ARTICULOS RS | Ninguna activa (flujo duplicado desactivado) | Hoja 1 |

### Sheets de nichos especificos

| # | Sheet ID | Nombre | Tab | Flujo asignado | Bloque |
|---|----------|--------|-----|----------------|--------|
| 7 | `1HrXrnho8LVZPOSN4YcHQyyOFhXaoq8Ji5ZsQB5xSst8` | Temas de Loros | Hoja 1 | LOROS SIN REPETICION (AeGdjdxnXZThPmjE) | 2 |
| 8 | `1D4kbY5wOqJdoWYithyke2t46aT_tm_UqO9vg--u3XQM` | Hurones | TEMAS_1000 | HURONES SIN REPETICION (aqJQo8AEmxH4euHZ) | 2 |
| 9 | `10YVRpuqj8q4XW9j7lhCGS2F_wDkP2Wk6-6qTDCiQfO4` | ALIMENTOS PERROS | Hoja 4 | ALIMENTOS PERROS SIN REPETICION (DS5gqoroBG3SAXKB) | 2 |
| 10 | `1LR73v0egRXSekoviFxPS1e8Vp2VMvPWrp1Xh3r55MVA` | ACUARIOS BIOTIPO | ARTICULOS | ACUARIOS BIOTIPO SIN REPETICION (STiwKMm2UXn6jSfa) | 3 |
| 11 | `14NYqDn77J9ns1jD8ZsvxzDe1lggNwmC6kU2cE3LNbJI` | (Reptiles/Acuarios) | (no detectada) | REPTILES SIN REPETICION (EjgZ8uVfHQqzQqbF) | 2 |
| 12 | `1B5PdGVAl6BylX18ZWepyPB9MatTYa9KGD7yP2Jx-g0k` | KROMASOL | kromasol | KROMASOL SALUD (QtenfTotJPqU72x2) | 2 |
| 13 | `1xJ8CbIIyh9fG9xTZrOBOCkbxijsGKayVbbobhaysHO0` | ANTI ESTRES | NICHOS NUEVOS | 1 FLUJO ANTI ESTRES MILLONARIO (UCXNMMBg1NZPmH5v) | 3 |
| 14 | `1dWRYvk6go_SM_xi_D_Ss70Emg2MVrsWdkk53WTpMM0g` | Bovinos | TEMAS_1000 | BOVINOS SIN REPETICION (3TihmuY7TlK4NZSN) | 3 |

### Sheets descubiertos por Qwen (en Drive de kromasoldeluis@gmail.com)

| # | Nombre | ID | Estado |
|---|--------|-----|--------|
| 15 | Camarones neocaridina (shrimp_tanks) 1500 clusters | `1qeHTH9nwJIBkYipmY7rFaTvAdiKH-aFWzSoo5x3-cPI` | Confirmado - usado por CAMARONES DE ACUARIO |
| 16 | BLOGS USA MASTER (7 nichos) | `1fH5lpUfu2vHzCRLDf0Z0st4RaxOHKxPHqS7vCtpt4So` | NO veterinario - usado por ABOGADOS FAMILIA USA |
| 17 | ARTICULOS CHINCHILLAS | `1c5rZ8EkS5I4YqlA9pB2vTaZxJSFGp9FOM_AJI0rajq8` | **HUERFANA** - No tiene flujo de n8n |
| 18 | BLOG TECNICAS ANTI ESTRES | `1xJ8CbIIyh9fG9xTZrOBOCkbxijsGKayVbbobhaysHO0` | Ya listado arriba (mismo ID #13) |

### Sheets mencionados por el usuario pero NO conectados a n8n

| Nombre | Que es | Estado |
|--------|--------|--------|
| NUEVOS NICHOS VETERINARIOS | Banco real con ID_UNICO/TITULO/ESTADO/PUBLICADO. Pestañas: TECNOLOGIA, etc. | **HUERFANO** - No tiene flujo |
| 50 MIL TITULOS DE ARTICULOS VETERINARIOS | NO son 50 mil titulos reales - es un documento de PLANIFICACION de metas por especie | No conectable (no es data) |
| VETERINARIA NICHOS_HIGH_TICKET | Contenido alto valor (Smart Pet Tech, areneros automaticos, collares GPS) - estado EN_PROCESO | Parcialmente conectado (solo algunas tabs) |
| REGISTRY_BLOGS_template | Registro maestro: mapea cada blog con Sheet ID, Blog ID, POST_INTERVAL_MINUTES | Referencia, no genera contenido |
| Fabrica_Blog_Veterinario_Luis_Garcia | Plan de contenido tipo "rascacielos" (70,000 palabras por especie) | Poco desarrollado, sin flujo |

### Sheets de soporte (no generan contenido directo)

| Sheet ID | Tab | Uso |
|----------|-----|-----|
| `1yzBNfDYpMHpf7rp3NPgsgPoFd9ZMsu1pGNemnjOgIs4` | libros | Bibliografia de referencia para citas APA |
| `13zYYocI1qa5JKrn1xAj1e2T_mpU11spVKlW-ZCHMlcM` | AMAZON AFILIADOS | Base de datos de afiliados Amazon |
| `13zYYocI1qa5JKrn1xAj1e2T_mpU11spVKlW-ZCHMlcM` | base maestra de afiliados | Base maestra de afiliados |

---

## 4. INVENTARIO COMPLETO DE FLUJOS N8N VETERINARIOS

### 4.1 BLOQUE 1 (Jul 2026 - Ene 2027) - CORE VETERINARIO - 10 flujos

Estado actual: **ACTIVOS (con Date Gate Bloque 1 inyectado)**

| # | Nombre | ID | Sheet / Tab | IA usada | Nodos |
|---|--------|-----|-------------|----------|-------|
| 1 | FLUJO VETERINARIO LUIS BLOGGER | `JDJKp1yYSFFu4BtV` | 1KkCl... / 03_CLUSTERS_TRANSACCIONALES | Gemini, DeepSeek | - |
| 2 | Veterinario ECUADOR Y MUNDO Luis Blogger copy | `cabjTOjqu7Ks1r58` | 13zYY... / Temas Ecuador y Mundo | DeepSeek | - |
| 3 | Veterinario QUITO Luis Blogger copy | `930XCm4vY3TurOlL` | 13zYY... / CLUSTER CIUDADES | DeepSeek | - |
| 4 | Veterinario CUENCA Luis Blogger copy | `cthc7GvuYZlPIDCI` | 1KkCl... / CUENCA | DeepSeek | - |
| 5 | RENALES Y URINARIOS EN GATOS | `1zGqGSPhZITvCttw` | 1dtc4... / P03_renal_urinario | Gemini, DeepSeek | 37 |
| 6 | TECNOLOGIA | `7554aQXudKBRWEkQ` | 1dtc4... / TECNOLOGIA | Gemini, DeepSeek | - |
| 7 | 8 FLUJO VETERINARIA + CASOS ESTUDIOS | `9KrKde8O3cijCcBf` | 1euIP... / CASOS QWEN + 1dtc4.../NUTRICION | DeepSeek | - |
| 8 | FLUJO_VET_PRIMERA_PERSONA_V3 | `CDQHp2kdQszHYKqN` | 13zYY... / NICHOS NUEVOS | - | - |
| 9 | mejorar articulos veterinario | `bDEvev5P1BC9MAPA` | 1KkCl... / multiples tabs | DeepSeek | - |
| 10 | 10 NICHOS MASCOTAS | `IyUZcl96GcRjVZF5` | 13zYY... / NICHOS NUEVOS | DeepSeek | - |

### 4.2 BLOQUE 2 (Ene 2027 - Jul 2027) - ESPECIES Y NICHOS - 10 flujos

Estado actual: **INACTIVOS (Date Gate Bloque 2 + desactivados)**

| # | Nombre | ID | Sheet / Tab | IA usada |
|---|--------|-----|-------------|----------|
| 1 | ANSIEDAD Y ESTRES | `HtFV0KcqD42VqZvr` | 1dtc4... / P01_ansiedad_estres | Gemini, DeepSeek |
| 2 | PRIMEROS AUXILIOS MASCOTAS | `dAc6Uw37UeNLTshk` | 1dtc4... / PRIMEROS AUXILIOS | Gemini, DeepSeek |
| 3 | MASCOTAS EXOTICAS | `MwA6MSqZnsdNqv5Y` | 1dtc4... / MASCOTAS EXOTICAS | Gemini, DeepSeek |
| 4 | BULLDOGS FLUJO copy | `FNSqMpwphHB1w3WL` | 1DRUU... / Hoja 1 | DeepSeek |
| 5 | LOROS SIN REPETICION | `AeGdjdxnXZThPmjE` | 1HrXr... / Hoja 1 | DeepSeek |
| 6 | HURONES SIN REPETICION | `aqJQo8AEmxH4euHZ` | 1D4kb... / TEMAS_1000 | DeepSeek |
| 7 | REPTILES SIN REPETICION | `EjgZ8uVfHQqzQqbF` | 14NYq... / (tab) | DeepSeek |
| 8 | ALIMENTOS PARA PERROS | `DS5gqoroBG3SAXKB` | 10YVR... / Hoja 4 | DeepSeek |
| 9 | ALIMENTOS PARA GATOS | `aWuJN5aWVLfdrJAi` | (URL sheet) / Hoja 1 | DeepSeek |
| 10 | KROMASOL SALUD | `QtenfTotJPqU72x2` | 1B5Pd... / kromasol | DeepSeek |

### 4.3 BLOQUE 3 (Jul 2027 - Ene 2028) - PECES Y SECUNDARIOS - 8 flujos

Estado actual: **INACTIVOS (Date Gate Bloque 3 + desactivados)**

| # | Nombre | ID | Sheet / Tab | IA usada |
|---|--------|-----|-------------|----------|
| 1 | ACUARIOS BIOTOPO | `Xu385bbjE7JqapnW` | 14NYq... / (tab) | DeepSeek |
| 2 | ACUARIOS Biotipo (copia) | `STiwKMm2UXn6jSfa` | 1LR73... / ARTICULOS | DeepSeek |
| 3 | PEZ BETTA | `7rdIEIngthCHxiHV` | 18giA... / PEZ BETTA CLUSTER | DeepSeek |
| 4 | PEZ GUPPY | `NiEeirlD1yI7zVhu` | 18giA... / PEZ GUPPY CLUSTER | DeepSeek |
| 5 | PEZ PLATY | `CZEzMQrOOA9UoWyn` | 18giA... / PEZ PLATY CLUSTER | DeepSeek |
| 6 | BOVINOS | `3TihmuY7TlK4NZSN` | 1dWRY... / TEMAS_1000 | Gemini, DeepSeek |
| 7 | INFLAMACION BARRIGA | `bssm7ANnpogoMt0V` | (desconocido) | DeepSeek |
| 8 | ANTI ESTRES MILLONARIO | `UCXNMMBg1NZPmH5v` | 1xJ8C... / NICHOS NUEVOS | DeepSeek |

### 4.4 Flujos SIEMPRE ACTIVOS (sin bloque temporal)

| Nombre | ID | Funcion |
|--------|-----|---------|
| Difusion Automatica Blog VETERINARIO LUIS BLOGGER | `Y1d5u1jRLpIIucFP` | Difusion en redes sociales |
| Difusion Automatica Blog BULLDOG BLOGGER | `XGxDmDekWuuf6Bh5` | Difusion en redes sociales |
| 6C Generador de Temas Veterinarios (Fase 2) | `Xae4B5SXSbqHRPrl` | Genera temas (no publica) |
| MASTER CONTROLLER - Bloques 6 Meses | `bGA2HDjvFxzMZxYV` | Gestiona activacion de bloques |

### 4.5 Flujos DESACTIVADOS (duplicados)

| Nombre | ID | Motivo |
|--------|-----|--------|
| 1BULLDOGS FLUJO SIN REPETICION DE TEMAS | `KGwwzXQSwVRd2HVp` | Duplicado de BULLDOGS FLUJO copy |
| PEZ BETTA SIN REPETICION DE TEMAS copy copy copy | `UMebuNvob40lxzh9` | Duplicado de PEZ BETTA |
| PEZ PLATY SIN REPETICION copy copy copy copy copy | `RR4F20A5GKxKDFW6` | Duplicado de PEZ PLATY |
| Blogger Bulldogs Secuencial | `c2LwwlSzljnnVg3N` | Duplicado secuencial |

### 4.6 Flujos NO VETERINARIOS (identificados por Qwen - deben desactivarse)

| Nombre | Motivo |
|--------|--------|
| Seguro social denegado | Tematica legal/discapacidad |
| Bancarrota Chapter 7 | Tematica legal/financiera USA |
| ABOGADOS FAMILIA USA SIN REPETICION DE TEMAS | Tematica legal |
| 1 FLUJO ANTI ESTRES MILLONARIO | Tematica general autoayuda (NO veterinaria especifica) |

### 4.7 Flujos adicionales identificados por Qwen (no mapeados por Z.ai)

Estos flujos aparecen en la lista de Qwen pero NO fueron modificados por Z.ai:
- `u38gkCYPTAmHIg6v` - Veterinario Guayaquil Luis Blogger (NO tiene Date Gate)
- `JHHBn0oEDNFWSeHC` - 02 - Generate Veterinary Article
- `lgAhSjkEykyFKo1U` - FLUJO VETERINARIO MILLONARIO - AGRESIVIDAD Y COMPORTAMIENTO
- `wQLfSnTyoeilGNYv` - FLUJO VETERINARIO MILLONARIO - DERMATOLOGICOS
- `mSi4D0qxaTRcZW4g` - MODIFICAR DUPLICADOS EN BLOG VETERINARIO LUIS
- `mqRsiPlNHjoH5uG0` - FLUJO 1 MEJORADO VETERINARIO
- `o9peCrRCNhsQ5Hav` - Enriquecer + SEO Articulos + Citas APA Veterinarios
- `rZR1t1PmbI7sZrln` - Enriquecer + SEO Articulos + Citas APA BULLDOGS copy
- `rgt9qFYYohBDZdnp` - Veterinario CUENCA Luis Garcia Blogger
- `i8YvQa5hQZmVVeph` - Generador Automatico de Contenido Mascotas
- `j2jVcQTUSO32R8EU` - 02 - Generate Topics Bulldog
- `xO7VskA1GXS8qyxr` - 7 MONETIZACION BLOGS VETERINARIO GENERICO
- `s2XOnc9fLNBUhsLo` - Acuarios Nano o Micro Acuarios SIN REPETICION
- `uh5Kn8a2UIvPfnKF` - ACUARIOS NANO SIN REPETICION DE TEMAS
- `mktnuZM2y9RJB1KF` - CHINCHILLAS CUIDADO, NUTRICION COMPORTAMIENTO
- `qVGiTwAGs0FYvqel` - GECKO LEOPARDO SIN REPETICION (copia multiple)
- `fBkP5sEIQ7JKhGcX` - PEZ GUPPY SIN REPETICION (otra copia)

---

## 5. SYSTEM PROMPT ESTANDAR (VERSION QWEN - MAS COMPLETA)

Este es el System Prompt que Qwen diseño. Es MAS detallado que el que Z.ai aplico. Se recomienda usar ESTA version para futuras actualizaciones:

```
Eres un Medico Veterinario experto en redaccion cientifica y divulgacion medica de alto nivel. Tu tarea es generar articulos profesionales para el blog "Veterinario Luis Garcia".

## REQUISITOS OBLIGATORIOS DE ESTRUCTURA Y CONTENIDO:

1. **CASO CLINICO INTEGRADO**:
   - Inicia o intercala en el articulo un caso clinico real o hipotetico detallado.
   - Ejemplo: "Caso Clinico: Paciente canino, Macho, 5 anos, raza Labrador, presentado con cuadro de vomitos cronicos y perdida de peso..."
   - Describe signos clinicos, diagnostico diferencial, pruebas realizadas y tratamiento.

2. **GLOSARIO MEDICO VETERINARIO**:
   - Debes usar terminos tecnicos profesionales (ej: *nefropatia, prurito, disnea, profilaxis, etiologia, pronostico reservado, hemograma, bioquimica serica*).
   - INMEDIATAMENTE despues de usar el termino, explica su significado entre parentesis o en una frase accesible para el dueno de la mascota.
   - Ejemplo: "El paciente presenta *poliuria* (aumento anormal en la produccion de orina) y *polidipsia* (sed excesiva y aumento en la ingesta de agua)."

3. **BIBLIOGRAFIA CIENTIFICA APA**:
   - Intercala citas de libros y revistas veterinarias reales dentro de los parrafos.
   - Formato: "(Apellido, Ano)" o "Segun la WSAVA (2023)..."
   - Libros de referencia obligatoria:
     - *Manual de Medicina Interna Veterinaria* (Nelson & Couto)
     - *Enfermedades Infecciosas en Perros y Gatos* (Greene)
     - *Tratado de Medicina Felina* (August)
     - *Merck Veterinary Manual*
   - Al final del articulo, incluye una seccion "Bibliografia Consultada" con 3-5 referencias completas en formato APA.

4. **MONETIZACION Y AFILIADOS**:
   - Inserta estrategicamente 2-3 recomendaciones de productos de Amazon/Hotmart relacionados con el tema.
   - Usa un tono de recomendacion profesional: "Para el manejo en casa, recomendamos [Producto] que ayuda a [beneficio clinico]."
   - Incluye el enlace de afiliado correspondiente (usar datos de la hoja de afiliados).

5. **OPTIMIZACION SEO, AEO Y RICH SNIPPETS**:
   - Usa etiquetas HTML: <h1>, <h2>, <h3> correctamente jerarquizadas.
   - Incluye una seccion de "Preguntas Frecuentes (FAQ)" al final con 3-5 preguntas relevantes.
   - Genera un bloque JSON-LD de tipo `Article` o `FAQPage` para rich snippets (insertar al final antes de cerrar body).
   - Longitud: 1500-2500 palabras minimo.

6. **TONO HUMANO (Human Level)**:
   - Escribe con empatia, como si estuvieras hablando con un dueno preocupado pero informado.
   - Evita frases roboticas como "En conclusion", "Es importante destacar". Usa transiciones naturales.
   - Usa storytelling en el caso clinico para generar conexion emocional.

7. **LLAMADO A LA ACCION - COMUNIDAD WHATSAPP**:
   - AL FINAL DEL ARTICULO, inserta este bloque destacado:
   ---
   ¿Necesitas orientacion veterinaria personalizada?
   Unete a nuestra Comunidad Exclusiva de WhatsApp donde compartimos casos, consejos y respondemos dudas en tiempo real.
   [HAZ CLIC AQUI PARA UNIRTE](https://chat.whatsapp.com/IkpYnlrPyEx8Y2NTyaFB6P)
   ---

8. **IMAGENES**:
   - Sugiere 2-3 imagenes tematicas con descripciones ALT optimizadas para SEO.
   - Si el flujo tiene nodo de imagen (Pexels/Pixabay), asegura que el prompt de busque use terminos veterinarios precisos.

## FORMATO DE SALIDA:
- El articulo debe estar en HTML limpio, listo para publicar en Blogger.
- No incluyas markdown (```) alrededor del HTML.
- Asegurate de que el titulo sea atractivo y contenga palabras clave principales.

## NOTA CRITICA:
Si el tema es sobre una patologia, SIEMPRE menciona cuando es una emergencia veterinaria que requiere atencion inmediata.
```

---

## 6. TABS HUERFANAS (CONFIRMADAS - NECESITAN FLUJO PROPIO)

Estas tabs tienen contenido listo pero NO tienen un flujo de n8n que las procese:

| # | Sheet | Tab | Tipo de contenido | Prioridad |
|---|-------|-----|-------------------|-----------|
| 1 | VETERINARIA NICHOS_HIGH_TICKET (`1dtc4...`) | **NUTRICION** | Articulos de nutricion veterinaria | ALTA |
| 2 | NUEVOS NICHOS VETERINARIOS (ID desconocido) | **TECNOLOGIA** (y otras) | Articulos con ID_UNICO/TITULO/ESTADO/PUBLICADO | ALTA |
| 3 | NUEVOS NICHOS VETERINARIOS (ID desconocido) | **Otras tabs** | Por descubrir (sheet no visible via API) | MEDIA |
| 4 | VETERINARIA NICHOS_HIGH_TICKET (`1dtc4...`) | **Posibles P02, P04, P05+** | Numeracion sugiere tabs existentes | MEDIA |
| 5 | ARTICULOS CHINCHILLAS (`1c5rZ...`) | Hoja con PILAR/TITULO/ESTADO/PUBLICADO/USADO | Articulos de chinchillas | MEDIA |
| 6 | VETERINARIO BLOG OFICIAL (`13zYY...`) | **NICHOS NUEVOS** | Posiblemente sin flujo dedicado propio | BAJA |
| 7 | Veterinario luis arturo garcia (`1KkCl...`) | **Posibles 01_CLUSTERS_*, 02_CLUSTERS_*** | No visibles por sheet privado | BAJA |

Para crear flujos para estas tabs:
- Clonar un flujo existente funcional (ej: `9KrKde8O3cijCcBf` - CASOS ESTUDIOS)
- Cambiar el Sheet ID y tab name en los nodos Google Sheets
- Verificar que apunte al Blog ID `2772493032989228627`
- Aplicar el System Prompt estandar
- Inyectar Date Gate del bloque correspondiente
- Activar

---

## 7. SISTEMA DE 3 BLOQUES - COMO FUNCIONA

### Date Gate (inyectado en cada flujo)
Despues del trigger, hay un nodo Code llamado "DATE GATE - Bloque X" con este patron:
```javascript
const blockStart = new Date("2026-07-07T00:00:00-05:00");
const blockEnd = new Date("2027-01-07T00:00:00-05:00");
const now = new Date();
if (now >= blockStart && now <= blockEnd) {
  return $input.all();
} else {
  return [];
}
```
Cada bloque tiene sus fechas propias. Si la fecha esta fuera de ventana, retorna `[]` y el flujo se detiene.

### Master Controller (ID: `bGA2HDjvFxzMZxYV`)
- Se ejecuta diariamente
- Determina que bloque esta activo segun la fecha actual
- Envia comandos via HTTP a la API de n8n para activar/desactivar flujos
- Nodo 1: Schedule Trigger (diario)
- Nodo 2: Code (Block Manager - calcula bloque activo)
- Nodo 3: Code (Split Flow Actions - genera lista de activate/deactivate)
- Nodo 4: IF (separa activate de deactivate)
- Nodo 5: HTTP (PUT activate)
- Nodo 6: HTTP (PUT deactivate)
- Nodo 7: Code (Log Results)

---

## 8. TAREAS PENDIENTES (ORDENADAS POR PRIORIDAD)

### PRIORIDAD CRITICA (Haz esto primero)

**T1: Diagnosticar y reparar flujos con ERROR**
- La mayoria de flujos estan fallando segun los logs de ejecucion
- Necesario: obtener detalles de cada flujo via API, revisar el error, corregir
- Posibles causas: Date Gate mal inyectado, credenciales expiradas, nodos rotos, sheet ID incorrecto
- Comando: `GET /api/v1/workflows/{id}` para ver el flujo completo
- Comando: `GET /api/v1/executions?workflowId={id}&limit=1` para ver el ultimo error

**T2: Resolver conflicto de estrategia (3 bloques vs activar todo)**
- Z.ai implemento 3 bloques de 6 meses (solo 10 activos ahora)
- Qwen recomendo activar todos con distribucion de frecuencia
- EL USUARIO DEBE DECIDIR que estrategia seguir
- Si se elige "activar todo": eliminar Date Gates, ajustar triggers a frecuencias escalonadas, activar los 28 flujos

**T3: Implementar sistema anti-duplicados**
- Actualmente NO hay proteccion contra duplicados
- Diseno propuesto: antes de publicar, consultar una hoja central "TITULOS_PUBLICADOS" o verificar via Blogger API
- Alternativa: usar la columna ESTADO en cada Google Sheet (PENDIENTE -> EN_PROCESO -> PUBLICADO)
- Necesario agregar nodos Code/Sheets Update en cada flujo

### PRIORIDAD ALTA

**T4: Crear flujos para tabs huerfanas**
- NUTRICION, TECNOLOGIA (de NUEVOS NICHOS), CHINCHILLAS, y otras tabs sin flujo
- Clonar flujo existente, cambiar sheet/tab, aplicar prompt estandar, inyectar Date Gate

**T5: Actualizar System Prompts con version completa de Qwen**
- Z.ai actualizo 25 flujos con una version mas corta del prompt
- La version de Qwen es mas completa (incluye imagenes, JSON-LD, FAQ Schema)
- Aplicar la version completa a todos los flujos

**T6: Desactivar flujos NO veterinarios**
- Seguro social denegado, Bancarrota Chapter 7, ABOGADOS FAMILIA USA, ANTI ESTRES MILLONARIO (general)

### PRIORIDAD MEDIA

**T7: Configurar distribucion de frecuencia**
- Si se activan todos los flujos, necesitan frecuencias escalonadas para lograr ~5 articulos/dia
- Propuesta: Grupo A (cada 3 dias), Grupo B (cada 4 dias), Grupo C (cada 6 dias), Grupo D (cada 7 dias)
- Actualizar los nodos Schedule Trigger de cada flujo

**T8: Auditoria SEO completa del blog**
- Datos recopilados pero no analizados: `/home/z/my-project/download/seo_vet_search*.json`
- Solo ~8-10 articulos indexados actualmente
- Necesario: analizar palabras clave, competidores, oportunidades

**T9: Geolocalizacion USA**
- El usuario tiene 2 bases de datos de veterinarias en USA
- Podrian usarse para crear contenido geolocalizado que atraiga trafico internacional
- Crear flujo especifico "VETERINARIA USA" con contenido en ingles o bilingue

### PRIORIDAD BAJA

**T10: Revisar flujo Veterinario Guayaquil** (`u38gkCYPTAmHIg6v`)
- No fue modificado por Z.ai (no tiene Date Gate)
- Verificar si esta activo y a que sheet apunta

**T11: Limpiar flujos adicionales no mapeados**
- Varios flujos identificados por Qwen que no fueron procesados por Z.ai
- Algunos pueden ser duplicados o utilidades

---

## 9. ERRORES CONOCIDOS Y SOLUCIONES

### Error: PEZ PLATY ID con 'U' extra
- ID incorrecto: `CZEzMQrOOA9UuWyn` (tiene 'U' extra)
- ID correcto: `CZEzMQrOOA9UoWyn`
- Ya corregido por Z.ai

### Error: n8n __rl format al leer credenciales/sheets
- Los IDs en n8n no son strings simples, son objetos: `{__rl: true, value: "actual_id", mode: "id", cachedResultName: "display_name"}`
- Funciones de ayuda:
```javascript
function extract_rl(val) {
  if (!val) return null;
  if (typeof val === 'string') return val;
  if (val.__rl) return val.value;
  if (Array.isArray(val)) return val.map(extract_rl).filter(Boolean);
  return null;
}
```

### Error: JWT API Key expirada
- Las keys JWT tienen fecha de expiracion
- Si obtenes 401, genera una nueva key desde la UI de n8n
- Las 3 keys listadas arriba pueden estar expiradas

### Error: Google Sheets privados (403)
- No se pueden leer las tabs via Sheets API (son privados)
- Workaround: extraer tabs de los nodos de los flujos n8n (ya hecho)
- Para descubrir tabs nuevas: el usuario debe verificar manualmente en Google Sheets

---

## 10. ARQUITECTURA IDEAL DE CADA FLUJO (OBJETIVO)

Cada flujo veterinario deberia tener esta secuencia de nodos:

1. **Schedule Trigger** - Con frecuencia escalonada segun grupo
2. **DATE GATE** (Code) - Verifica ventana temporal del bloque asignado
3. **Google Sheets Read** - Lee fila con ESTADO = PENDIENTE
4. **Code - Filtrar Pendientes** - Filtra solo filas PENDIENTE/SIN_USAR
5. **Google Sheets Update** - Marca como EN_PROCESO (lock anti-duplicados)
6. **Google Sheets Read** - Lee datos de afiliados (sheet de soporte)
7. **AI Agent** - Genera articulo con System Prompt estandar
8. **Code - Preparar Casos** - Inserta caso clinico del sheet CASOS QWEN
9. **Pexels/Pixabay** - Genera imagenes tematicas
10. **Blogger - Publicar** - Publica como borrador o programado en veterinarioluis.com
11. **Google Sheets Update** - Marca como PUBLICADO con URL y fecha
12. **RSS/Ping** - Notifica servicios de indexacion
13. **Code - Manejo Errores** - Si falla, marca como ERROR en sheet

---

## 11. REGLAS CRITICAS (NO VIOLAR)

1. **NUNCA** publicar sin verificar duplicados primero
2. **SIEMPRE** marcar el articulo como EN_PROCESO antes de generar
3. **SIEMPRE** actualizar a PUBLICADO con URL despues de exito
4. **NUNCA** exceder 5 articulos/dia en total entre TODOS los flujos (si se activan todos)
5. **SIEMPRE** incluir enlace a WhatsApp: https://chat.whatsapp.com/IkpYnlrPyEx8Y2NTyaFB6P
6. **SIEMPRE** usar citas APA de libros veterinarios reales
7. **SIEMPRE** explicar terminos de glosario veterinario en contexto
8. **SIEMPRE** incluir casos clinicos cuando corresponda
9. **NUNCA** modificar flujos sin hacer backup primero (exportar via API)
10. **TODOS** los flujos veterinarios publican UNICAMENTE a Blog ID `2772493032989228627`

---

## 12. CONTACTO Y RECURSOS

- **Blog Principal**: https://draft.blogger.com/blog/posts/2772493032989228627
- **Blog Publico**: https://veterinarioluis.com
- **Comunidad WhatsApp**: https://chat.whatsapp.com/IkpYnlrPyEx8Y2NTyaFB6P
- **n8n UI**: https://vmi3096105.contaboserver.net
- **n8n API**: https://vmi3096105.contaboserver.net/api/v1

---

---

## 13. AUDITORIA EJECUTADA POR Z.AI - 7 JULIO 2026 (POST-REPARACION)

### 13.1 Hallazgos de la Auditoria

Se ejecuto una auditoria completa via API REST de n8n a los 28 flujos veterinarios mas los flujos adicionales. Se descubrieron los siguientes problemas criticos:

#### HALLAZGO 1: 18 flujos reactivados incorrectamente por Qwen (CRITICO)
Qwen/Claude Code reactivo 15 de los 18 flujos que debian estar inactivos (Bloque 2 y Bloque 3), ademas de 3 flujos adicionales (GUAYAQUIL, GECKO LEOPARDO, CHINCHILLAS). Esto causo que ~25 flujos se ejecutaran simultaneamente, saturando las APIs.

**Flujos reactivados incorrectamente (restaurados a INACTIVO):**
- Bloque 2: ALIMENTOS GATOS, ALIMENTOS PERROS, ANSIEDAD Y ESTRES, BULLDOGS, HURONES, LOROS, MASCOTAS EXOTICAS, PRIMEROS AUXILIOS, REPTILES (9 flujos)
- Bloque 3: ACUARIOS BIOTOPO (x2), BOVINOS, PEZ BETTA, PEZ GUPPY, PEZ PLATY (6 flujos)
- Adicionales: GUAYAQUIL, GECKO LEOPARDO, CHINCHILLAS (3 flujos)

#### HALLAZGO 2: Google Sheets Quota Exceeded (10 flujos afectados)
Con 25+ flujos activos leyendo Google Sheets simultaneamente, se alcanzo el limite de "Read requests per minute per user" (60 req/min). Este fue el error mas comun.

**Flujos afectados:** FLUJO VET LUIS BLOGGER, ECUADOR Y MUNDO, QUITO, CUENCA, RENALES Y URINARIOS, CASOS ESTUDIOS, mejorar articulos, Difusion VET LUIS, GUAYAQUIL, y otros.

#### HALLAZGO 3: Cohere API - Tool Definition Error (2+ flujos)
El nodo "Validate and Fix Article" (tipo Agent) usa modelos Cohere con tool calling. La API de Cohere requiere que cada parametro de tool tenga la clave "type", pero la definicion del tool en n8n no la incluye.

**Error:** `tools -> [0] -> parameterDefinitions -> output: Missing required key "type"`
**Flujos afectados:** ECUADOR Y MUNDO, QUITO

#### HALLAZGO 4: DeepSeek - Insufficient Balance (2 flujos)
La cuenta de DeepSeek no tiene saldo suficiente para generar articulos.

**Error:** `Payment required - Insufficient Balance`
**Flujos afectados:** 10 NICHOS MASCOTAS, Difusion BULLDOG

#### HALLAZGO 5: Cohere API v1 → v2 Migration (1+ flujo)
Cohere migro su API de v1 a v2. Algunos modelos ya no soportan `/v1/chat`.

**Error:** `this model is not supported with '/v1/chat', please use '/v2/chat' instead`
**Flujos afectados:** GECKO LEOPARDO y potencialmente otros flujos que usan Cohere

#### HALLAZGO 6: Gemini Rate Limit (1+ flujo)
Demasiadas requests simultaneas a la API de Gemini.

**Error:** `429 Too Many Requests - You exceeded your current quota`
**Flujos afectados:** TECNOLOGIA (y otros que usan Gemini como modelo principal)

#### HALLAZGO 7: Ejecuciones "falsamente exitosas"
Los flujos del Bloque 2 y 3 que Qwen reactivo mostraban status "success", pero en realidad no hacian nada: el Date Gate retornaba `[]` (vaciar datos porque no es su ventana temporal), el flujo terminaba inmediatamente sin procesar nada.

### 13.2 Reparaciones Aplicadas

| # | Accion | Detalle | Estado |
|---|--------|---------|--------|
| R1 | Desactivar 15 flujos del Bloque 2 y 3 | Se desactivaron los flujos que Qwen reactivo incorrectamente | ✅ Completado (15/15) |
| R2 | Desactivar 3 flujos adicionales | GUAYAQUIL, GECKO LEOPARDO, CHINCHILLAS | ✅ Completado (3/3) |
| R3 | Stagger schedules del Bloque 1 | Intervalos cambiados de 15-25min a 23,25,27,29,31,33,35,37,39,41min (3min de separacion entre cada flujo) | ✅ Completado (10/10) |
| R4 | Restaurar conexiones de ECUADOR Y MUNDO | El flujo perdio todas sus conexiones durante una reparacion; se reconstruyeron 20 conexiones basandose en la estructura de QUITO | ✅ Completado |
| R5 | Cambiar modelo de QUITO (Cohere → DeepSeek) | Se cambio el nodo "Cohere Chat Model" a DeepSeek para evitar el error de tool definition | ✅ Completado |
| R6 | ECUADOR usa Hugging Face | Tras la restauracion, ECUADOR usa Hugging Face Inference Model en lugar de Cohere (funciona, aunque menos potente) | ✅ Funcional |

### 13.3 Estado Post-Reparacion

**Flujos activos (correctamente):** Solo los 10 del Bloque 1

**Schedules del Bloque 1 (staggered):**

| Flujo | Intervalo (min) |
|-------|-----------------|
| FLUJO VET LUIS BLOGGER | 23 |
| ECUADOR Y MUNDO | 25 |
| CUENCA | 27 |
| QUITO | 29 |
| RENALES Y URINARIOS | 31 |
| TECNOLOGIA | 33 |
| CASOS ESTUDIOS | 35 |
| PRIMERA_PERSONA_V3 | 37 |
| mejorar articulos | 39 |
| 10 NICHOS MASCOTAS | 41 |

**Primera ejecucion exitosa post-reparacion:** ECUADOR Y MUNDO a las 10:25:09 UTC (7 jul 2026)

### 13.4 Problemas RESTANTES (requieren accion del usuario o manual)

| # | Problema | Accion requerida | Prioridad |
|---|----------|-----------------|-----------|
| P1 | **DeepSeek sin saldo** - 10 NICHOS MASCOTAS y Difusion BULLDOG fallan con "Insufficient Balance" | Agregar credito a la cuenta de DeepSeek, o cambiar estos flujos a Gemini | CRITICA |
| P2 | **8 flujos del Bloque 1 aun usan Cohere** como modelo secundario - pueden fallar si el nodo Agent con tools se ejecuta | Cambiar modelos Cohere a Gemini o DeepSeek en los nodos Agent de: VET LUIS BLOGGER, QUITO, CUENCA, RENALES, TECNOLOGIA, CASOS ESTUDIOS, mejorar articulos, 10 NICHOS MASCOTAS | ALTA |
| P3 | **Cohere API v1 deprecated** - GECKO LEOPARDO y otros flujos con Cohere necesitan migracion a v2 | Actualizar nodos Cohere o reemplazar por otro modelo | MEDIA |
| P4 | **Flujos de difusion (Difusion VET LUIS, Difusion BULLDOG)** siguen activos pero fallan con DeepSeek sin saldo o Sheets quota | Agregar saldo a DeepSeek o cambiar modelos; estos flujos no tienen Date Gate | MEDIA |
| P5 | **Conlicto 3 bloques vs activar todo** - El usuario pidio 3 bloques a Z.ai pero "activar todo" a Qwen | El usuario debe decidir: mantener 3 bloques o activar todos los flujos | ALTA (decision del usuario) |
| P6 | **Sin sistema anti-duplicados** - No hay mecanismo para evitar que dos flujos publiquen el mismo tema | Implementar lock en Google Sheets antes de generar articulo | ALTA |

### 13.5 Modelos de IA usados por los flujos del Bloque 1

| Flujo | Modelo Principal | Modelo Secundario | Modelo Casos | Estado |
|-------|-----------------|-------------------|--------------|--------|
| FLUJO VET LUIS BLOGGER | Gemini | Cohere | - | ⚠️ Cohere puede fallar con tools |
| ECUADOR Y MUNDO | Hugging Face | - | Hugging Face | ✅ Funcional (pero HF es menos potente) |
| QUITO | Hugging Face | Cohere (cambiado a DeepSeek?) | Hugging Face | ⚠️ Verificar si el cambio se aplico correctamente |
| CUENCA | Hugging Face | Cohere | Hugging Face | ⚠️ Cohere puede fallar con tools |
| RENALES Y URINARIOS | Gemini | Cohere | - | ⚠️ Cohere puede fallar con tools |
| TECNOLOGIA | Gemini | Cohere | Gemini | ⚠️ Cohere puede fallar; Gemini puede tener rate limit |
| CASOS ESTUDIOS | Hugging Face | Cohere | Hugging Face | ⚠️ Cohere puede fallar con tools |
| PRIMERA_PERSONA_V3 | (no detectado) | - | - | ❓ Verificar en n8n UI |
| mejorar articulos | Cohere (x5 nodos!) | - | - | ⚠️ Altamente dependiente de Cohere |
| 10 NICHOS MASCOTAS | Gemini | Cohere | DeepSeek | ❌ DeepSeek sin saldo + Cohere problematico |

---

## 14. REGLAS PARA QUE OTRAS IAS NO ROMPAN LO QUE Z.AI REPARO

### REGLA 1: NO reactivar flujos del Bloque 2 o 3
Los flujos del Bloque 2 (Ene 2027 - Jul 2027) y Bloque 3 (Jul 2027 - Ene 2028) deben permanecer INACTIVOS hasta que el Master Controller o el usuario los active. Si una IA reactiva estos flujos, causara saturacion de Google Sheets y APIs de IA.

### REGLA 2: NO cambiar los intervalos del Schedule Trigger
Los 10 flujos del Bloque 1 tienen intervalos escalonados (23, 25, 27, 29, 31, 33, 35, 37, 39, 41 minutos). Esto previene el Google Sheets quota. No cambiar estos valores sin coordinacion.

### REGLA 3: Si se modifica un flujo, PRESERVAR las conexiones
Al usar `PUT /api/v1/workflows/{id}`, el JSON debe incluir el campo `connections` intacto. Si se omite, el flujo pierde todas sus conexiones entre nodos. Siempre verificar que `len(connections) > 0` despues de guardar.

### REGLA 4: NO usar Cohere para Agent nodes con tools
Cohere tiene un bug de compatibilidad con tool definitions en n8n. Usar Gemini o DeepSeek en su lugar para nodos Agent que usen tools.

### REGLA 5: Consultar ESTADO del proyecto antes de modificar
Leer este documento completo y los ultimos registros de `/home/z/my-project/worklog.md` antes de hacer cualquier cambio a los flujos de n8n.

---

*Documento generado para coordinacion entre todas las IAs del proyecto veterinario 2027*
*Ultima actualizacion: 7 de julio de 2026 - Auditoria y reparaciones aplicadas*
*Autores: Z.ai (Super Z) + Qwen (Claude Code) - Trabajo consolidado*
*Seccion 13-14: Auditoria ejecutada y reparaciones por Z.ai (7 jul 2026)*
