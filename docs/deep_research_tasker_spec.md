# Especificación Técnica del Motor Interno de Tasker para Compilación XML vía FastMCP
*Generado vía Google Gemini Deep Research (@investigador-pro-v2) - Noviembre 2026*

Construir un servidor **FastMCP (Model Context Protocol)** capaz de compilar, validar y auditar automatizaciones para **Tasker en Android** exige operar directamente sobre el Árbol de Sintaxis Abstracta (AST) serializado en XML (`<TaskerData>`), sus contratos posicionales de argumentos y el mapa real de permisos de Android 10–16+. El motor de ejecución de Tasker no interpreta nombres legibles de acciones ni parámetros nominales: despacha códigos numéricos de operación (`<code>`), consume argumentos posicionales tipados (`<Str>`, `<Int>`, `<Bundle>`) y mantiene integridad referencial mediante identificadores internos (`<id>`, `<mid0>`, `<mid1>`, `<pids>`, `<tids>`).

Para emitir artefactos importables sin errores sintácticos, el servidor FastMCP debe implementar una arquitectura de **esquema híbrido**: combinar el catálogo comunitario verificado de `Tasker_XML_Codes.md` —cuya instantánea documentada corresponde a Tasker v5.15.5-beta con 373 acciones de tarea, 82 eventos de perfil, 50 estados de perfil y 12 códigos obsoletos— con la ingestión dinámica del archivo nativo `/storage/emulated/0/Tasker/meta/datadef.xml` exportado desde el dispositivo objetivo (*Options > More > Developer Options > Save Data Definitions*). Esta hidratación en tiempo de ejecución cubre los huecos no publicados en tablas comunitarias estáticas: las acciones y eventos introducidos entre Tasker v6.2 y v6.7 (*HTTP Response*, *Received Share*, *Get Calendar Events*, *Java Code*, *Shizuku Available*, *Scene V2*), el mapeo completo de operadores `<op>` y las firmas posicionales de acciones sin exportaciones de referencia. Al mismo tiempo, la integración nativa de **Shizuku** en Tasker v6.6 y la suite auxiliar de João Dias (*Tasker Settings*, *Tasker Permissions* y *AutoApps*) eliminan la mayoría de los falsos límites técnicos sin acceso root.

---

## 1. Especificación del Motor de Bajo Nivel: XML DOM, Códigos de Operación y Contratos de Serialización

### 1.1 Taxonomía de Exportaciones y Jerarquía del DOM XML

Tasker encapsula todas sus configuraciones bajo el nodo raíz `<TaskerData sr="" dvi="1" tv="X.Y.Z">`, donde `tv` registra la versión de Tasker que generó el archivo y `dvi` acompaña la cabecera de formato de datos. Aunque el índice general del repositorio comunitario Tasker-XML-Info encabeza la sección como cuatro tipos, en su especificación enumera cinco formatos XML distintos diferenciables tanto por sufijo como por sus nodos hijos inmediatos. Un parser o compilador MCP debe clasificar siempre los documentos inspeccionando sus nodos estructurales para tolerar archivos renombrados:

| Tipo de Exportación | Sufijo | Nodos Contenidos y Reglas de Autocontención | Regla de Detección Estructural |
| :--- | :--- | :--- | :--- |
| **Data Backup** | `.xml` | Configuración íntegra del dispositivo: todos los `<Project>`, `<Profile>`, `<Scene>`, `<Task>` y `<dmetric>`. | Contiene la configuración global completa y múltiples proyectos. |
| **Project** | `.prj.xml` | Un `<Project>` más todos los perfiles, escenas y tareas que contiene y cualquier entidad de otros proyectos referenciada o invocada por él, produciendo un paquete autocontenido (*standalone*). | Nodo `<Project>` acompañado de los nodos enlazados por `<pids>`, `<tids>` y `<scenes>`. |
| **Profile** | `.prf.xml` | Un `<Profile>` junto con sus tareas referenciadas, incluidas las tareas anónimas de entrada (`<mid0>`) y salida (`<mid1>`) que carecen de etiqueta `<nme>`. | Presencia de `<Profile>` sin `<Project>` y sus nodos `<Task>` dependientes. |
| **Scene** | `.scn.xml` | Un `<Scene>` con `<PropertiesElement>`, elementos visuales y las tareas anónimas disparadas por eventos UI (`<clickTask>`, `<longclickTask>`, `<itemclickTask>`, `<keyTask>`, etc.). | Un único nodo `<Scene>` y nodos `<Task>` opcionales sin etiqueta `<nme>`. |
| **Task** | `.tsk.xml` | Exclusivamente el nodo `<Task>` exportado. | Un único nodo `<Task>` hijo de `<TaskerData>`. |

