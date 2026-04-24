# Proyecto Bladerunners | HackODS UNAM 2026

Análisis y tablero interactivo sobre abandono escolar en educación media superior, brecha de género, conectividad y vulnerabilidad territorial en México.

El repositorio ya integra tres piezas del flujo de trabajo:

- un notebook en Python para construir y analizar los datos;
- un dashboard en Quarto para comunicar hallazgos;
- una carpeta `docs/` con la versión publicada del tablero y los reportes exportados.

## Objetivo

El proyecto busca identificar entidades con mayor riesgo estructural de exclusión educativa a partir de indicadores oficiales de:

- abandono escolar en media superior;
- pobreza multidimensional;
- rezago educativo;
- acceso a internet en hogares;
- brecha de género en abandono escolar.

El indicador central es el `Índice de Vulnerabilidad Educativa (IVE)`:

```text
IVE = (pobreza_pct + (100 - internet_hogares_pct)) / 2
```

## Estructura actual del repositorio

```text
hackatonods/
├── README.md
├── pyproject.toml
├── LICENSE
├── declaratoria_IA.md
├── ai-log_template_bladerunners.md
├── dashboard/
│   ├── _quarto.yml
│   ├── custom.scss
│   ├── index.qmd
│   ├── mexico_states.geojson
│   ├── pyproject.toml
│   └── report_utils.py
├── datos/
│   ├── metadata.md
│   └── processed/
│       ├── datos_estados.csv
│       ├── serie_temporal.csv
│       ├── brecha_genero_estados.csv
│       ├── correlaciones_abandono.csv
│       ├── matriz_correlacion.csv
│       ├── coeficientes_modelo.csv
│       ├── resumen_modelos.csv
│       └── zonas_criticas.csv
├── notebooks/
│   ├── 01_pipeline_bladerunners_python.ipynb
│   ├── _quarto.yml
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── report_utils.py
│   └── mexico_states.geojson
├── docs/
│   ├── index.html
│   ├── metadata.md
│   ├── reportes/
│   │   ├── reporte_dashboard_completo.xlsx
│   │   └── zonas_criticas.csv
│   └── index_files/
└── logs/
    └── xvba_debug.log
```

## Flujo de trabajo

### 1. Instalar dependencias

Desde la raíz del proyecto:

```powershell
uv sync
```

Esto instala las dependencias declaradas en `pyproject.toml`, incluyendo `pandas`, `numpy`, `plotly`, `statsmodels`, `jupyter`, `openpyxl` y `quarto-cli`.

### 2. Generar o revisar los insumos analíticos

El notebook principal está en:

```text
notebooks/01_pipeline_bladerunners_python.ipynb
```

Ese notebook documenta la construcción del dataset estatal y genera los archivos analíticos en `datos/processed/`, incluyendo:

- `datos_estados.csv`
- `serie_temporal.csv`
- `correlaciones_abandono.csv`
- `matriz_correlacion.csv`
- `coeficientes_modelo.csv`
- `resumen_modelos.csv`
- `zonas_criticas.csv`
- `brecha_genero_estados.csv`

### 3. Renderizar el dashboard

El tablero fuente está en:

```text
dashboard/index.qmd
```

Para renderizarlo:

```powershell
uv run quarto render dashboard/index.qmd
```

La salida esperada se publica en:

```text
docs/index.html
```

## Qué incluye el dashboard

El dashboard reúne los principales entregables visuales y analíticos del proyecto:

- top 5 de estados con mayor `IVE`;
- mapa nacional del índice de vulnerabilidad;
- lectura exploratoria de correlaciones con abandono escolar;
- visualización de brecha de género por entidad;
- metodología del modelo;
- botones de descarga para reportes y metadatos.

## Artefactos publicados

La carpeta `docs/` ya contiene una versión lista para compartir:

- `docs/index.html`: tablero renderizado;
- `docs/metadata.md`: ficha técnica y limitaciones;
- `docs/reportes/reporte_dashboard_completo.xlsx`: reporte consolidado;
- `docs/reportes/zonas_criticas.csv`: exportación de entidades prioritarias.

## Publicar en GitHub Pages

El repositorio ya quedó listo para desplegar el tablero en GitHub Pages usando GitHub Actions.

1. Sube el contenido a un repositorio en GitHub.
2. En GitHub, entra a `Settings > Pages`.
3. En `Source`, selecciona `GitHub Actions`.
4. Haz push a la rama `main`.

El workflow [`.github/workflows/deploy-pages.yml`](.github/workflows/deploy-pages.yml) instalará dependencias, renderizará `dashboard/index.qmd`, conservará la salida en `docs/` y publicará el sitio automáticamente.

El archivo [`docs/.nojekyll`](docs/.nojekyll) evita que GitHub Pages procese el sitio con Jekyll y ayuda a que los assets estáticos del dashboard se sirvan sin interferencias.

## Fuentes de datos

- INEGI / SEP: abandono escolar en media superior por entidad y sexo, ciclo 2022-2023.
- CONEVAL: pobreza multidimensional y rezago educativo, 2022.
- ENDUTIH 2023: acceso a internet en hogares por entidad.
- UNESCO UIS: referencia de contexto para metas ODS 4.

Más detalle de procedencia y variables en:

- `datos/metadata.md`
- `docs/metadata.md`

## Hallazgo principal

Los estados con mayor pobreza y menor conectividad no siempre coinciden con las mayores tasas observadas de abandono en el corto plazo, pero sí concentran el mayor riesgo estructural. Por eso el tablero prioriza territorio a partir del `IVE` y complementa esa lectura con brecha de género, correlaciones y un modelo exploratorio de regresión.

## Requisitos

- Python 3.11 o superior
- `uv`
- Quarto CLI

## Notas

- `dashboard/` contiene la versión fuente del tablero.
- `notebooks/` concentra la parte reproducible del pipeline analítico.
- `docs/` funciona como salida publicada del proyecto.
- `logs/` contiene archivos auxiliares de ejecución local.
