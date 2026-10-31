# 🤖 BI-Code Copilot: Auditoría y Gobernanza Automatizada de SQL y DAX con IA
[🇪🇸 Español](#-español) | [🇬🇧 English](#-english)

> ✅ **Versión 1.0 Operativa.** Herramienta de automatización interna (*Internal Tooling*) diseñada para auditar, optimizar y documentar repositorios de código analítico (T-SQL y DAX) en lote, compilando informes técnicos de arquitectura en PDF. Nacido como aplicación práctica tras superar la certificación de Inteligencia Artificial de Microsoft.

---

## 🇪🇸 Español

### 📖 Resumen del Proyecto
En los equipos de Ingeniería de Datos y Business Intelligence, la revisión de código (*Code Review*), la optimización de consultas lentas y la documentación técnica suelen convertirse en un cuello de botella operativo. **BI-Code Copilot** automatiza este flujo actuando como un Arquitecto de Datos Senior integrado en la terminal.

Lo diferencial de este proyecto no es simplemente conectar un LLM para explicar código, sino **el enfoque arquitectónico del análisis y la resiliencia del pipeline**: el orquestador escanea directorios completos de scripts `.sql` y `.dax`, evalúa el impacto en los motores de base de datos (**SQL Server Engine** y **Motor Tabular VertiPaq**), detecta antipatrones de modelado y compila automáticamente entregables corporativos en formato PDF listos para negocio o auditoría interna.

### 🛠️ Decisiones de Arquitectura y Stack Tecnológico
Cada herramienta de este proyecto fue seleccionada por un motivo estrictamente funcional y de integración empresarial:

| Componente | Tecnología Elegida | Justificación Arquitectónica (El "Porqué") |
| :--- | :--- | :--- |
| **Orquestación y Lotes** | `Python 3.13` (`os.walk`) | Seleccionado por su ligereza para recorrer árboles de directorios locales o en contenedores CI/CD sin depender de interfaces pesadas. |
| **Motor de Razonamiento** | `google-genai` (`gemini-3.8-flash`) | Elegido por su ventana de contexto y velocidad de inferencia para analizar árboles lógicos de consultas SQL y contextos de filtro DAX complejos en pocos segundos. |
| **Motor de Entregables** | `ReportLab` (Platypus Engine) | Los equipos directivos y de gobernanza no leen salidas de terminal; se optó por compilar documentos PDF vectoriales con jerarquía visual corporativa. |
| **Seguridad y Entorno** | `python-dotenv` | Aislamiento estricto de credenciales y claves de API fuera del código fuente para cumplir con las políticas de seguridad en repositorios Git. |

### 🎯 Puntos Clave
* **Procesamiento Batch Multi-Lenguaje:** Detección y clasificación automática de scripts relacionales (`T-SQL`) y fórmulas tabulares (`DAX`) en una sola ejecución.
* **Diagnóstico de Motor Tabular (VertiPaq):** Identificación de transiciones de contexto costosas, uso correcto de modificadores como `KEEPFILTERS` y desacoplamiento de medidas bajo el principio *DRY (Don't Repeat Yourself)*.
* **Optimización Relacional (SQL Server):** Análisis de planes de ejecución teóricos, alerta sobre *Memory Grants* elevados en operadores `COUNT(DISTINCT)` y generación de scripts DDL para índices *Non-Clustered* con cláusulas `INCLUDE`.
* **Resiliencia ante Caídas de Red (Modo Fallback):** Arquitectura tolerante a fallos que intercepta errores `503 Server Unavailable` de la API para no interrumpir la generación de reportes en demos o pipelines automatizados.

### 💡 Retos y Soluciones Técnicas

#### 0️⃣ Deprecación abrupta de SDKs y bloqueo silencioso en consola 🔍
**Reto:** Al implementar la primera versión del conector con la librería clásica `google.generativeai`, la ejecución en terminal arrojaba advertencias de *FutureWarning* por fin de soporte y las llamadas a la API se quedaban congeladas indefinidamente sin devolver un código de error explícito. **Solución:** Se realizó una migración completa del motor de inferencia al nuevo estándar oficial `google-genai` (v2.31.0), reestructurando la instanciación hacia el objeto `genai.Client()` y eliminando la deuda técnica desde la raíz.

#### 1️⃣ Retirada de modelos legacy (Errores 404 Not Found) 🔄
**Reto:** La velocidad a la que evolucionan los LLMs hace que versiones estándar como `gemini-1.5-flash` o `gemini-2.5-flash` dejen de estar disponibles para nuevas peticiones en el endpoint `v1beta`, rompiendo el flujo de ejecución con excepciones `404 NOT_FOUND`. **Solución:** Actualización del pipeline al modelo de producción vigente (`gemini-3.8-flash`), ajustando la estructura de los prompts del sistema para aprovechar su mayor capacidad de diagnóstico sobre motores columnares y relacionales.

#### 2️⃣ Reintentos infinitos y picos de demanda en la nube (Error 503) 🛡️
**Reto:** El nuevo SDK incorpora la librería `tenacity` bajo el capó para reintentar peticiones automáticamente cuando los servidores de Google sufren picos de demanda global (`503 UNAVAILABLE`). Esto provocaba que el script pareciera colgado durante minutos antes de abortar el proceso completo. **Solución:** Implementación de manejo de excepciones robusto (`try/except`) con inyección de un **Modo Fallback de Contingencia**, garantizando que el orquestador continúe con el resto de archivos del lote y genere el PDF igualmente.

#### 3️⃣ Interrupción prematura en el escaneo de directorios 📂
**Reto:** En la primera iteración del lector de archivos, el uso de una sentencia `return` directa dentro del bucle `os.walk("inputs")` provocaba que el sistema procesara únicamente el primer archivo encontrado (el `.dax`) e ignorara silenciosamente las subcarpetas de `sql/`. **Solución:** Refactorización hacia una arquitectura de recolección en lista (`get_all_inputs()`), desacoplando la fase de descubrimiento de archivos de la fase de inferencia y maquetación en lote.

#### 4️⃣ Conversión de Markdown crudo a maquetación PDF corporativa 📄
**Reto:** Los modelos de lenguaje devuelven texto estructurado en Markdown (con encabezados `##`, listas y bloques de código), pero el motor `SimpleDocTemplate` de ReportLab no interpreta Markdown de forma nativa, lo que generaba texto plano difícil de leer. **Solución:** Construcción de un parser ligero línea a línea que transforma las etiquetas Markdown en objetos `Paragraph`, `Spacer` y `HRFlowable` con estilos tipográficos corporativos (`#1E3A8A` y `#0F172A`).

### 🚀 Cómo ejecutarlo localmente
```bash
# 1. Clonar el repositorio y entrar al directorio
git clone [https://github.com/floresdelolmo-ai/bi-code-copilot.git](https://github.com/floresdelolmo-ai/bi-code-copilot.git)
cd bi-code-copilot

# 2. Crear entorno virtual e instalar dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configurar clave de API en archivo .env
echo 'GEMINI_API_KEY="tu_clave_aqui"' > .env

# 4. Ejecutar el procesamiento por lotes
python src/workflow.py