El elemento `<dmetric>` almacena el ancho y alto del área utilizable de pantalla (excluyendo la barra de navegación) para escalar escenas entre dispositivos. De manera transversal, los nodos estructurales emplean dos atributos sistemáticos: `sr` (identificador de referencia dentro del contenedor padre, como `proj0`, `prof34`, `task4`, `con0`, `act0`, `arg0`, `c0`, `pv0` o `icn`) y `ve` (versión de esquema del nodo: `ve="2"` en Project, Profile, State, Event e Img; `ve="3"` en Str y Condition; y `ve="7"` en Action).

En exportaciones reales se observan contratos estructurales específicos por nodo padre:
* Un nodo `<Project sr="proj0" ve="2">` exige `<name>`, registra `<cdate>`, enumera sus miembros en listas separadas por comas mediante `<pids>`, `<tids>` y `<scenes>`, y opcionalmente incluye ordenamiento (`<psort>`, `<tsort>`), metadatos de App Factory (`<Kid>`), ficha de publicación (`<Share>`), icono (`<Img sr="icon" ve="2">`) y variables de proyecto (`<ProfileVariable sr="pvN">`).
* Un `<Profile sr="profN" ve="2">` exige `<id>` y al menos un subnodo de contexto (`<App>`, `<Day>`, `<Event>`, `<Loc>`, `<State>` o `<Time>`), además de los nodos opcionales `<nme>`, `<cdate>`, `<edate>`, `<clp>` (p. ej., `true`), `<flags>` (p. ej., `8`), `<mid0>` (ID de tarea de entrada) y `<mid1>` (ID de tarea de salida).
* Por último, `<Task sr="taskN">` requiere `<id>` y al menos un `<Action>`, junto con etiquetas opcionales de control de ejecución: `<nme>` (omitida en tareas anónimas), `<cdate>` y `<edate>`, `<pri>` (prioridad entera, p. ej., `100`), `<rty>` (manejo de colisiones: `0` o ausente = *Abort New Task*, `1` = *Abort Existing Task*, `2` = *Run Both Together*), `<stayawake>` (`false`/ausente o `true`), `<ProfileVariable>` e `<Img sr="icn" ve="2">`.

---

### 1.2 Mapeo de Códigos Numéricos de Acción (Action Codes), Argumentos Posicionales y Banderas

Una particularidad crítica del serializador nativo de Tasker es que **ordena los nodos hijos de argumentos de forma lexicográfica por `sr` y no numérica** (`arg1`, `arg10`, `arg11`, `arg12`, `arg2`...). Históricamente, cualquier desajuste de tipo en un argumento invalidaba la importación; desde Tasker v6.5.5-beta, el importador fue endurecido para ignorar argumentos con tipos erróneos en lugar de descartar la acción entera.

En cuanto a las banderas de nivel de acción, las exportaciones verificadas confirman el uso de `<label>` (etiqueta textual de salto o documentación) y `<coll>false</coll>` (estado visual en bloques If). Por el contrario, respecto a las banderas booleanas de control de error (`<se>false</se>` para *Continue Task After Error*) y deshabilitación (`<on>false</on>`), las exportaciones XML analizadas confirman la existencia funcional de *Continue Task After Error*, vinculada a `%err` y `%errmsg`.

La siguiente tabla reúne los códigos verificados en `Tasker_XML_Codes.md` (v5.15.5-beta) y las firmas posicionales confirmadas directamente en exportaciones XML reales:

