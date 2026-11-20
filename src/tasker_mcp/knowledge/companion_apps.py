"""Catálogo del Ecosistema de Companion Apps y Plugins Oficiales de João Dias (joaomgcd).

Resuelve el problema de falsos límites técnicos: cuando Tasker nativo no puede
realizar una tarea por restricciones del sistema operativo Android, estos plugins
oficiales proporcionan la capacidad requerida.
"""

from typing import Optional, TypedDict

class CompanionAppInfo(TypedDict):
    name: str
    developer: str
    package_name: str
    type: str  # "system_helper" | "autoapp_plugin"
    source: str  # "Play Store" | "GitHub" | "Web"
    url: str
    purpose: str
    solves_restriction: str
    typical_use_cases: list[str]

COMPANION_APPS_REGISTRY: dict[str, CompanionAppInfo] = {
    "autolocation": {
        "name": "AutoLocation",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autolocation",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autolocation",
        "purpose": "Geolocalización avanzada, geovallas (geofencing) de ultra bajo consumo y reconocimiento de actividad física.",
        "solves_restriction": "Android restringe el GPS en segundo plano y el escaneo constante agota la batería. AutoLocation usa la API de Google Fused Location y hardware geofences sin despertar la CPU continuamente.",
        "typical_use_cases": [
            "Rastreo de ubicación periódico en segundo plano sin drenar batería",
            "Geovallas de llegada/salida (llegar a casa, oficina, colegio)",
            "Detectar actividad del usuario (en vehículo, en bicicleta, caminando, corriendo, quieto)",
        ]
    },
    "autoinput": {
        "name": "AutoInput",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autoinput",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autoinput",
        "purpose": "Automatización de interfaz gráfica (UI Automation) sin Root mediante Servicios de Accesibilidad.",
        "solves_restriction": "Tasker nativo no puede interactuar con aplicaciones de terceros que carecen de API. AutoInput permite hacer clics, escribir texto y leer la pantalla.",
        "typical_use_cases": [
            "Hacer clics automáticos en botones de cualquier app de terceros",
            "Escribir credenciales o búsquedas en cuadros de texto",
            "Inspeccionar y extraer texto visible en pantalla (Screen scraping)",
            "Detectar pulsaciones de teclas de hardware o gestos",
        ]
    },
    "autonotification": {
        "name": "AutoNotification",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autonotification",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autonotification",
        "purpose": "Control total de notificaciones de Android, interceptación de mensajes y creación de notificaciones interactivas.",
        "solves_restriction": "Tasker nativo solo puede crear notificaciones simples y tiene soporte limitado para leer datos internos de notificaciones de terceros (como botones de acción o respuestas directas).",
        "typical_use_cases": [
            "Interceptar notificaciones de WhatsApp, Telegram, correo o bancos y extraer variables (remitente, cuerpo, id)",
            "Responder mensajes en segundo plano simulando la acción 'Quick Reply'",
            "Bloquear o cancelar notificaciones molestas de otras apps",
            "Crear notificaciones con botones personalizados, listas y barras de progreso complejas",
        ]
    },
    "autovoice": {
        "name": "AutoVoice",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autovoice",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autovoice",
        "purpose": "Reconocimiento y procesamiento de lenguaje natural por voz, integración con Google Assistant y Amazon Alexa.",
        "solves_restriction": "Tasker solo ofrece reconocimiento de voz rudimentario con el cuadro de diálogo estándar de Google. AutoVoice permite escucha continua en segundo plano y comandos en lenguaje natural estructurado.",
        "typical_use_cases": [
            "Reconocimiento de comandos por voz continuos con Regex y variables automáticas",
            "Creación de Skills personalizadas de Alexa que ejecutan tareas en el teléfono",
            "Integración de rutinas de Google Home disparando eventos en Tasker",
        ]
    },
    "autotools": {
        "name": "AutoTools",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autotools",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autotools",
        "purpose": "La navaja suiza de utilidades avanzadas: diálogos HTML/Web, OCR, JSON parsing, gestos y Secure Settings.",
        "solves_restriction": "Permite escribir en configuraciones globales/seguras de Android sin root, parsear JSON sin scripts complejos y mostrar cuadros de diálogo modernos que Tasker nativo no ofrece.",
        "typical_use_cases": [
            "Parseo y filtrado rápido de estructuras JSON complejas",
            "OCR (reconocimiento óptico de caracteres) en imágenes o capturas",
            "Diálogos avanzados (selectores de fecha, listas con imágenes, sliders)",
            "Ajustes de sistema seguros (Secure Settings) mediante permiso ADB",
        ]
    },
    "autosheets": {
        "name": "AutoSheets",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.autosheets",
        "type": "autoapp_plugin",
        "source": "Play Store",
        "url": "https://play.google.com/store/apps/details?id=com.joaomgcd.autosheets",
        "purpose": "Lectura y escritura nativa en hojas de cálculo de Google Sheets sin configurar complejas APIs de Google Cloud.",
        "solves_restriction": "Conectar Tasker a Google Sheets directamente mediante HTTP Request exige gestionar tokens OAuth2 complejos. AutoSheets abstrae toda la autenticación con un solo clic.",
        "typical_use_cases": [
            "Registrar gastos, registros de llamadas o ubicaciones en una hoja de Google Sheets en la nube",
            "Consultar valores o configuraciones guardadas en una hoja para usarlas en Tasker",
        ]
    },
    "join": {
        "name": "Join by joaoapps",
        "developer": "joaomgcd",
        "package_name": "com.joaomgcd.join",
        "type": "autoapp_plugin",
        "source": "Play Store / Web / Chrome Extension",
        "url": "https://joinjoaomgcd.appspot.com/",
        "purpose": "Interconexión y mensajería bidireccional entre dispositivos (Android, PC con Windows/Mac/Linux, navegadores web).",
        "solves_restriction": "Tasker solo corre localmente en el dispositivo. Join permite enviar comandos de Tasker desde la PC o entre diferentes teléfonos de forma cifrada.",
        "typical_use_cases": [
            "Sincronizar portapapeles universal entre PC y teléfono",
            "Enviar SMS desde la computadora a través del teléfono con Tasker",
            "Disparar tareas de Tasker en el móvil desde un script en la PC o un webhook remoto",
        ]
    },
    "tasker_settings": {
        "name": "Tasker Settings",
        "developer": "joaomgcd",
        "package_name": "net.dinglisch.android.taskerm",
        "type": "system_helper",
        "source": "GitHub",
        "url": "https://github.com/joaomgcd/TaskerSettings/releases",
        "purpose": "Helper de sistema que retiene permisos heredados para ejecutar acciones bloqueadas en Android 10+.",
        "solves_restriction": "Android 10+ bloquea conmutar Wi-Fi, Android 13+ bloquea Bluetooth, Android 14+ bloquea instalación de APKs viejos. Tasker Settings actúa como puente con SDK antiguo para saltarse estas restricciones.",
        "typical_use_cases": [
            "Alternar Wi-Fi en Android 10 y versiones superiores",
            "Alternar Bluetooth en Android 13+",
            "Alternar punto de acceso (Wi-Fi Tether / Hotspot)",
            "Modificar tamaño de pantalla o apagar modo No Molestar en Android moderno",
        ]
    },
    "shizuku": {
        "name": "Shizuku",
        "developer": "Rikka",
        "package_name": "moe.shizuku.privileged.api",
        "type": "system_helper",
        "source": "Play Store / GitHub",
        "url": "https://shizuku.rikka.app/",
        "purpose": "Servidor de privilegios ADB en segundo plano que otorga permisos de nivel de sistema sin requerir Root.",
        "solves_restriction": "Muchos comandos de Tasker (o instalación de Tasker Settings en Android 14+) requieren una PC con cable ADB. Shizuku permite mantener privilegios ADB inalámbricos directamente desde el móvil.",
        "typical_use_cases": [
            "Instalar Tasker Settings en Android 14+ sin conectar a una PC",
            "Ejecutar comandos en la acción 'ADB Wifi' o 'Run Shell' con privilegios elevados sin Root",
            "Activar Hotspot en Android 16+",
        ]
    }
}

