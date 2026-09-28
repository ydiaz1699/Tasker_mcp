# Montar Tasker_mcp en Kiro IDE (Windows)

Kiro IDE corre en **tu PC**, así que (a diferencia de Kiro Web, que es un sandbox en
la nube sin ruta a tu LAN) puede lanzar este MCP **localmente** y —si el teléfono con
Tasker está en la misma red— también **ejecutar en vivo** (`run_tasker_task`).

Con esto tienes el flujo completo en un solo sitio: **diseñar/validar XML (offline) +
ejecutar en el teléfono (en vivo)**.

## 1. Instalar el paquete

Clona el repo y, en su carpeta, instala en un entorno de Python (recomendado un venv):

```powershell
git clone https://github.com/ydiaz1699/Tasker_mcp.git
cd Tasker_mcp
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

> Requisitos: Python >= 3.11. Comprueba con `python --version`. Si `python` no existe,
> prueba `py --version` (el lanzador de Windows) y usa `py` en su lugar.

## 2. Configurar el MCP en Kiro IDE

Kiro IDE lee la configuración MCP de un `mcp.json`:

- **Por workspace:** `.kiro/settings/mcp.json` dentro del proyecto abierto.
- **Global (todos los workspaces):** el `mcp.json` de usuario de Kiro.

Copia `mcp.json` de esta carpeta y **ajusta**:

- `command`: lo más robusto en Windows es la **ruta absoluta al python del venv**
  (evita depender del PATH que ve Kiro). Ejemplo:
  `C:\\Users\\TU_USUARIO\\...\\Tasker_mcp\\.venv\\Scripts\\python.exe`.
  Si instalaste en el Python global y está en el PATH, puede bastar `"python"` o `"py"`.
- `TASKER_HOST`: la IP del teléfono que corre Tasker (en tu WiFi). **CAMBIAR.**
- `TASKER_API_KEY`: la API key `tk_...` que genera la tarea `MCP generate_api_key`
  en el teléfono (ver la sección de dceluis en `../../docs/integracion-dceluis.md`). **CAMBIAR.**

> Las barras en las rutas JSON van **escapadas** (`\\`) o usa `/` (Windows lo acepta).

## 3. Verificar

Reinicia/recarga los servidores MCP en Kiro IDE. Deberías ver el server `tasker-mcp`
con **14 tools**:

- **Diseñar (offline, no tocan el teléfono):** `search_tasker_actions`, `search_tasker_events`,
  `search_tasker_states`, `search_tasker_variables`, `generate_task_xml`,
  `generate_profile_xml`, `generate_project_xml`, `generate_quick_automation`,
  `validate_tasker_xml`, `get_action_info`, `list_action_categories`,
  `list_common_patterns`, `get_pattern_details`.
- **Ejecutar en vivo (necesita el teléfono en la LAN):** `run_tasker_task`.

Prueba rápida sin teléfono: pídele *"busca la acción de WiFi en Tasker"* → usa el índice
FTS5 y devuelve códigos reales. Con teléfono: *"lanza la tarea MCP Flash Text"*.

## Notas

- **La ejecución en vivo solo funciona si el teléfono está en la misma red que el PC.**
  Si está en otra VLAN / red de invitados, no habrá ruta a `TASKER_HOST`.
- La generación de XML **siempre** funciona (offline), con o sin teléfono.
- Si no configuras `TASKER_HOST`/`TASKER_API_KEY`, las 13 tools de diseño funcionan
  igual; solo `run_tasker_task` avisará de que está deshabilitada.
- El índice de búsqueda (`tasker_index.db`) se **auto-construye** en el primer arranque
  desde la fuente vendorizada; no hay que hacer nada. Para regenerarlo tras un update de
  Tasker: `python -m tasker_mcp.indexer.build_db --refresh`.