| Acción en UI | Código (`<code>`) | Argumentos Posicionales Observados (`arg0`..`argN`) y Tipos XML | Notas de Compilación y Banderas |
| :--- | :--- | :--- | :--- |
| **HTTP Request** | `339` | `arg0`: `<Bundle>` (`RELEVANT_VARIABLES`) \| `arg1`: `<Int>` (0 en GET) \| `arg2`: `<Str>` (URL) \| `arg3`: `<Str>` (Headers, ej. `%http_auth_headers`) \| `arg4`..`arg6`: `<Str>` (vacíos en GET) \| `arg7`: `<Str>` (directorio/archivo de salida, ej. `Download`) \| `arg8`: `<Int>` (5, timeout) \| `arg9`..`arg12`: `<Int>` (0, 0, 0, 1) | Reemplaza a las obsoletas 116 (HTTP Post), 117 (HTTP Head) y 118 (HTTP Get). Activar Continue Task After Error si se validará `%err`. |
| **HTTP Auth** | `351` | `arg0`: `<Bundle>` (`RELEVANT_VARIABLES` con `%http_auth_headers`) \| `arg1`: `<Int>` (1) \| `arg2`..`arg6`: `<Str>` \| `arg7`..`arg8`: `<Int>` (0, 30) \| `arg9`..`arg10`: `<Str>` (credenciales, ej. `admin`) | Genera `%http_auth_headers` para encadenar en `arg3` de HTTP Request 339. |
| **Variable Set** | `547` | `arg0`: `<Str>` (Nombre `%var`) \| `arg1`: `<Str>` (Valor o expresión) \| `arg2`..`arg6`: `<Int>` (0, 0, 0, 3, 0) | Soporta consultas de arrays y regex en `arg1` como `%apps.app(#?~R^%name$)`. |
| **Flash** | `548` | `arg0`: `<Str>` (Texto) \| `arg1`..`arg2`: `<Int>` \| `arg3`..`arg8`: `<Str>` \| `arg9`: `<Int>` (1) \| `arg10`: `<Str>` \| `arg11`: `<Int>` (1) \| `arg12`: `<Int>` (0) \| `arg13`: `<Str>` \| `arg14`: `<Int>` (0) \| `arg15`: `<Str>` | Expande hasta 16 argumentos (`arg0`..`arg15`) en versiones modernas (layout de Tasker, Continue Task Immediately, Dismiss On Click). |
| **Perform Task** | `130` | `arg0`: `<Str>` (Nombre de tarea) \| `arg1`: `<Int>` (polimórfico: atributo `val` o hijo `<var>%priority</var>`) \| `arg2`..`arg4`: `<Str>` \| `arg5`..`arg6`: `<Int>` \| `arg7`: `<Str>` \| `arg8`..`arg10`: `<Int>` (0, 0, 1) | En UI expone `%par1`, `%par2`, Return Value Variable, Stop y Local Variable Passthrough. Regla clave: `arg1` acepta `<var>%priority</var>` en vez de `val`. |
| **Return** | `126` | `arg0`: `<Str>` (Valor de retorno, ej. `%pkg`) \| `arg1`..`arg3`: `<Int>` (1, 0, 0) \| `arg4`: `<Str>` | Devuelve datos a la variable receptora del llamador Perform Task 130. |
| **If / Else / End If** | `37` / `43` / `38` | `37` emplea `<ConditionList sr="if">` con nodos `<Condition sr="cN" ve="3">` (`<lhs>`, `<op>`, `<rhs>`). `43` y `38` no llevan argumentos posicionales en el flujo estándar. | `37` admite `<coll>false</coll>`. |
| **Goto** | `135` | Expone Type, Number y Label. | Restringir siempre a Type: Action Label apuntando a un `<label>` existente. |
| **Anchor** | `300` | Emplea `<label>...</label>` dentro de `<Action>` sin argumentos funcionales requeridos. | Destino preferente de Goto 135 y marcador de ayuda al inicio de tareas. |
| **Run Shell** | `123` | `arg0`: `<Str>` (Comando shell) \| `arg1`..`arg2`: `<Int>` (0, 1) \| `arg3`..`arg5`: `<Str>` \| `arg6`..`arg7`: `<Int>` (1, 0) | Soporta ejecución con Shizuku desde v6.6 y Use Tasker Settings. |
| **Set Clipboard** | `105` | `arg0`: `<Str>` (Texto, ej. `%http_data[Clipboard]`) \| `arg1`: `<Int>` (0) \| `arg2`: `<Str>` \| `arg3`: `<Int>` (0) | En segundo plano (Android 10–14+) requiere permisos ADB/READ_LOGS. |
| **Read File / Write File** | `417` / `410` | `417`: `arg0` `<Str>` (Ruta), `arg1` `<Str>` (Var destino), `arg2` `<Int>` (1). `410`: `arg0` `<Str>` (Ruta), `arg1` `<Str>` (Contenido), `arg2`..`arg3` `<Int>` (0, 0). | Ejemplo verificado sobre `Download/check.txt`. |
| **Plugins de Terceros / AutoApps** | `1000` (código base en tabla) o entero específico por acción (ej. `107361459` en AutoInput Action v2) | `arg0`: `<Bundle>` con `<Vals sr="val">` (pares `<clave>` + `<clave-type>`) \| `arg1`: `<Str>` (Package Name, ej. `com.joaomgcd.autoinput`) \| `arg2`: `<Str>` (Activity de configuración) \| `arg3`: `<Int>` (Timeout, ej. 60) \| `arg4`: `<Int>` (1) | Las exportaciones reales de plugins emiten un entero específico del plugin/acción. |