def get_companion_app(app_key: str) -> Optional[CompanionAppInfo]:
    """Obtiene la información técnica de una companion app por su clave."""
    return COMPANION_APPS_REGISTRY.get(app_key.lower().strip())

def list_companion_apps() -> list[CompanionAppInfo]:
    """Lista todas las companion apps y plugins oficiales catalogados."""
    return list(COMPANION_APPS_REGISTRY.values())

def find_plugin_for_need(need_description: str) -> list[CompanionAppInfo]:
    """Busca y recomienda qué plugin oficial resuelve una necesidad o restricción técnica."""
    desc_lower = need_description.lower()
    matches = []
    
    keywords_map = {
        "autolocation": ["ubicacion", "ubicación", "gps", "geofence", "geovalla", "rastrear", "rastreo", "coche", "hermano", "bateria"],
        "autoinput": ["clic", "click", "tocar", "pantalla", "interfaz", "ui", "escribir texto", "scrape", "leer pantalla"],
        "autonotification": ["notificacion", "notificación", "whatsapp", "telegram", "mensaje", "responder", "quick reply"],
        "autovoice": ["voz", "alexa", "google assistant", "hablar", "microfono", "comando de voz"],
        "autotools": ["json", "ocr", "dialogo", "diálogo", "secure settings", "texto en imagen"],
        "autosheets": ["sheet", "sheets", "hoja de calculo", "google sheets", "excel", "registro"],
        "join": ["pc", "computadora", "remoto", "portapapeles", "compartir", "sms desde pc"],
        "tasker_settings": ["wifi", "wi-fi", "bluetooth", "hotspot", "tether", "android 10", "android 13", "android 14"],
        "shizuku": ["adb", "sin root", "privilegios", "permisos adb", "inalambrico"]
    }
    
    for key, keywords in keywords_map.items():
        if any(kw in desc_lower for kw in keywords):
            app = COMPANION_APPS_REGISTRY[key]
            if app not in matches:
                matches.append(app)
                
    return matches
