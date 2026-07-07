# Credenciales del Proyecto Veterinario

## n8n API
- URL: https://vmi3096105.contaboserver.net/api/v1
- API Key Permanente: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmOGM1MTJmNy1mNTVhLTQwYjYtYWU1Ni00MDM0OWNlMDlmMjkiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYjAxODVjY2MtYWNlOC00M2YxLTg5N2ItNzEyMzYwMTdlY2ZmIiwiaWF0IjoxNzgzNDIxMTQ5fQ.S2Sz6qqZC0eeuSsyMHhSTY_dMykP7GBh1JAv-Ozx2sI
- Header: X-N8N-API-KEY

## Blogger
- Blog ID: 2772493032989228627
- URL: veterinarioluis.com

## Credenciales IA en n8n (Credential IDs para nodos)
- DeepSeek: tNIbvUHUgCDukRly
- Gemini: wQOnKlUsbUnFFzD1
- Cohere: 6LmusRbYdpPXTD10 (NO USAR en Agent nodes con tools)
- Google Sheets: UviJg5pB7TsCtYBk
- Agnes AI: M2BdhhUp0ZryKpmq

## n8n __rl format
Los IDs en n8n usan: {__rl: true, value: "actual_id", mode: "id", cachedResultName: "display_name"}

## clean_for_update() - REQUERIDA para PUT /workflows/{id}
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
