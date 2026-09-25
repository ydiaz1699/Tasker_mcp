# Integración con `dceluis/tasker-mcp`: diseñar → ejecutar

Este documento explica cómo **este repo (Tasker_mcp, Python)** y el MCP externo
[`dceluis/tasker-mcp`](https://github.com/dceluis/tasker-mcp) (Go) se complementan,
y —lo más importante— **cómo el LLM genera automatizaciones de Tasker sin equivocarse**.

> Adoptamos el mecanismo de `n8n-mcp` (SOURCE → LOADER → PARSER → DB SQLite/FTS5 →
> tools de búsqueda) porque Tasker, al no tener nodos visuales, necesita un índice
> consultable de acciones/eventos/estados para que el LLM no invente códigos. Este
> documento describe ese índice, la validación que lo respalda, y cómo enchufar la
> ejecución en vivo por encima.

---

## 1. Los dos MCP no compiten: se reparten el problema

| | **Tasker_mcp (este repo, Python)** | **dceluis/tasker-mcp (Go)** |
|---|---|---|
| Rol | **El cerebro** — diseña y genera | **Las manos** — ejecuta en vivo |
| Qué produce | XML válido (`.tsk/.prf/.prj.xml`) offline | Dispara tareas ya existentes en el teléfono |
| Cómo | Knowledge base + motor XML + validador | `POST /run_task` al server HTTP de Tasker (`:1821`) |
| Sabe de Tasker | Sí (373 acciones, 82 eventos, 50 estados, 99 vars) | No — solo ejecuta lo que le declares |
| Necesita el móvil | No (genera archivos) | Sí (Tasker corriendo y en red) |
| Valida | **Sí** (`validate_tasker_xml`) | No |

**Flujo combinado:**

```
Usuario: "apaga el wifi cuando la bateria baje del 20%"
   │
   ▼
[Tasker_mcp]  busca estado Battery Level (code real) + accion WiFi (425),
              genera .prf.xml, lo VALIDA  ──▶  usuario lo importa en Tasker
   │
   ▼
[dceluis/tasker-mcp]  (opcional) dispara la tarea en vivo para probarla:
                      POST /run_task  ──▶  el telefono actua
```

El repo externo no conoce Tasker; solo ejecuta. Este repo garantiza que lo que se
genera es correcto. Por eso encajan.

---

## 2. Cómo Tasker "conecta" acciones y por qué el LLM NO se inventa nada

### 2.1. Qué es un "nodo" en Tasker

Tasker no tiene nodos visuales (como n8n). Su unidad es la **acción**, identificada
por un **código numérico**:

- `548` = Flash · `425` = WiFi · `41` = Send SMS · `559` = Say · `61` = Vibrate …

Estructura de los archivos:

- **`.tsk.xml`** = una `Task`: lista ordenada de `Action` (cada una con su `<code>`).
- **`.prf.xml`** = un `Profile`: un **contexto disparador** (evento / estado / tiempo /
  app) + tarea de entrada (y opcional de salida).
- **`.prj.xml`** = un `Project`: varios perfiles + tareas juntos.

El riesgo real: si el LLM **inventa un código, un argumento o un valor**, Tasker
rechaza el import o hace algo inesperado. Aquí están las capas que lo evitan.

### 2.2. Capa 1 — Índice consultable (patrón n8n-mcp), no memoria

Igual que n8n-mcp indexa sus ~525 nodos para que el LLM los conozca, este repo indexa
las acciones/eventos/estados de Tasker. Pipeline: **SOURCE → LOADER → PARSER → DB
(SQLite + FTS5) → tools de búsqueda** (`src/tasker_mcp/indexer/`).

- **SOURCE autoritativa:** [Taskomater/Tasker-XML-Info](https://github.com/Taskomater/Tasker-XML-Info)
  → `code → name → kind` de 373 acciones, 82 eventos, 50 estados. Vendorizada en
  `indexer/data/Tasker_XML_Codes.md` (build offline) y re-descargable con `--refresh`.
- **ENRICHMENT:** `knowledge/*.py` añade descripciones, args y las 99 variables/patterns
  que la fuente no trae.
- **DB:** `build_db.py` fusiona ambos en `tasker_index.db` (SQLite + **FTS5**, ranking BM25).
- Las `search_tasker_*` consultan ese índice. Si falta la DB, **fallback** a la búsqueda
  en memoria; y el server la **auto-construye** en el primer arranque.

El LLM **consulta**, no adivina:

```
search_tasker_actions("wifi")   →   busca en el índice FTS5, devuelve los códigos
                                     reales rankeados por relevancia (BM25)
```

Ventaja del LOADER frente a mantener los datos a mano: la lista de códigos deja de
tipearse (antes había ~90 acciones a mano; ahora están las 373 de la fuente), y se
re-indexa con un comando cuando Tasker publique una versión nueva.

### 2.3. Capa 2 — Validación antes de entregar

`validate_tasker_xml(xml)` es la red de seguridad. Comprueba:

1. XML bien formado (parseable).
2. Raíz `TaskerData` con `sr=""` y atributo `tv` (versión).
3. **Cada `<code>` existe en los 373 conocidos** — si no, error `"Unknown action code: N"`.
4. Cada `Task` tiene `<id>`; cada `Profile` tiene `<mid0>` (tarea de entrada).

Es decir, aunque el LLM se colara con un código inventado, se detecta **antes** de
que el usuario importe el archivo al teléfono. Regla operativa: **generar → validar →
entregar**. Nunca entregar XML sin pasar por `validate_tasker_xml`.

### 2.4. Capa 3 — El "gem" anti-alucinación

`gem tasker/instrucciones.md` (+ los registros `.txt`) es un system prompt que:

- Prohíbe describir acciones/eventos/estados que no estén en los archivos.
- Obliga a usar nombres **verbatim** ("Variable Set", no "Set Variable").
- Prohíbe inventar argumentos, valores de dropdown o "dejar en blanco para X".
- Obliga a decir "no lo sé / pruébalo en la app" en vez de adivinar.

Es el activo diferencial de este repo frente al externo (que no tiene grounding).

### 2.5. Resumen para el LLM (checklist anti-error)

1. Nunca escribas un `<code>` de memoria → obténlo con `search_tasker_actions/events/states`.
2. Nunca inventes argumentos → usa los `args` que devuelve la búsqueda.
3. Genera con `generate_task_xml / generate_profile_xml / generate_project_xml`.
4. **Valida siempre** con `validate_tasker_xml` antes de dar el archivo al usuario.
5. Ante la duda, di que se verifique en la app; no rellenes huecos.

---

## 3. Cómo hacer que convivan (dos opciones)

### Opción A — Registrar los dos MCP a la vez (sin tocar código)

En el cliente (Kiro CLI en el NAS, Claude Desktop, etc.) se registran ambos servers.
El LLM ve las tools de los dos y elige: `search_/generate_/validate_*` (este repo)
para **diseñar**, y `tasker_*` (dceluis) para **ejecutar**. Ver
`examples/kiro-cli/` para los archivos `mcp_tools/*.json` de referencia.

Requisitos de la parte de ejecución (dceluis):
- Tasker con su server HTTP activo (puerto `1821` por defecto).
- El binario Go alcanzable (Termux en el móvil, o PC en la misma red).
- API key de Tasker (`tk_...`) generada por la tarea `MCP generate_api_key`.

### Opción B — Fusionar: ejecución en vivo dentro de este repo (recomendado)

En vez de depender de un repo externo inactivo (último commit 2025-03, usa un fork
propio de `mcp-go`), portamos **solo la idea** del `POST /run_task` como una tool
más de este servidor Python. Así queda **un único MCP** que diseña, valida y ejecuta.

Ver la implementación en `src/tasker_mcp/live.py` y la tool `run_tasker_task` en
`server.py`. Es opt-in: solo actúa si se configuran `TASKER_HOST` / `TASKER_API_KEY`.

---

## 4. Ideas del repo externo que valdría la pena adoptar (backlog)

Extraídas de `dceluis/tasker-mcp` (ficha en `Varios_tools/tool_catalog/entries/tasker-mcp-dceluis.md`):

1. **Ejecución en vivo** (`POST /run_task`) → implementada como Opción B.
2. **Parser XML → tools** (`utils/xml-to-tools.js`): el camino inverso a este repo.
   Podríamos leer un `.prj.xml` exportado del teléfono y reconstruir los modelos
   Pydantic (útil para editar automatizaciones existentes). Backlog.
3. **Tools data-driven**: deducir el schema de datos en vez de codificar cada tool.
   Menos relevante aquí porque nuestro valor está en el knowledge base. Backlog.

---

## Notas de realidad

- La **generación de XML es 100 % offline**; la **ejecución en vivo necesita el móvil**
  en red con Tasker corriendo.
- **Kiro Web no puede ejecutar** (sin ruta a la LAN/teléfono); usar Kiro CLI en el NAS
  o el propio teléfono/PC. La generación sí funciona en cualquier sitio.
- El repo externo es MIT; aquí no se copia su código, solo se reimplementa la idea del
  `POST /run_task` de forma independiente en Python.
