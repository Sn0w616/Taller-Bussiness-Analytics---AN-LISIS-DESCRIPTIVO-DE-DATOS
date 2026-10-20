# Taller-Bussiness-Analytics---AN-LISIS-DESCRIPTIVO-DE-DATOS
### R2-A10-S10 ANÁLISIS DESCRIPTIVO DE DATOS
### Extracción, Transformación y Carga de datos — Curso de Big Data

**Autor:** Camilo Andrés González López   
**Tecnologías:** Python, Pandas, SQLite, SQL, Google Colab y Power BI Desktop.

[![Abrir en Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12RkXhLIpbqbb0Zqu352IPXRo4tMljp7h?usp=sharing)

---

## 1. Descripción del proyecto

Este proyecto desarrolla un proceso ETL (*Extract, Transform, Load*) utilizando Python para integrar, limpiar, transformar y almacenar datos provenientes de diferentes fuentes de información.

El ejercicio se desarrolla a partir del caso de estudio de **TecnoAndes**, una tienda de tecnología con operaciones en diferentes ciudades de Colombia. La empresa necesita consolidar la información de ventas, clientes y productos para facilitar el análisis de sus operaciones y apoyar la toma de decisiones.

Los datos de entrada contienen problemas de calidad intencionales, como registros duplicados, fechas en diferentes formatos, valores nulos, cantidades inválidas, inconsistencias en los textos y referencias a clientes inexistentes.

A través del proceso ETL, se busca convertir estas fuentes heterogéneas en información estructurada, consistente y útil para su posterior análisis mediante SQL y Power BI.

## 2. Objetivos

### Objetivo general

Implementar un proceso ETL con Python que permita extraer, depurar, transformar e integrar datos de ventas, clientes y productos, almacenándolos en un modelo de datos que facilite el análisis de información empresarial.

### Objetivos específicos

- Extraer información desde archivos CSV, JSON y Excel.
- Identificar problemas de calidad mediante técnicas de perfilamiento de datos.
- Limpiar registros duplicados, valores nulos e información inválida.
- Estandarizar fechas, textos, categorías y valores numéricos.
- Integrar las fuentes mediante relaciones entre clientes, productos y ventas.
- Construir un pequeño *data warehouse* en SQLite utilizando un modelo estrella.
- Validar la consistencia de los datos cargados mediante consultas SQL.
- Preparar los datos para su visualización y análisis en Power BI Desktop.

## 3. Fuentes de datos

El caso de estudio utiliza tres fuentes principales:

| Archivo | Formato | Descripción |
|---|---|---|
| `ventas.csv` | CSV | Registros de ventas correspondientes al año 2025. |
| `clientes.json` | JSON | Información de los clientes, sus ciudades y fechas de registro. |
| `productos.xlsx` | Excel | Catálogo de productos, categorías y precios unitarios. |

Los archivos son generados mediante un script de Python incluido en el notebook. Esto permite reproducir el ejercicio sin depender de archivos de entrada preparados manualmente.

### Problemas de calidad identificados

Durante el perfilamiento inicial se identifican situaciones como:

- Duplicidad de registros de ventas.
- Fechas almacenadas en distintos formatos.
- Cantidades nulas o negativas.
- Descuentos representados como texto.
- Diferencias en mayúsculas, espacios y tildes.
- Registros de ventas asociados a clientes inexistentes.
- Campos incompletos en la información de los clientes.
- Inconsistencias en los nombres de las categorías de productos.

## 4. Metodología ETL

El desarrollo se divide en tres etapas principales.

### 4.1. Extracción (Extract)

Se leen los archivos de origen mediante las herramientas de Python y Pandas:

- `pandas.read_csv()` para las ventas.
- `json` y `pandas.DataFrame()` para los clientes.
- `pandas.read_excel()` para el catálogo de productos.

Posteriormente, se realiza un perfilamiento inicial para conocer los tipos de datos, la cantidad de registros, los valores nulos, los duplicados y los valores únicos de las columnas.

### 4.2. Transformación (Transform)

En esta etapa se aplican reglas de limpieza, estandarización e integración para mejorar la calidad de los datos.

Las principales operaciones son:

1. Eliminación de registros duplicados, considerando el identificador de venta.
2. Estandarización de fechas mediante formatos explícitos.
3. Identificación y separación de registros rechazados por cantidades o fechas inválidas.
4. Conversión de descuentos expresados como texto a valores numéricos.
5. Normalización de nombres, ciudades, canales y categorías.
6. Verificación de la integridad referencial entre ventas, clientes y productos.
7. Integración de las fuentes mediante operaciones de unión (*joins*).
8. Cálculo de valores derivados, como subtotales, totales, mes, año y trimestre.
9. Validación de reglas de calidad antes de cargar los datos.

Las transformaciones se realizan sobre copias de los datos originales para conservar la información sin procesar y registrar las operaciones de calidad efectuadas.

### 4.3. Carga (Load)

Los datos transformados se almacenan en una base de datos SQLite mediante un modelo estrella.

La estructura principal está compuesta por una tabla de hechos y tres tablas de dimensiones:

| Tabla | Función |
|---|---|
| `fact_ventas` | Almacena las métricas y los identificadores asociados a las ventas. |
| `dim_cliente` | Contiene información descriptiva de los clientes. |
| `dim_producto` | Contiene información de los productos y sus categorías. |
| `dim_fecha` | Permite analizar las ventas por fecha, mes, año y trimestre. |
| `rechazos` | Registra las ventas descartadas durante las validaciones de calidad. |

La base de datos resultante se guarda en:

`salida/tecnoandes_dw.db`

Se utiliza una estrategia de carga completa, reemplazando las tablas existentes durante la ejecución del proceso.

## 5. Pipeline ETL reproducible

Además del desarrollo paso a paso en el notebook, se presenta una versión del proceso organizada en un script de Python denominado `etl_pipeline.py`.

Esta implementación agrupa las operaciones en funciones para facilitar su ejecución, mantenimiento y reutilización. También incorpora registros de ejecución (*logging*) para realizar seguimiento al proceso.

El script generador crea los archivos de entrada y el pipeline los procesa para construir el almacén de datos.

Los archivos principales son:

- `Taller_ETL_Python_GonzalezCamilo.ipynb`: desarrollo documentado del taller.
- `generar_datos.py`: generación de las fuentes de datos de ejemplo.
- `etl_pipeline.py`: implementación del proceso ETL.
- `datos/`: archivos de entrada generados.
- `salida/`: resultados del procesamiento y archivos exportados.

> La carpeta `datos/` y los archivos de `salida/` se generan durante la ejecución. Su presencia en el repositorio depende de cuáles resultados se hayan guardado o publicado.

## 6. Validación y análisis de resultados

Antes de finalizar la carga, se ejecutan comprobaciones para verificar que los datos cumplen las reglas definidas.

Entre las validaciones se encuentran:

- Unicidad de los identificadores de venta.
- Ausencia de fechas nulas.
- Cantidades mayores que cero.
- Descuentos dentro del rango permitido.
- Coherencia entre subtotales y totales.
- Correspondencia de las ciudades con los valores estandarizados.
- Consistencia del año de las transacciones.
- Conciliación entre registros extraídos, cargados, rechazados y duplicados, según las reglas implementadas.

También se realizan consultas SQL para consolidar las ventas por ciudad, categoría, canal y mes.

La información permite explorar el comportamiento comercial y preparar indicadores que faciliten la interpretación de los datos.

## 7. Integración con Power BI Desktop

Como etapa complementaria, el proyecto prepara los datos para su utilización en Power BI Desktop.

Se genera un archivo Excel con una hoja para cada una de las cuatro tablas principales del modelo estrella:

`salida/powerbi/modelo_tecnoandes.xlsx`

También se exportan archivos CSV individuales para las tablas.

Con esta información es posible construir un tablero de análisis de ventas que incluya:

- Ventas totales.
- Número de transacciones.
- Ticket promedio.
- Porcentaje de ventas digitales.
- Evolución mensual de las ventas.
- Comparación de ventas por ciudad.
- Distribución de ventas por categoría de producto.
- Filtros por ciudad, canal y mes.

El notebook incluye ejemplos de medidas DAX y una guía para establecer las relaciones del modelo y validar los resultados del tablero.

**Valor de control documentado:** $801.828.500 en ventas totales, que debe coincidir con el resultado del modelo sin filtros aplicados.

## 8. Tecnologías y herramientas

| Tecnología | Aplicación |
|---|---|
| Python | Desarrollo del proceso ETL. |
| Pandas | Manipulación, limpieza e integración de datos. |
| JSON | Lectura de datos de clientes. |
| SQLite | Almacenamiento del *data warehouse*. |
| SQL | Consultas y análisis de información. |
| Matplotlib | Visualización exploratoria de las ventas. |
| Google Colab | Entorno de ejecución del notebook. |
| Power BI Desktop | Construcción del tablero de análisis. |
| Excel | Exportación de las tablas para Power BI. |

## 9. Requisitos y ejecución

### Opción 1. Ejecutar en Google Colab

Esta es la forma recomendada para desarrollar el taller.

1. Abre el notebook desde el enlace de Google Colab ubicado al inicio de este documento.
2. Guarda una copia en tu Google Drive mediante **Archivo → Guardar una copia en Drive**.
3. Ejecuta las celdas en orden, desde la preparación del entorno hasta la descarga de resultados.
4. Verifica la creación de las carpetas `datos/` y `salida/`.
5. Revisa las tablas, las validaciones de calidad y los resultados de las consultas SQL.
6. Descarga los resultados generados al finalizar el ejercicio.

### Opción 2. Ejecutar en un entorno local

Para ejecutar el proyecto fuera de Colab, se requiere Python 3, las bibliotecas necesarias y los archivos del notebook.

Instala las dependencias con:

```bash
pip install pandas openpyxl matplotlib
```

Ejecuta los scripts desde la raíz del proyecto, una vez que los archivos correspondientes estén disponibles:

```bash
python generar_datos.py
python etl_pipeline.py
```

El proceso genera la base de datos SQLite y los archivos de salida definidos en el código.

**Nota:** el notebook contiene instrucciones específicas de Google Colab, como `!python`, `%%writefile` y la descarga de archivos. Si se desea ejecutar directamente como un script local, deben adaptarse esas instrucciones al entorno utilizado.

## 10. Resultados esperados

Al completar el taller, se espera disponer de:

- Fuentes de datos generadas en formatos CSV, JSON y Excel.
- Diagnóstico de los problemas de calidad identificados.
- Datos depurados, estandarizados e integrados.
- Una bitácora de las transformaciones realizadas.
- Una base de datos SQLite con el modelo estrella.
- Una tabla de registros rechazados para su revisión.
- Un archivo CSV con las ventas limpias.
- Archivos Excel y CSV preparados para Power BI.
- Un pipeline ETL que permite ejecutar nuevamente el procesamiento.
- Una base para construir un tablero de análisis comercial.

## 11. Conclusiones

El desarrollo de este taller permite comprender la importancia de los procesos ETL para convertir datos provenientes de diferentes fuentes en información confiable y estructurada.

La identificación y el tratamiento de inconsistencias son fundamentales para evitar errores en los análisis posteriores. Asimismo, el uso de reglas de calidad, registros de las transformaciones y conciliaciones entre los datos de entrada y salida contribuye a mejorar la trazabilidad del proceso.

La construcción del modelo estrella en SQLite facilita la organización de la información, mientras que la integración con Power BI permite trasladar los resultados técnicos a indicadores y visualizaciones útiles para la toma de decisiones empresariales.

## 12. Autoría y reconocimiento

**Desarrollado por:** Camilo Andrés González López.

**Material de referencia:** el notebook original, creado y distribuido como guía de estudio por el gestor del conocimiento Edgar Mauricio López Rojas.

Universidad de Cundinamarca.
2026