---

## 2. Structured Output (JSON, HTML/XML, CSV), Referencias Indirectas y Arrays

Desde Tasker v5.12, las variables creadas con **Structured Output** habilitado permiten evaluar estructuras directamente:
* **JSON**: `%json.name` o `%json[name]` devuelve la primera coincidencia y `%json.name()` devuelve una lista separada por comas de todos los valores coincidentes. Claves simples (`%json.name`) buscan en profundidad; rutas compuestas (`%json.names.name`) hacen coincidencia exacta. La clave reservada `=:=root=:=` lee el array raíz (`%json_array[=:=root=:=]()`). **Regla estricta:** si una clave contiene mayúsculas o espacios (`SomeField`), la notación con punto está prohibida y debe usarse corchetes (`%json[SomeField]`).
* **HTML/XML**: `%html.div` o `%html[div]` extrae el texto del primer elemento, `=:=` accede a atributos (`%html[img=:=src]`) y `=:=html` devuelve el bloque HTML (`%html[body=:=html]`).
* **CSV**: `%csv.columna` y `%csv.columna()` leen el primer valor o la columna completa.
* **Arrays y Operadores**: Arrays 1-indexados (`%arr1`..`%arrN`):
  * `%arr(#)`: cantidad total de elementos.
  * `%arr(#>)` / `%arr(#<)`: primer / último índice definido.
  * `%arr(#?~Rregex)`: índices coincidentes por regex.
  * `%arr(2:4)`: subrango de elementos.
  * `%arr(+=+)`: unión con separador personalizado.
  * Doble referencia: `%%varname` resuelve nombres de variables indirectamente.

---

## 3. Reglas de Oro del Intérprete para Generación de XML

1. **Saltos Goto (135) exclusivos por `<label>`:** Prohibir saltos por número de acción.
2. **Tareas Anónimas vs. Nombradas:** Tareas sin `<nme>` permitidas únicamente cuando pertenezcan a un `<Profile>` (`<mid0>`/`<mid1>`) o `<Scene>`. Toda tarea en `<Project>` o invocada con Perform Task (130) exige `<nme>` y registro en `<tids>`.
3. **Reglas Léxicas de Variables:** Prefijo `%`, al menos 3 caracteres alfanuméricos, sin guiones bajos al inicio o al final.
4. **Structured Output y Notación:** Usar `%json[SomeField]` si hay mayúsculas o espacios.
5. **Polimorfismo `<Int>` / `<var>`:** Cuando el argumento entero sea una variable, emitir `<Int sr="arg1"><var>%priority</var></Int>` en vez de `val="%priority"`.
6. **Volatilidad Inmediata de `%err` / `%errmsg`:** Capturar `%err` en la acción inmediatamente posterior junto con *Continue Task After Error*.

---

## 4. Ecosistema Satélite de João Dias (`joaomgcd`), Helpers y Restricciones de Android

| Componente | Package ID / Origen | Restricciones que Resuelve |
| :--- | :--- | :--- |
| **AutoInput** | `com.joaomgcd.autoinput` | Control de UI sin Root mediante Accesibilidad reactiva: clics, UI Query, UI Update (espera reactiva por app), gestos y captura de teclas. |
| **AutoNotification** | `com.joaomgcd.autonotification` | Interceptación avanzada de notificaciones (WhatsApp, bancos), consultas con campos JSON y Quick Reply en segundo plano. |
| **AutoTools** | `com.joaomgcd.autotools` | Ajustes de sistema seguros sin root, OCR en pantalla, parseo JSON nativo y cuadros de diálogo WebScreens. |
| **AutoLocation** | `com.joaomgcd.autolocation` | Geovallas de hardware y reconocimiento de actividad física sin agotar la batería en segundo plano. |
| **Join** | `com.joaomgcd.join` | Comunicación bidireccional Android-PC, portapapeles compartido y disparo remoto de tareas. |
| **Tasker Settings** | GitHub `joaomgcd/TaskerSettings` | Alternar Wi-Fi en Android 10+ (API 29), Bluetooth en Android 13+ (API 33), Hotspot y saltar el bloqueo de instalación de APKs en Android 14+. |
| **Shizuku** | `moe.shizuku.privileged.api` | Privilegios ADB inalámbricos de sistema sin Root ni PC para Airplane Mode, Wi-Fi, Red Móvil, Dumpsys y Tethering en Android 16+. |
