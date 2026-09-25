# Montar Tasker en Kiro CLI (Opción A: los dos MCP juntos)

Estos archivos son ejemplos para registrar **ambos** servidores MCP a la vez en Kiro
CLI (patrón `mcp_tools/*.json` + `mcp-build` + wrapper `--env-file`, el mismo que usas
para rclone / nextdns / n8n). Así el LLM tiene:

- **`tasker-mcp`** (este repo, Python) → diseñar/generar/validar XML (offline).
- **`tasker-live`** (dceluis, Go) → ejecutar tareas en vivo en el teléfono.

> Alternativa: la **Opción B** ya viene integrada en este repo (tool `run_tasker_task`),
> así que con SOLO `tasker-mcp` + las env vars `TASKER_HOST`/`TASKER_API_KEY` ya diseñas
> **y** ejecutas con un único server. Usa esta Opción A solo si prefieres el binario Go
> de dceluis para la ejecución. Ver `../../docs/integracion-dceluis.md`.

## ⚠️ Importante

- **Kiro Web no puede ejecutar** (sin ruta a la LAN/teléfono). Esto es para **Kiro CLI
  en el NAS** o donde tengas ruta al teléfono.
- La parte **live** necesita: Tasker con su server HTTP activo (puerto 1821), el binario
  Go de dceluis alcanzable, y la API key `tk_...` (tarea `MCP generate_api_key`).
- Sustituye los placeholders en MAYÚSCULAS. **No** hardcodees secretos en el JSON:
  van en un `.env` que el wrapper inyecta con `--env-file`.

## Archivos

- `mcp_tools/tasker-mcp.json` — este repo (Python). Ejecución en vivo opt-in por env.
- `mcp_tools/tasker-live.json` — binario Go de dceluis (solo si eliges Opción A pura).
- `tasker.env.example` — plantilla de secretos (copiar a `$dkco/kiro-cli/tasker.env`, chmod 600).

## Pasos (resumen)

1. Copia cada `mcp_tools/*.json` a tu carpeta `settings/mcp_tools/` de Kiro CLI.
2. Copia `tasker.env.example` a `$dkco/kiro-cli/tasker.env`, rellena valores, `chmod 600`.
3. Regenera el `mcp.json` con `mcp-build` (debe listar tus MCP + estos).
4. Asegúrate de que el wrapper `kiro` inyecta `--env-file /docker/kiro-cli/tasker.env`.
5. Clasifica permisos en `permissions.yaml` (V3): las `search_*`/`generate_*`/`validate_*`
   → `allow` (solo lectura/generación); `run_tasker_task` y las `tasker_*` de dceluis
   → `ask` (actúan en el teléfono real).
